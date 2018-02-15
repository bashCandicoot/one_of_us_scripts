#!/usr/bin/python     
#: Title        :avg_temp
#: Date         :2016-03-21
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :generates avg temp of all cpu cores

import subprocess, MySQLdb
from sys import argv
from datetime import datetime

script_name, time_id = argv

db = MySQLdb.connect(host='###', user='###', passwd='###', db='###')
cur = db.cursor()

def avg_core_temp(cores):
    total_temp = 0.0
    num_of_cores = 0
    for core in cores:
        num_of_cores +=1
        total_temp += float(core)
    return total_temp/num_of_cores

temps = subprocess.Popen(['sudo sensors'], stdout=subprocess.PIPE, shell=True).communicate()[0]
cores = []

for char in range (len(temps)):
    if temps[char] == '+':
        if temps[char-2] == ' ':
            cores.append(temps[char+1] + temps[char+2] + temps[char+3] + temps[char+4])

host_name = subprocess.Popen(['hostname'], stdout=subprocess.PIPE).communicate()[0][:6]
host_temp = avg_core_temp(cores)
cur.execute('SELECT ### FROM ### WHERE ### = ("%s")' % (host_name))
machine_id = cur.fetchone()
if machine_id is None:
    fullName = host_name + '###'
    cur.execute("INSERT INTO ###(###,###) VALUES(%s,%s)",(fullName,host_name))
    db.commit()
else:
    machine_id = machine_id[0]
    cur.execute('INSERT INTO ### VALUES ("%s", "%s", "%s")' % (machine_id, time_id, str(round(host_temp, 2))))
    db.commit()

cur.close()
db.close()  
