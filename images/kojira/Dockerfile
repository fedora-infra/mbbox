FROM centos:7

RUN yum install -y koji-utils

COPY entrypoint.sh /entrypoint.sh

ENV USER=1001

ENTRYPOINT /entrypoint.sh
