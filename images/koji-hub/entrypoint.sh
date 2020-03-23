#!/bin/bash

if [ "${KOJI_HUB_CA_CERT_PATH}" == "" ]; then
  KOJI_HUB_CA_CERT_PATH="/etc/cacert/cert"
fi

ln -s ${KOJI_HUB_CA_CERT_PATH} /etc/pki/tls/certs/`openssl x509 -hash -noout -in ${KOJI_HUB_CA_CERT_PATH}`.0
update-ca-trust

if [ ! -f "/var/cache/kojihub/.dbschema" ]; then
  PGPASSWORD="${POSTGRES_PASSWORD}" psql \
  -h ${POSTGRES_HOST} \
  -U ${POSTGRES_USER} \
  -W ${POSTGRES_DB} < /usr/share/doc/koji/docs/schema.sql

  touch /var/cache/kojihub/.dbschema
fi

mkdir -p /httpdir/run/
ln -s /usr/lib64/httpd/modules /httpdir/modules
truncate --size=0 /httpdir/accesslog /httpdir/errorlog
tail -qf /httpdir/accesslog /httpdir/errorlog &
ulimit -c 0
mkdir -p /mnt/koji/{packages,repos,work,scratch,repos-dist}
exec httpd -f /etc/koji-hub/httpd.conf -DFOREGROUND -DNO_DETACH
