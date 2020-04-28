FROM fedora:31

ENV PSQL_USER=mbox \
PSQL_PASS=mbox \
PSQL_HOST=postgre \
PSQL_DB=mbox-identity

RUN dnf install -y ipsilon ipsilon-openidc python2-psycopg2 curl httpd mod_ssl python3-mod_wsgi 

COPY start.sh /etc/ipsilon-cfg/start.sh
RUN chmod +x /etc/ipsilon-cfg/start.sh && \
chown -R 1001:root /etc/ipsilon-cfg
RUN printf "def fix_user_dirs(*args, **kwargs):\n    pass\n" >>/usr/lib/python3.7/site-packages/ipsilon/tools/files.py

COPY cfgprofile /etc/ipsilon-cfg/cfgprofile
RUN mkdir /etc/ipsilon/{httpd,ipsilon,data} && \
LOGFILE=/dev/stdout ipsilon-server-install --config-profile=/etc/ipsilon-cfg/cfgprofile

EXPOSE 8443

ENTRYPOINT /etc/ipsilon-cfg/start.sh