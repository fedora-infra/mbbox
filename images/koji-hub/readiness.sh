#!/bin/bash

BODY='<?xml version="1.0" encoding="utf-8"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>'

res=$(curl \
-X POST \
-H 'Content-Type: text/xml' \
-d '$BODY' \
http://127.0.0.1:8080/kojihub/)

if [ "$?" != '0' ]
then
    exit 1
fi

if [ "$res" == '*<fault>*' ]
then
   echo $res
   exit 1
fi

echo $http_code

exit 0