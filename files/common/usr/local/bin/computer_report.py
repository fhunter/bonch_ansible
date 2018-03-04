#!/usr/bin/env python
import requests
import os
import psutil
import subprocess
import json
import dbus
import pwd

def cksessions():
    users = []
    try:
        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object('org.freedesktop.ConsoleKit','/org/freedesktop/ConsoleKit/Manager')
        sessions=proxy.GetSessions(dbus_interface='org.freedesktop.ConsoleKit.Manager')
        for session in sessions:
            proxy1=system_bus.get_object('org.freedesktop.ConsoleKit', str(session))
	    userid=proxy1.GetUnixUser(dbus_interface='org.freedesktop.ConsoleKit.Session')
	    if userid >= 1000:
	        username=pwd.getpwuid(userid).pw_name
	        users.append(username)
    finally:
        return users



uptime_seconds = 0
with open('/proc/uptime', 'r') as f:
	uptime_seconds = float(f.readline().split()[0])

hostname = os.uname()[1]
loggedusers = []
for i in subprocess.check_output('who').splitlines():
    user = i.split()[0]
    if not user in loggedusers:
	loggedusers.append(user)
for j in cksessions():
    if not j in loggedusers:
	loggedusers.append(j)


loadavg = 0
with open('/proc/loadavg', 'r') as f:
    loadavg = float(f.readline().split()[1])

loadbycpu = psutil.cpu_percent(2.0,True) #over 2 seconds. all cores
cores = 0
load = 0
for i in loadbycpu:
    load+=i
    cores+=1

cpu = {'cores': cores, 'load': load, 'loadavg': loadavg } #load - immediate, in percents. cores - number of processors. loadavg - 5 minute average load

data = { 'hostname': hostname, 'uptime': uptime_seconds, 'users' : loggedusers, 'cpu': cpu }
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

t = requests.post("http://eniac.dcti.sut.ru/online/api/data", data = json.dumps(data), headers=headers)
