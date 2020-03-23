#!/bin/bash

update-ca-trust
exec /usr/sbin/kojid --fg --force-lock --verbose
