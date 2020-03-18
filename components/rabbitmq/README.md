# RabbitMQ Certificates

## Generator

Generate CA, server and client certificates by running:

```sh
git clone https://github.com/michaelklishin/tls-gen tls-gen
cd tls-gen/basic
# private key password
make PASSWORD=mbox
make verify
make info
```

Certificate files will be created in `tls-gen/basic/result/`.

Copy the contents of CA, certificate and key (.key file) into the secret for both server and client configmaps.

RabbitMQ can now be deployed by running `kubectl apply -f .`

