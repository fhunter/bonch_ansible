#!/bin/bash
LOCALDIR=$(dirname "$(readlink -f "$0")")
PASS=$(${LOCALDIR}/gpw.py)
#PASS=$(pwgen -A -0 -B -1 6)
kadmin -p automator/admin -k -t /etc/krb5.keytab << EOF
addprinc -policy "$1" -pw "${PASS}" "$2"
modprinc +needchange "$2"
EOF
echo "$2" "$PASS" >> "$3"
