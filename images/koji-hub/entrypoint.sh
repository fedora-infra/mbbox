#!/bin/bash

#cp cacert/cert /etc/pki/ca-trust/source/anchors/mbox_ca.pem

update-ca-trust

mkdir -p /httpdir/run/
ln -s /usr/lib64/httpd/modules /httpdir/modules
truncate --size=0 /httpdir/accesslog /httpdir/errorlog
tail -qf /httpdir/accesslog /httpdir/errorlog &
ulimit -c 0
mkdir -p /mnt/koji/{packages,repos,work,scratch,repos-dist}
exec httpd -f /etc/koji-hub/httpd.conf -DFOREGROUND -DNO_DETACH