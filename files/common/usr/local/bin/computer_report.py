#!/usr/bin/env python3
import os
import subprocess
import json
import pwd
import dbus
import psutil
import requests

def cksessions():
    users = []
    try:
        system_bus = dbus.SystemBus()
        proxy = system_bus.get_object(
            'org.freedesktop.ConsoleKit',
            '/org/freedesktop/ConsoleKit/Manager')
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
    with open('/etc/machine-id','r') as datafile:
        machineid = datafile.readline().strip()
    return machineid

def getuptime():
    uptime_seconds = 0
    with open('/proc/uptime', 'r') as datafile:
        uptime_seconds = float(datafile.readline().split()[0])
    return uptime_seconds

def getloadavg():
    loadavg = 0
    with open('/proc/loadavg', 'r') as datafile:
        loadavg = float(datafile.readline().split()[1])
    return loadavg

def getcoresnload():
    loadbycpu = psutil.cpu_percent(2.0,True) #over 2 seconds. all cores
    cores = 0
    load = 0
    for i in loadbycpu:
        load+=i
        cores+=1
    return (cores, load)

def getloggedusers():
    loggedusers = []
    for i in subprocess.check_output('who').splitlines():
        user = i.split()[0]
        if not user in loggedusers:
            loggedusers.append(user.decode('utf-8'))
    for i in cksessions():
        if not i in loggedusers:
            loggedusers.append(i)
    return loggedusers

def getscratchsize():
    temp = os.statvfs('/scratch')
    total = temp.f_frsize*temp.f_blocks
    free = temp.f_frsize*temp.f_bavail
    return (total, free)

def getansibleline():
    temp = subprocess.check_output('tail -n 3 /var/log/ansible-pull.log',shell=True).splitlines()
    line = ""
    for i in enumerate(temp):
        if "PLAY RECAP" in i[1].decode('utf-8'):
            if i[0] < (len(temp)-1):
                line = temp[i[0]+1].decode('utf-8')
    return line

def post_data(data_list):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
        }
    session = requests.Session()
    # list of tuples - url, data
    for i in data_list:
        session.post(i[0], data = json.dumps(i[1]), headers=headers,allow_redirects=True)


def main():
    # list of tuples - url, data
    data_to_send = []

    # load - immediate, in percents.
    # cores - number of processors.
    # loadavg - 5 minute average load
    cores, load = getcoresnload()
    cpu = {
        'cores': cores,
        'load': load,
        'loadavg': getloadavg()
        }

    data = {
        'hostname': os.uname()[1],
        'uptime': getuptime(),
        'users' : getloggedusers(),
        'cpu': cpu,
        'machineid': get_machineid()
        }
    data_to_send.append(("https://report.dcti.sut.ru/online/api/data", data))

    # upload scratch free space
    temp = getscratchsize()
    data = {
        'scratch_total': temp[0],
        'scratch_free': temp[1]
        }
    data_to_send.append(("https://report.dcti.sut.ru/online/api/scratch", data))

    # upload ansible status
    line = getansibleline()
    try:
        line = line.split('|')[-1:][0]
        line = line.split(':')[1].split()
    except IndexError:
        line=[]
    data = {}
    for i in line:
        parts=i.split('=')
        if len(parts)>1:
            for key in ['ok','changed','unreachable', 'failed']:
                if parts[0] == key:
                    data[key]=int(parts[1])
    data_to_send.append(("https://report.dcti.sut.ru/online/api/ansible", data))
    post_data(data_to_send)

    return 0



if __name__ == "__main__":
    main()
