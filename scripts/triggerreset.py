#!/usr/bin/env python

import requests
from requests_kerberos import HTTPKerberosAuth
import sys

if len(sys.argv) > 1:
	data = { 'username': sys.argv[1] }
	response = requests.post('http://eniac.dcti.sut.ru/selfreg/process/newuser',auth=HTTPKerberosAuth(), json = data)
