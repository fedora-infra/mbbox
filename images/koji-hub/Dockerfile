FROM fedora:31

RUN dnf install --setopt tsflags= -y \
koji koji-hub koji-web koji-hub-plugins \
curl httpd mod_ssl postgresql fedora-messaging python3-mod_wsgi 

RUN curl https://infrastructure.fedoraproject.org/cgit/ansible.git/plain/roles/koji_hub/templates/fedmsg-koji-plugin.py -o /usr/lib/koji-hub-plugins/fedmsg-koji-plugin.py
RUN rm -f /etc/kojiweb/web.conf && \
ln -s /etc/koji-hub/kojiweb.conf /etc/kojiweb/web.conf
RUN chown -R 1001:root /etc/koji-hub

COPY readiness.sh /readiness.sh
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh /readiness.sh && \
chown 1001:root /entrypoint.sh /readiness.sh

ENV USER=1001

EXPOSE 8443

ENTRYPOINT bash /entrypoint.sh

USER 1001
