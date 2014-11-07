#!/usr/bin/env python

import cgi,sys,os
import cgitb
import uuid
import time
import json

cgitb.enable()

try:
	remoteUser = os.environ['REMOTE_USER']
except KeyError:
	remoteUser = 'cgregg'

userFullName=os.popen('ldapsearch -x "(uid='+remoteUser+')" | grep gecos | cut -d" " -f2-').read()

sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\n")
sys.stdout.write("\n")
sys.stdout.write(userFullName)

