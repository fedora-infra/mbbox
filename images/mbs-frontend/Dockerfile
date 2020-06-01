FROM fedora:31

RUN yum install -y module-build-service python3-psycopg2 httpd python3-mod_wsgi mod_ssl

COPY entrypoint.sh /entrypoint.sh 
COPY mbs.wsgi /mbs.wsgi
RUN chmod +x /entrypoint.sh

ENV USER=1001
EXPOSE 8443

ENTRYPOINT /entrypoint.sh
