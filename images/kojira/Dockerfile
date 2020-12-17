FROM centos:8

RUN yum install -y epel-release
RUN yum install -y koji-utils

COPY entrypoint.sh /entrypoint.sh

ENV USER=1001

ENTRYPOINT /entrypoint.sh
