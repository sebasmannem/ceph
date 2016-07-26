#!/usr/bin/env python2
import subprocess
import ConfigParser
config = ConfigParser.ConfigParser()
try:
    config.readfp(open('/etc/keystone/keystone.conf'))
    print(config.get('DEFAULT', 'admin_token'))
except:
    openssl = subprocess.Popen(['openssl', 'rand', '-hex', '10'], stdout=subprocess.PIPE)
    admin_token = openssl.stdout.read()
    admin_token = admin_token.strip()
    try:
        config.add_section('DEFAULT')
    except:
        pass
    config.set('DEFAULT', 'admin_token', admin_token)
    config.write(open('/etc/keystone/keystone.conf', 'w+'))
    print(admin_token)
