#!/bin/bash
PASS=$(pwgen -A -0 -B -1 6)
kadmin -p automator/admin -k -t /etc/krb5.keytab << EOF
cpw -pw "${PASS}" "$2"
modprinc +needchange "$2"
EOF
echo -e "$2\t$PASS" >> "$3".txt
