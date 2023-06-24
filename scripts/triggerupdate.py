#!/usr/bin/env python3

import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL, DISABLED, REQUIRED
import sys

kerberos_auth = HTTPKerberosAuth(mutual_authentication=REQUIRED)
response = requests.get('http://srv-1.dcti.sut.ru/selfreg/resync',auth=kerberos_auth)
print(response)
