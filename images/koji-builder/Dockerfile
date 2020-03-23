FROM centos:8

RUN yum install -y epel-release && \
yum install -y koji-builder

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
chown 1001:root /entrypoint.sh

ENV USER=1001

ENTRYPOINT bash /entrypoint.sh

USER 1001