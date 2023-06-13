#!/usr/bin/env python3
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

def get_machineid():
    machineid = ""
    with open('/etc/machine-id','r') as f:
        machineid = f.readline().strip()
    return machineid

uptime_seconds = 0
with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

hostname = os.uname()[1]
loggedusers = []
for i in subprocess.check_output('who').splitlines():
    user = i.split()[0]
    if not user in loggedusers:
        loggedusers.append(user.decode('utf-8'))
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

machineid = get_machineid()
data = { 'hostname': hostname, 'uptime': uptime_seconds, 'users' : loggedusers, 'cpu': cpu, 'machineid': machineid }
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

for i in ['eniac', 'report']:
    t = requests.post(f"http://{i}.dcti.sut.ru/online/api/data", data = json.dumps(data), headers=headers)

# upload scratch free space
temp = os.statvfs('/scratch')
data = { 'scratch_total': temp.f_frsize*temp.f_blocks, 'scratch_free': temp.f_frsize*temp.f_bavail }
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
for i in ['eniac', 'report']:
    t = requests.post(f"http://{i}.dcti.sut.ru/online/api/scratch", data = json.dumps(data), headers=headers)

# upload CMOS battery status
# Not done currently

# upload ansible status
t = subprocess.check_output('tail -n 3 /var/log/ansible-pull.log',shell=True).splitlines()
try:
    t = t[1].decode('utf-8')
    t = t.split(':')[1].split()
except:
    exit()
data = {}
for i in t:
    p=i.split('=')
    if len(p)>1:
        if p[0] == 'ok':
            data['ok']=int(p[1])
        elif p[0] == 'changed':
            data['change']=int(p[1])
        elif p[0] == 'unreachable':
            data['unreachable']=int(p[1])
        elif p[0] == 'failed':
            data['failed'] = int(p[1])

for i in ['eniac', 'report']:
    t = requests.post(f"http://{i}.dcti.sut.ru/online/api/ansible", data = json.dumps(data), headers=headers)
