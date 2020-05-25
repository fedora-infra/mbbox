FROM fedora:latest

RUN yum install -y module-build-service python3-psycopg2 python3-fedmsg

RUN mkdir /etc/mbs-backend && \
chown -R 1001:root /etc/mbs-backend

COPY entrypoint.sh /entrypoint.sh
COPY mbs-scheduler.py /etc/mbs-backend/mbs-scheduler.py

ENV USER=1001

ENTRYPOINT /entrypoint.sh
