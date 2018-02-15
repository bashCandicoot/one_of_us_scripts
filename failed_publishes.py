#!/usr/bin/python     
#: Title        :failed_publishes
#: Date         :2015-03-20
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :emails users any failed publishes in the last 15mins
#                + a random fail gif


import sys
sys.path.append('/###/###/###/')

import os
import subprocess
import smtplib
import MySQLdb
import oou_io
from sys import argv
from collections import OrderedDict
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from random import randint

db = MySQLdb.connect(host='olivier', user='root', passwd='', db='pfx_dw')
cur = db.cursor()

# gets failed publish jobs in the last 15mins
cur.execute("""select ###, ###, ###, ###, FROM_UNIXTIME(job_timesubmit) 
            From ###, ###, ### WHERE (###.##=###.###) AND 
            (###.###=###.###) AND ###='failed' AND 
            ###.### LIKE '###%' AND ### > (UNIX_TIMESTAMP() - 900);"""
            )

data = cur.fetchall()

failed_publishes = ''
gif_dir_path = '/###/###/failed_publishes_gifs/'
list_of_gifs = os.listdir(gif_dir_path)
gif_path = gif_dir_path + list_of_gifs[(randint(1,58))]

users = ['###', '###', '###', '###']

for failed_publish in data:
    failed_publishes += 'Id: ' + str(failed_publish[0]) + \
                        '\tUsername: ' + failed_publish[1] + \
                        '\t\tRender: ' + failed_publish[2] + \
                        '\t\tTime: ' + str(failed_publish[4])[-8:] + '\n'

if (failed_publishes == ''):
    cur.close()
    db.close()

else:
    oou_io.send_email(list_of_recipients = users,
                      subject = 'Failed Publishes',
                      message = 'These publishes failed ' \
                                'within the last 15 mins:\n\n' \
                                + failed_publishes,
                      image = gif_path)
    cur.close()
    db.close()
