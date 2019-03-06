import datetime
import os
import os.path
import uuid

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from .base import BaseComponent


class CertificateAuthority(BaseComponent):
    componentName = "CA"

    _seen_names = {}

    @property
    def is_inited(self):
        return self.state.oc_object_exists(
            "secret",
            "cacert",
        )

    def create_build(self):
        self.logger.debug("Nothing to build for CA")

    def create(self):
        self.create_ca()
        self.register_openshift()

    @property
    def path(self):
        return os.path.abspath(os.path.join(self.state.config.state_dir, "ca"))

    def _check_seen_name(self, certtype, name):
        if self._seen_names.get(name) not in (None, certtype):
            raise ValueError("Cert for name %s previously known as other type")
        self._seen_names[name] = certtype

    @staticmethod
    def extcb_noca(cert):
        cert = cert.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        cert = cert.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=True,
                key_encipherment=True,
                data_encipherment=True,
                key_agreement=True,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        return cert

    def generate_extcb_service(self, service_name, *hostnames):
        def extcb(cert):
            cert = CertificateAuthority.extcb_noca(cert)
            cert = cert.add_extension(
                x509.SubjectAlternativeName(
                    [
                        x509.DNSName(service_name),
                    ] +
                    [
                        x509.DNSName(hostname)
                        for hostname
                        in hostnames
                    ]
                ),
                critical=True,
            )
            cert = cert.add_extension(
                x509.ExtendedKeyUsage(
                    usages=[
                        x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
                    ],
                ),
                critical=True,
            )
            return cert
        return extcb

    def _ensure_service_cert(self, service_name, *hostnames):
        if not os.path.exists(os.path.join(self.path,
                                           "%s.key" % service_name)):
            self.logger.info("Creating service cert for %s", service_name)
            self.create_cert(
                name=service_name,
                signer_key=self.ca_key,
                issuer_cn=None,
                subject_cn=service_name,
                extcb=self.generate_extcb_service(service_name,
                                                  *hostnames),
            )

    def _register_service_cert(self, service_name):
        self.logger.info("Registering service cert for %s", service_name)
        self.state.oc_create_secret_tls(
            "cert-%s" % service_name,
            os.path.join(self.path, "%s.crt" % service_name),
            os.path.join(self.path, "%s.key" % service_name),
        )

    def create_service_cert(self, service_name, *hostnames):
        if service_name == "ca":
            raise ValueError("'ca' is not a valid CA service name")
        self._check_seen_name("service", service_name)
        if not self.state.oc_object_exists("secret", "cert-%s" % service_name):
            self._ensure_service_cert(service_name, *hostnames)
            self._register_service_cert(service_name)

    def _ensure_client_cert(self, client_name):
        if not os.path.exists(os.path.join(self.path,
                                           "%s.key" % client_name)):
            self.logger.info("Creating client cert for %s", client_name)
            self.create_cert(
                name=client_name,
                signer_key=self.ca_key,
                issuer_cn=None,
                subject_cn=client_name,
                extcb=self.generate_extcb_client(),
            )

    def _register_client_cert(self, client_name):
        self.logger.info("Registering client cert for %s", client_name)
        self.state.oc_create_secret_tls(
            "cert-client-%s" % client_name,
            os.path.join(self.path, "%s.crt" % client_name),
            os.path.join(self.path, "%s.key" % client_name),
        )

    def generate_extcb_client(self):
        def extcb(cert):
            cert = CertificateAuthority.extcb_noca(cert)
            cert = cert.add_extension(
                x509.ExtendedKeyUsage(
                    usages=[
                        x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
                    ],
                ),
                critical=True,
            )
            return cert
        return extcb

    def create_client_cert(self, client_name):
        if client_name == "ca":
            raise ValueError("'ca' is not a valid client name")
        self._check_seen_name("client", client_name)
        if not self.state.oc_object_exists("secret",
                                           "cert-client-%s" % client_name):
            self._ensure_client_cert(client_name)
            self._register_client_cert(client_name)

    def register_openshift(self):
        """ Create the CA certificate "secret" in Openshift. """
        if not self.state.oc_object_exists("secret", "cacert"):
            self.logger.info("Registering CA certificate in Openshift")
            self.state.oc_create_secret_file(
                "cacert",
                {
                    "cert": os.path.join(self.path, "ca.crt"),
                }
            )

    @property
    def ca_cert(self):
        with open(os.path.join(self.path, "ca.crt"), "rb") as f:
            return x509.load_pem_x509_certificate(
                data=f.read(),
                backend=default_backend(),
            )

    @property
    def ca_key(self):
        with open(os.path.join(self.path, "ca.key"), "rb") as f:
            return serialization.load_pem_private_key(
                data=f.read(),
                password=None,
                backend=default_backend(),
            )

    def create_cert(self, name, signer_key, issuer_cn, subject_cn, extcb):
        # Generate a new certificate and key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        if signer_key is None:
            signer_key = private_key
        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME,
                               subject_cn)
        ])
        if issuer_cn is None:
            issuer = self.ca_cert.subject
        else:
            issuer = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME,
                                   issuer_cn)
            ])
        builder = x509.CertificateBuilder(
            subject_name=subject,
            issuer_name=issuer,
            not_valid_before=datetime.datetime.now()-datetime.timedelta(
                days=1,  # Otherwise timezones become a challenge....
            ),
            not_valid_after=datetime.datetime.now()+datetime.timedelta(
                days=365*10),
            serial_number=int(uuid.uuid4()),
            public_key=private_key.public_key(),
        )
        builder = extcb(builder)
        cert = builder.sign(
            private_key=signer_key,
            algorithm=hashes.SHA256(),
            backend=default_backend(),
        )

        with open(os.path.join(self.path, "%s.crt" % name), "wb") as f:
            f.write(cert.public_bytes(
                encoding=serialization.Encoding.PEM,
            ))

        # More complicated os.open to create file as 0600
        with open(os.open(
                os.path.join(self.path, "%s.key" % name),
                os.O_CREAT | os.O_WRONLY,
                0o600), "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                # NOTE: Not encrypting for now because this is meant as a dev
                # setup. In production deployments, do make sure your CA key
                # is properly protected.....
                encryption_algorithm=serialization.NoEncryption(),
            ))

    @staticmethod
    def extcb_ca(cert):
        cert = cert.add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        )
        cert = cert.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        return cert

    def create_ca(self):
        os.mkdir(self.path)

        cn = "MBOX Certificate Authority"
        self.create_cert("ca", None, cn, cn, self.extcb_ca)
