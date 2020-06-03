#!/bin/python3
import requests
import re
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requestFile = open('request','r')

req = []

for line in requestFile.readlines():
    line = line.strip()
    if line != "":
        req.append(line)

header = {}
for s in req[2:-1]:
    split = re.split('[:]',s)
    header[split[0]] = split[1].strip()

cookieParams = {}
if ('Cookie' in header):
    params = header['Cookie'].split(";")
    
    for p in params:
        split = re.split('=',p)
        cookieParams[split[0]] = split[1].strip()

    url = req[0].split()[1]
    response = requests.get(url, headers=header, verify=False)

    for key in cookieParams:
        if response.text.find(cookieParams[key]) > -1:
            print(key + " is reflected into the response")

else:
    print("There is not cookie in the supplied request")

