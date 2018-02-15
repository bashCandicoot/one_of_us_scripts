#!/usr/bin/python                                                                                                                                                     
#: Title        :wbinfo
#: Date         :2015-08-03
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :runs wbinfo -u/-i on all users
import subprocess, sys

users = subprocess.Popen(['wbinfo -u'], stdout = subprocess.PIPE, shell=True).communicate()[0].split('\n')
output = []; invalid_users = 0

for user in users:
    stdout, stderr = subprocess.Popen(['wbinfo -i ' + user], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    try:    
        if stderr[53] == 'C':
            stderr = stderr[52:]
            print stderr[1:-1]
            invalid_users +=1
    except:
        pass
    if stdout != '':    
        output.append(stdout[:-1])

print ''
for element in output:
    print element

print '\nTotal Users:', len(output) + invalid_users, '\nInvalid users:', invalid_users, '\nValid users:', len(output)
sys.exit(0)
