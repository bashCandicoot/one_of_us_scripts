#!/usr/bin/python     
#: Title        :nuke_license_count
#: Date         :2015-12-02
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :stores total/avail licenses for nuke/mari

read_file = '/###/nukelice.txt'
print 'Reading license file from %s' % read_file
open_file = open(read_file)
output = open_file.readlines()[45:63]

write_file = '/###/nuke_license_count.txt'
print 'Written the following to %s' % write_file
f = open(write_file,'w')
for line in output:
    line = ''.join(line.split())
    if line[0:4] == 'nuke' or line[0:4] == 'mari':
        license_name = line[:line.index('_')]
        if line[0:6] == 'nuke_i' or line[0:6] == 'nuke_r':
            license_name = line[0:6]    
    if line[0:5] == 'count':
        total = line[6:line.index(',')]
        chunk = line[-19:]
        in_use = chunk[chunk.index(':'):chunk.index(',')]
        available = int(total) - int(in_use[-1:])
        f.write(license_name + ':' + total + ':' + str(available) + ':\n')
        print license_name + ':' + total + ':' + str(available) + ':'
f.close()       
