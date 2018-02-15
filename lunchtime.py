#!/usr/bin/python                                                                                                                             
#: Title        :lunctime
#: Date         :2016-02-02
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :puts machine on the farm for specified duration

import sys
import time
import ascii_art
import socket
import subprocess
import os
import MySQLdb
from datetime import datetime

"""
example usage:

    Typing 1hr will put your machine on the farm for 1 hour
    10m will put your machine on the farm for 10 minutes
    1h10m will put your machine on the farm for 1 hour and 10 minutes
    Ctrl-c will take your machine off the farm early
"""


print "\x1b[8;20;95t"
user = subprocess.Popen('printf $USER', stdout=subprocess.PIPE, shell=True).communicate()[0]
date = datetime.now().strftime('%Y-%m-%d')
time_now = datetime.now().strftime('%H:%M:%S')

ascii_art.lunchtime(2)
answer = False
while answer != True:
	lb = raw_input('\n1h = 1 hour || 10m = 10 minutes || Examples: 15m || 2h || 1h30m\n\nEnter duration: ')
	try:
		if 'm' in lb and 'h' in lb:
			mins = int(lb[lb.index('h')+1:lb.index('m')])
			hours = int(lb[:lb.index('h')])
			seconds = (mins*60) + (hours*60*60)
			answer = True
		elif 'h' in lb:
			hours = int(lb[:lb.index('h')])
			seconds = hours*60*60
			answer = True
		elif 'm' in lb:
			mins = int(lb[:lb.index('m')])
			seconds = mins*60
			answer = True
		else:
			print 'Dafuq?'
	except:
		print 'Dafuq?'

lock_host = '/usr/local/pfx/qube/bin/qblock --purge %s' % (socket.gethostname())
unlock_host = '/usr/local/pfx/qube/bin/qbunlock %s' % (socket.gethostname())
out = subprocess.Popen(unlock_host, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]
if 'nothing' in out:
	sys.exit('Sorry, your machine is unable to go on the farm')

try:
    db = MySQLdb.connect(host='###', user='###', passwd='###', db='###')
    cur = db.cursor()
    insert = "INSERT INTO `usage`(`username`, `duration`, `date`, `time`) VALUES ('%s','%s','%s','%s');" % (user, lb, date, time_now)
    cur.execute(insert)	
except:
    pass

print '\nYour machine is on the farm!...'
print '\nPress Ctrl+c to cancel early' 
try:
	while seconds != 0:
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		sys.stdout.write("\r%d:%02d:%02d" % (h, m, s))
		sys.stdout.flush()
		time.sleep(1)
		seconds -=1
except KeyboardInterrupt:
	subprocess.Popen(lock_host, stdout=subprocess.PIPE, shell=True).wait()
	sys.exit('\nUser cancelled\nMachine not on the farm!')
out = subprocess.Popen(lock_host, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0]
print '\nMachine not on the farm!'

cur.close()
db.close()
