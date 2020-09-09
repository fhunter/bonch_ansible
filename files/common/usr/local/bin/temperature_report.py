#!/usr/bin/env python
import requests
import os
import subprocess
import json
import glob

def readhddtemp():
    temps = []
    drives = glob.glob("/dev/sd[a-z]")
    commandline = ["hddtemp", "-n", "-q" ]
    for i in drives:
        commandline.append(i)
    for i in subprocess.check_output(commandline).splitlines():
        temp = int(i.split()[0])
        if temp != 0:
            temps.append(i)
    return temps

def readfilecontents(name):
    f = open(name, "r")
    contents = f.readline()
    contents = contents.replace("\n","")
    f.close()
    return contents

def gethwmon():
    temp = {}
    names = glob.glob("/sys/class/hwmon/hwmon*/name")
    for i in names:
        number = int(i.replace("/sys/class/hwmon/hwmon","").replace("/name",""))
        temp[number]=readfilecontents(i)
    return temp

def sensormatch(name):
    if name == "coretemp":
        return True
    return False

def gethwmon_values(number,name):
    inputs = glob.glob("/sys/class/hwmon/hwmon%s/temp*_input" % number)
    temps = []
    for i in inputs:
        temp = int(readfilecontents(i))
        temp = temp/1000.0
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


t = requests.post("http://eniac.dcti.sut.ru/temperature/post", data = json.dumps(data), headers=headers)
