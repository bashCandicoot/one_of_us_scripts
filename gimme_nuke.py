#!/usr/bin/python     
#: Title        :gimme_nuke
#: Date         :2015-11-01
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :emails current nuke users asking them to free up a license

import os, subprocess, smtplib, sys, MySQLdb
from datetime import datetime
from sys import argv
from collections import OrderedDict
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
date = datetime.now().strftime('%Y-%m-%d')
time = datetime.now().strftime('%H:%M:%S')

if len(argv) == 2:
    print 'No license type argument\nOptions are: nuke_i, nukex_i, nukestudio_i\nOr no username specified'
    sys.exit(1)
else:
    script_name, user_name, nuke_license_type = argv

read_file = '/###/###/nukelice.txt'
#print '\nReading license file from %s' % read_file

try:
    with open(read_file) as f:
        output = f.readlines()
except:
    print 'License file not found.\nPlease email steve@weacceptyou.com and complain.'
    sys.exit(2)
        
del output[0:81]

nuke_i_users = []; nuke_x_users = []; nuke_studio_users = []
for line in output:
    line = ''.join(line.split())
    if line[0:6] == 'nuke_i':
        chunk = line[17:]
        user = chunk[:chunk.index('@')]
        nuke_i_users.append(user)       
    if line[0:7] == 'nukex_i':
        chunk = line[18:]
        user = chunk[:chunk.index('@')]
        nuke_x_users.append(user)
    if line[0:12] == 'nukestudio_i':
        chunk = line[23:]
        user = chunk[:chunk.index('@')]
        nuke_studio_users.append(user)

licenses = OrderedDict()
licenses = {'nukestudio_i':set(nuke_studio_users), 'nukex_i':set(nuke_x_users), 'nuke_i':set(nuke_i_users)}
users = []

for key, value in licenses.iteritems():
    if key == nuke_license_type:
        if len(value) == 0:
            print '\nAll licenses available for %s' % key
            if nuke_license_type == 'nukestudio_i':
                nuke_license_type = 'nukex_i'
            elif nuke_license_type == 'nukex_i':
                nuke_license_type = 'nuke_i'

        else:
            print '\nLicense email requests sent to %s users:' % nuke_license_type
            for user in value:
                print '&nbsp;&nbsp;' + user
                users.append(user + '@weacceptyou.com')

msg = MIMEMultipart()
msg['From'] = '%s@weacceptyou.com' % user_name
msg['To'] = ", ".join(users)
msg['Subject'] = 'Spare Nuke license request'
body = 'Hey,\nCan any of you free up a %s license?\nThanks!' % key
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('###')
server.sendmail(msg['From'], users, msg.as_string())
server.quit()

try:
    db = MySQLdb.connect(host='###', user='###', passwd='###', db='###')
    cur = db.cursor()
    cur.execute('INSERT INTO button_pressed VALUE(" ", "%s", "%s", "%s", "%s")' % (user_name, nuke_license_type, date, time))
    cur.close()
    db.close()
except:
    sys.exit()
