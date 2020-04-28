#!/bin/bash
set -xe

mkdir /httpdir/run || rm -rf /httpdir/run/*
ln -s /etc/httpd/modules /httpdir/modules
truncate --size=0 /httpdir/accesslog /httpdir/errorlog
ulimit -c 0

exec httpd -f /etc/ipsilon-cfg/httpd/httpd.conf -DFOREGROUND -DNO_DETACH