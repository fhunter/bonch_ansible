#!/usr/bin/env python
import requests
import os
import psutil
import subprocess
import json

uptime_seconds = 0
with open('/proc/uptime', 'r') as f:
	uptime_seconds = float(f.readline().split()[0])

hostname = os.uname()[1]
loggedusers = []
for i in subprocess.check_output('who').splitlines():
    user = i.split()[0]
    if not user in loggedusers:
	loggedusers.append(user)

networkspeed = 0

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

disks = psutil.disk_partitions()
diskspace = [] #total, free, volume
for i in disks:
    temp = {}
    mountpoint = i.mountpoint
    usage = psutil.disk_usage(mountpoint)
    temp['total']=usage.total
    temp['free']=usage.free
    temp['volume']=mountpoint
    diskspace.append(temp)

data = { 'hostname': hostname, 'uptime': uptime_seconds, 'users' : loggedusers, 'netspeed': networkspeed, 'cpu': cpu, 'disks': diskspace }
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

t = requests.post("http://eniac.dcti.sut.ru/online/api/data", data = json.dumps(data), headers=headers)
