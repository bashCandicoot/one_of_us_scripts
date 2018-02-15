#!/usr/bin/python     
#: Title        :disk_space
#: Date         :2015-11-19
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :stores output of du and df in text files 

import os, sys, subprocess
from datetime import datetime
date = datetime.now().strftime('%Y-%m-%d')
time = datetime.now().strftime('%H:%M:') + '00'
dir_path = '/###/###/###/'
write_file = open('/###/###/###/' + date + '/' + date + time + '.txt', 'w')

dirs_list = []; sub_dirs_list = []

for dirr in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, dirr)):
        print "dir=", os.path.join(dir_path, dirr)
        dirs_list.append(os.path.join(dir_path, dirr))

for dirr in dirs_list:
    for sub_dir in os.listdir(dirr):
        if os.path.isdir(os.path.join(dirr, sub_dir)):
            print 'sub_dir=', os.path.join(dirr, sub_dir)
            sub_dirs_list.append(os.path.join(dirr, sub_dir))

df = subprocess.Popen(['df -Ph | grep /###'], stdout = subprocess.PIPE, shell=True).communicate()[0][34:-7]
disk_size = ''; j = 0
while j < len(df):
    if df[j] != ' ':
        disk_size += df[j]
    else:
        if disk_size[-1] != ';':
            disk_size += ';'
        else:
            pass    
    j += 1

write_file.write(disk_size + '\n' + date + ';' + time)
dirs_list += sub_dirs_list

for dirr in dirs_list:
    size_location = subprocess.Popen(['du -sb ' + dirr], stdout=subprocess.PIPE, shell=True).communicate()[0]
    print size_location
    i = 0 
    while i < len(size_location):
        if size_location[i] == '\t': 
            size = size_location[:i] + ';'
            location = size_location[i:]        
            if size != '0;':
                output = size + location        
        i += 1
    output = ''.join(output.split())
    write_file.write('\n' + output)

write_file.close()
sys.exit(0)
