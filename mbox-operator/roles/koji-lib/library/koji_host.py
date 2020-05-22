#!/usr/bin/env python

# This file is part of the mbbox project.
# Copyright (C) 2020  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

DOCUMENTATION = '''
---
module: koji_host

short_description: Ansible module that ensures a koji host state in a remote koji-hub instance.

description:
  - This module ensures that a koji host is added in koji
  - It requires a running koji-hub instance

options:
    host:
        description:
            - a qualified and unique koji hostname
        required: true
    arch:
        description:
            - a valid koji host archtecture
        default: x86
    server:
        description:
            - the full koji-hub server url
        required: true
    state:
        description:
            - the koji desired state
        default: present
        choices: present, absent
    ssl_auth:
        description:
            - a dictonary which contains the require ssl authentication info
    ssl_auth.cert:
      description:
        - the client pem file path to use, this file must contain both key and certificate in PEM format  
    ssl_auth.serverca:
      description:
        - the certificate authority PEM file path used by both koji-hub server and koji-builder client pem file
    ssl_auth.verify:
      description:
        - A boolean flag to tell koji-builder to validate the client pem file, should be set to false if using self-signed certificates.
      default: true

author:
    - Red Hat, Inc. and others
'''

EXAMPLES = '''
- koji_host:
  server: https://koji-hub:8443/kojihub
    host: koji-hub:8443
    arch: x86
    ssl_auth:
      cert: /tmp/admin.pem
      serverca:/tmp/ca.pem
      verify: false
'''

from optparse import Values

from ansible.module_utils.basic import AnsibleModule
import koji
from koji_cli.lib import activate_session


def build():
  """
  Builds an AnsibleModule object instance
  """
  spec = dict(
    host=dict(type='str', required=True),
    arch=dict(type='str', required=True),
    server=dict(type='str', required=True),
    state=dict(type='str', default='present', choices=['present', 'absent']),
    ssl_auth=dict(type='dict')
  )
  return AnsibleModule(
    argument_spec=spec,
    supports_check_mode=True
  )


def ssl_config(module):
  """
  Creates a ssl config dictionary to be used for ssl auth.
  """
  ctx = module.params['ssl_auth']
  try:
    return {
      'cert': ctx['cert'],
      'serverca': ctx['serverca'],
      'no_ssl_verify': ctx.get('verify', True),
      'authtype': 'ssl'
    }
  except KeyError as e:
   module.fail_json(changed=False,
      skipped=False, 
      failed=True, 
      error='Missing ssl_auth "%s" key.' % e.args[0])


def main():
  """
  Main funtion that runs the module. 
  """
  module = build()
  config = {'server': module.params['server']}

  if 'ssl_auth' in module.params:
    config.update(**ssl_config(module))
  else:
    module.fail_json(changed=False,
      skipped=False, 
      failed=True, 
      error='Missing authentication config')

  options = Values(config)
  session_opts = koji.grab_session_options(options)
  session = koji.ClientSession(options.server, session_opts)
  
  try:
    session.ssl_login(options.cert, None, options.serverca)
  except Exception as e:
    module.fail_json(changed=False,
      skipped=False,
      failed=True,
      error=str(e))
  host = session.getHost(module.params['host'])
  if host:
    module.exit_json(changed=False,
      skipped=True,
      failed=False)

  try:
    host = session.addHost(module.params['host'], module.params['arch'])
  except Exception as e:
     module.fail_json(changed=False,
      skipped=False,
      failed=True,
      error=str(e))

  module.exit_json(changed=True,
    skipped=False,
    failed=False, result=host)


if __name__ == '__main__':
  main()
