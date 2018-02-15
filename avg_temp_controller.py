#!/usr/bin/python                                                                                                                                                                                             
#: Title        :avg_temp_controller
#: Date         :2015-10-10
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :runs avg_temp.py and links temp data of all rnd machines in SQL database

from datetime import datetime
import subprocess, MySQLdb
date = datetime.now().strftime('%Y-%m-%d')
time = datetime.now().strftime('%H:%M') + ':00'

db = MySQLdb.connect(host='###', user='###', passwd='###', db='###')
cur = db.cursor()

def get_id():
    cur.execute('SELECT ### FROM ### WHERE date = "%s" and time = "%s"' % (date, time))
    time_id = cur.fetchone()
    if time_id == None:
        cur.execute('INSERT INTO ###(date,time) VALUE("%s", "%s")' % (date, time))
        db.commit()
        cur.execute('SELECT ### FROM ### WHERE date = "%s" and time = "%s"' % (date, time))
        time_id = cur.fetchone()
        return time_id[0]
    else:
        return time_id[0]

time_id = get_id()

subprocess.Popen("sudo ### cmd.run 'python /###/avg_temp.py '" + str(time_id), shell=True).wait()
cur.close()
db.close()
