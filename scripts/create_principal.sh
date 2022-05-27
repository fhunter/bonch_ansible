#!/bin/bash
kadmin -p automator/admin -k -t /etc/krb5.keytab << EOF
addprinc -policy "$1" -randkey "$2"
EOF
