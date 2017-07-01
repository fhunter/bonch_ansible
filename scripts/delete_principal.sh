#!/bin/bash
kadmin -p automator/admin -k -t /etc/krb5.keytab << EOF
delprinc "$2"
EOF
