#!/bin/python3

import socket
import re

f = open("/home/man715/WDE Testing/additional_hosts_from_maint_doc.lst","r")

ips = []
for host in f.readlines():
    h = host[:-1]
    try:
        print(h + ", " + socket.gethostbyname(h))
    except socket.gaierror:
        print("",end="")
f.close()


