#!/usr/bin/bash

update-ca-trust
mkdir -p /httpdir/run
ln -s /usr/lib64/httpd/modules /httpdir/modules
truncate --size=0 /httpdir/accesslog /httpdir/errorlog
tail -qf /httpdir/accesslog /httpdir/errorlog &
ulimit -c 0
exec httpd -f /etc/mbs-frontend/httpd.conf -DFOREGROUND -DNO_DETACH
