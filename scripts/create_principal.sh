#!/bin/bash
PASS=$(pwgen -c -n -B -1 8)
kadmin -p automator/admin -k -t /etc/krb5.keytab << EOF
addprinc -policy "$1" -pw "${PASS}" "$2"
modprinc +needchange "$2"
EOF
echo "$2" "$PASS" >> "$3"
