#!/usr/bin/env python3

import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL, DISABLED, REQUIRED
import sys

if len(sys.argv) > 1:
	data = { 'username': sys.argv[1] }
	kerberos_auth = HTTPKerberosAuth(mutual_authentication=REQUIRED)
	response = requests.post('http://srv-1.dcti.sut.ru/selfreg/process/newuser',auth=kerberos_auth, json = data)
	print(response.text)
	print(response.json())
