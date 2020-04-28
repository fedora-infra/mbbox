# Identity Deployment

An identity kubernetes deployment for development purposes.

It requires two secrets in order to work:

HTTPD CA cert secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: service-ca
  labels:
    app: identity
data:
  cert: fillme
```

HTTPD certificate and key:

```
apiVersion: v1
kind: Secret
metadata:
  name: service-cert
  labels:
    app: identity
data:
  tls.crt: fillme
  tls.key: fillme
---
```