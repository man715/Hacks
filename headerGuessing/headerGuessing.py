#!/bin/python3
import requests
import random
import os
import socket
import urllib3
import sys
import re
from time import sleep
from datetime import datetime

# Disables the warning when requesting HTTPS. This allows you to run 
# this tool through a proxy without it breaking
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

args = sys.argv[1:]
i = 0 
delay = 0
request_file = 'request'
results_file = ''
while i < len(args):
    if args[i] == '-d' or args[i] == '--delay':
        delay = int(args[i+1])
        i += 1
    elif args[i] == '-f' or args[i] == '--file':
        request_file = args[i+1]
    elif args[i] == '-o' or args[i] == '--output':
        output_file = args[i+1]

    i += 1


req = []
file =  open(request_file,'r')
for line in file.readlines():
    line = line.strip()
    if line != '':
        req.append(line)
file.close()

# Get the path from the first line and second item in the list.
path = req[0].split()[1]

# Create alist of headers from everything but the first line
headers_list = req[1:]

# Convert the header list into a header dict that requests expects
headers = {}
for word in headers_list:
    split = re.split('[:]',word,1)
    # Stip any whitespace from the beginning and end of the line
    headers[split[0]] = split[1].strip()

# Get the original response to compare against
original_response = requests.get(path, headers=headers, verify=False,
                                allow_redirects=False)

# List of the test headers
file = open('headers.lst','r')

if len(results_file) == 0:
    results_file = headers['Host'] + datetime.now().strftime(
                                    '%y-%m-%d-%H-%M-%S')

# Remove testing header if it is already in the request
test_header_list = []
for test in file.readlines():
    test_header_list.append(test.lower().rstrip())

test_header_list = list(dict.fromkeys(test_header_list))

for key in headers:
    for test in test_header_list:
        if key.lower() == test:
            test_header_list.remove(test)
            print(test)

for test_header in test_header_list:
    retry = 0
    # Remove the newline character
    test_header = test_header.rstrip()
    # The value of the headers and the value we will be looking for 
    # in the response
    test_value = '/alkdsfj/en' 

    safety = random.randrange(1,1000000000)
    # Build the url
    url = path + '?safe=' + str(safety)
    print(url)    
    # Add the test header to the other headers
    h = headers
    h[test_header] = test_value

    #Send the request
    try:
        response = requests.get(url, headers=h,verify=False,
                               allow_redirects=False) 

        if response.status_code == 404:
            while retry < 3:
                sleep(delay) 
                response = requests.get(url, headers=h,verify=False, 
                                        allow_redirects=False)
                retry += 1
        h.pop(test_header)

        # See if the test_value is anywhere in the request
        if len(response.text) != len(original_response.text):
            # Test to see if the header value is reflected 
            # in the response
            if response.text.find(test_value) > -1:
                results = open(results_file, 'a')
                print('\n' + test_header + ' is reflected back into the body')
                results.write('URL: ' + url + '\nStatus Code: ' 
                              + str(response.status_code) + '\n'+ 'Header: ' 
                              + test_header + '\n' + 'Note: This header is reflected in the response body.')
                results.write('\n-------------------------\n')
                file.close()
            else:
                print('\n' + test_header + ' may be of interest')
                results = open(results_file, 'a')
                results.write('URL: ' + url + '\nStatus Code: ' 
                              + str(response.status_code) + '\n'+ 'Header: ' 
                              + test_header + '\n')
                if response.status_code == 302:
                    print('This header caused a redirect\n')
                    results.write('Note: This header caused a redirect\n')
                    results.write('\n-------------------------\n')
                    file.close()
                else:
                    results.write('\n-------------------------\n')
                    file.close()
    # ToDo: create a more robust error handler
    except (ValueError,socket.gaierror,urllib3.exceptions.NewConnectionError,
            urllib3.exceptions.MaxRetryError,
            requests.exceptions.ConnectionError):
        print(test_header)
        print(sys.exc_info()[1])
    
file.close()
