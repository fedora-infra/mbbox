FROM centos:8

RUN yum install -y epel-release
RUN yum install -y \
koji koji-hub koji-web koji-hub-plugins \
curl httpd mod_ssl postgresql fedora-messaging python3-mod_wsgi

RUN curl https://pagure.io/fedora-infra/ansible/raw/master/f/roles/koji_hub/templates/fedmsg-koji-plugin.py -o /usr/lib/koji-hub-plugins/fedmsg-koji-plugin.py
RUN rm -f /etc/kojiweb/web.conf && \
ln -s /etc/koji-hub/kojiweb.conf /etc/kojiweb/web.conf
RUN chown -R 1001:root /etc/koji-hub && \
chown -R 1001:root /etc/pki/tls
RUN mkdir -p /var/cache/kojihub && \
chown -R 1001:root /var/cache/kojihub

COPY readiness.sh /readiness.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh /readiness.sh && \
chown 1001:root /entrypoint.sh /readiness.sh

ENV USER=1001

EXPOSE 8443

ENTRYPOINT bash /entrypoint.sh

USER 1001
