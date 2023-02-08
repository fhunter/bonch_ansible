#!/bin/bash
HOST=$(hostname|awk -F. '{print $1}')
PRINCIPAL="automator"
case "$HOST" in
    "srv-1") PRINCIPAL="automator1" ;;
    "srv-2") PRINCIPAL="automator2" ;;
esac
kadmin -p ${PRINCIPAL}/admin -k -t /etc/krb5.keytab << EOF
delprinc "$2"
EOF
