#!/bin/bash
kadmin -p automator/admin -k -t /etc/krb5.keytab << EOF
addprinc -policy "$1" -pw "__$2" "$2"
modprinc +needchange "$2"
EOF
