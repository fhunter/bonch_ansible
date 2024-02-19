#!/usr/bin/env python3
import subprocess
import json
import glob
import requests

def readhddtemp():
    temps = []
    drives = glob.glob("/dev/sd[a-z]")
    commandline = ["/usr/sbin/hddtemp", "-n", "-q" ]
    for i in drives:
        commandline.append(i)
    for i in subprocess.check_output(commandline).splitlines():
        temp = int(i.split()[0])
        if temp != 0:
            temps.append(i.decode('utf-8'))
    return temps

def readfilecontents(name):
    fname = open(name, "r")
    contents = fname.readline()
    contents = contents.replace("\n","")
    fname.close()
    return contents

def gethwmonnumber(path):
    if "/device/" in path:
        return int(path.replace("/sys/class/hwmon/hwmon","").replace("/device/name",""))
    else:
        return int(path.replace("/sys/class/hwmon/hwmon","").replace("/name",""))

def gethwmon():
    temp = {}
    names = glob.glob("/sys/class/hwmon/hwmon*/name")
    names2 = glob.glob("/sys/class/hwmon/hwmon*/device/name")
    names = names + names2
    for i in names:
        number = gethwmonnumber(i)
        temp[number]=readfilecontents(i)
    return temp

def sensormatch(name):
    if name == "coretemp":
        return True
    if name == "f71869a": #Lab 439
        return True
    if name == "atk0110": # for a44101
        return True
    if name == "it8720": # for a43904
        return True
    if name == "k10temp": # for termserver2
        return True
    return False

def gethwmon_values(number,name):
    inputs = glob.glob("/sys/class/hwmon/hwmon%s/temp*_input" % number)
    inputs2 = glob.glob("/sys/class/hwmon/hwmon%s/device/temp*_input" % number)
    inputs = inputs + inputs2
    temps = []
    for i in inputs:
        temp = int(readfilecontents(i))
        temp = temp/1000
        if (temp > 0) and (temp < 120 ):
            temps.append(temp)
    return temps

def readcputemp():
    temps = []
    dictionary = gethwmon()
    for i in dictionary:
        if sensormatch(dictionary[i]):
            for k in gethwmon_values(i,dictionary[i]):
                temps.append(k)
    return temps

data = {}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

data['hdd'] = readhddtemp()
data['cpu'] = readcputemp()

t = requests.post(
        "https://report.dcti.sut.ru/temperature/post",
        data = json.dumps(data),
        headers=headers, allow_redirects=True)
