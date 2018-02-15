#!/usr/bin/python 
#: Title        :oou_io
#: Date         :2016-04-14
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :classes & functions related to input/output tasks

import os
import subprocess
import sys
import time
import datetime
import smtplib
import re
import ascii_art
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from shotgun_api3 import Shotgun

def get_linux_username():
   return subprocess.Popen('printf $USER',
                           stdout=subprocess.PIPE,
                           shell=True).communicate()[0]

def get_all_job_names():
    return {0: 'mph', 1: 'crown', 2: 'boswell', 3: 'vot',
            4: 'checkmate', 5: 'spacebear', 6: 'ka',
            7: 'lv', 8: 'cfw'}

def append_cwd_to_directory_path(directory):
    if os.path.exists(directory):
        return os.getcwd() + '/' + directory
    else:
        sys.exit('Invalid path.\nAborting.')

def set_job_num_name(all_job_names, *args):
    for string in args:
        for num, job in all_job_names.iteritems():
            if job in string:
                if len(args) == 1:
                    return num, job
                else:
                    return num, job, string
    print 'No matching job in string' \
          '\nAborting.' 
    sys.exit()

def list_job_contents_of_io_machine_ingest_directory(job_name):
    ls = subprocess.Popen("ssh ### \
                          'ls /###/'" + 
                          job_name + "'/in'", 
                          stdout=subprocess.PIPE, 
                          shell=True).communicate()[0]
    if not len(ls):
        print '\nThere are no files for that job on the io machine.\n'
        ascii_art.fuck_up()
        sys.exit()
    else:
        return ls.split('\n')[:-1] 

def send_email(**kwargs):
    list_of_recipients = kwargs['list_of_recipients']
    subject = kwargs['subject']
    message = kwargs['message']
    if 'image' in kwargs:
        image = kwargs['image']
    else:
        image = ''

    msg = MIMEMultipart()
    msg['From'] = 'mail@weacceptyou.com'
    if len(list_of_recipients) == 1:
        msg['To'] = list_of_recipients[0] + '@weacceptyou.com'
    else:
        msg['To'] = '@weacceptyou.com, '.join(list_of_recipients) + '@weacceptyou.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if image:
        img_data = open(image, 'rb').read()
        formatted_image = MIMEImage(img_data, name=os.path.basename(image))
        msg.attach(formatted_image)

    server = smtplib.SMTP('###')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

class ShotgunDelivery(object):
    def __init__(self, **kwargs):
        self.contents_folder = kwargs['contents_folder']
        self.linux_username = kwargs['linux_username']
        self.job_num = kwargs['job_num']
        self.job_name = kwargs['job_name']
        self.locate_user_shotgun_id = kwargs['locate_user_shotgun_id']
        self.in_or_out = kwargs['in_or_out']
        
        if self.in_or_out == 'in':
            self.ingested_files = kwargs['ingested_files']

        proxy = '###'
        server_path = '###'
        convert_datetimes_to_utc = False
        
        self.sg = Shotgun(server_path,
                          kwargs['script_name'],
                          kwargs['script_key'],
                          convert_datetimes_to_utc, 
                          proxy)
        
        self.contents = ''
        self.title = ''

    def create_shotgun_delivery(self):
        if self.locate_user_shotgun_id:
            self.find_user_shotgun_id()
        else:
            self.known_user_shotgun_id()
        self.set_users_shotgun_id()
        self.generate_all_jobs_shotgun_details()
        self.generate_contents_and_title_fields()
        self.populate_delivery_fields()
        self.build_shotgun_delivery()
        self.link_shotgun_delivery()

    def find_user_shotgun_id(self):
        newbee = '\nHmm, you must be new here.' \
                 '\nGo to the shotgun website.' \
                 '\nClick on the search bar in the top right.' \
                 '\nSearch for your name.' \
                 '\nClick on person info.' \
                 '\nSee the 2 or 3 digit Id number?' \
                 '\nEnter that here* '
        for letter in newbee:
            if letter != '*':
                sys.stdout.write(letter)
                sys.stdout.flush()
                time.sleep(0.05)
            else:
                sys.stdout.write(': ')
                sys.stdout.flush()
                self.shotgun_user_id = raw_input()
                while len(shotgun_user_id) != 2 and len(shotgun_user_id) != 3:
                    self.shotgun_user_id = raw_input('\nThat\'s not a valid Id ' \
                                                     'number.\nIt is a 2 or 3 digit number ' \
                                                     'probably 3 in your case.\nId: ')
        time.sleep(1)

    def known_user_shotgun_id(self):
        shotgun_user_ids = {'###': '' }

        match = False
        for shotgun_user, shotgun_user_id in shotgun_user_ids.iteritems():
            if shotgun_user == self.linux_username:
                self.shotgun_user_id = shotgun_user_id
                match = True

        if not match:
            self.shotgun_user_id = int(raw_input('\nEnter your shotgun user ID ' \
                                                 '(run script with -id to ' \
                                                 'find what it is): '))
    
    def set_users_shotgun_id(self):
        if self.locate_user_shotgun_id:
            self.find_user_shotgun_id()
        else:
            self.known_user_shotgun_id()

    def generate_all_jobs_shotgun_details(self):
        self.all_job_details = {'job_name':['###', '###',  
                                            '###', '###', '###', 
                                            '###', '###',
                                            '###', '###', '###'], 
                                'project_id': ['###', '###', '###', '###',
                                               '###', '###', '###', 
                                               '###', '###',],
                                'client_id': ['###', '###', '###', '###',
                                              '###', '###', '###', 
                                              '###', '###'],
                                'delivery_method': ['###', '###',  
                                                    '###', '###','###', 
                                                    '###', '###', 
                                                    '###', '###', '###']}

    def generate_contents_and_title_fields(self):
        if self.in_or_out == 'in':
            for the_file in self.ingested_files:
                self.contents += str(subprocess.Popen('ls -1 -R ' + \
                                     self.contents_folder + the_file,
                                     stdout=subprocess.PIPE, 
                                     shell=True).communicate()[0])
                self.title += the_file + ', '

        if self.in_or_out == 'out':
            self.contents = str(subprocess.Popen('ls -1 -R ' + self.contents_folder,
                                stdout=subprocess.PIPE, 
                                shell=True).communicate()[0])
            split_contents_folder = self.contents_folder.split('/')
            self.title = split_contents_folder[-1]
            if not self.title:
                self.title = split_contents_folder[-2]

    def populate_delivery_fields(self):
        todays_date = datetime.datetime.now()
        self.shotgun_job_details = {'job_name': self.all_job_details['job_name'][self.job_num],
                                    'title': self.title,
                                    'date': todays_date.strftime('%Y-%m-%d'),
                                    'project_id': self.all_job_details['project_id'][self.job_num],
                                    'to_client': {'type': 'ClientUser', 
                                                  'id': self.all_job_details['client_id'][self.job_num]},
                                    'delivery_method': self.all_job_details['delivery_method'][self.job_num],
                                    'delivery_template': {'type':'TaskTemplate', 'id': 8},
                                    'contents': self.contents }

        if self.in_or_out == 'in':
            self.shotgun_job_details['from_user'] = {'type': 'ClientUser', 
                                                     'id': self.all_job_details['client_id'][self.job_num]}
            self.shotgun_job_details['to_user'] = {'type': 'HumanUser', 
                                                   'id': int(self.shotgun_user_id)}
            self.shotgun_job_details['status'] = 'recd'                                                                                                                                                       
            self.shotgun_job_details['delivery_type'] = 'IN'
        elif self.in_or_out == 'out': 
            self.shotgun_job_details['from_user'] = {'type': 'HumanUser',
                                                     'id': int(self.shotgun_user_id)}
            self.shotgun_job_details['to_user'] = {'type': 'ClientUser', 
                                                   'id': self.all_job_details['client_id'][self.job_num]}
            self.shotgun_job_details['status'] = 'dlvr'
            self.shotgun_job_details['delivery_type'] = 'OUT'

    def build_shotgun_delivery(self):
        self.delivery_data = {
            'project': {"type": "Project",
                        "id": self.shotgun_job_details['project_id']},
            'title': self.shotgun_job_details['title'],
            'sg_from': self.shotgun_job_details['from_user'],
            'addressings_to': [self.shotgun_job_details['to_user']],
            #'addressings_cc': [cc_user],
            'sg_delivery_method': self.shotgun_job_details['delivery_method'],
            'sg_contents': self.shotgun_job_details['contents'], 
            'sg_status_list': self.shotgun_job_details['status'],
            'sg_delivery_type': self.shotgun_job_details['delivery_type'],
            'task_template': self.shotgun_job_details['delivery_template']
        }

        if self.in_or_out == 'in':
            desc = 'Recevied '
            self.delivery_data['sg_received_date'] = self.shotgun_job_details['date']
        elif self.in_or_out == 'out':
            desc = 'Delivered '
            self.delivery_data['sg_due_date'] = self.shotgun_job_details['date']
 
        self.delivery_data['description'] = '%s %s' \
                                            % (desc, 
                                            self.shotgun_job_details['title'])

    def link_shotgun_delivery(self):
        create_del = self.sg.create("Delivery", self.delivery_data)

        link_file_data = {
            'this_file': {
                'local_path': self.contents_folder,
                'name': self.shotgun_job_details['title'],
                },
            'attachment_links': [{'type': 'Delivery', 
                                  'id': create_del['id']}],
            'project': {'type': 'Project',
                        'id': self.shotgun_job_details['project_id']}
        }

        self.sg.create('Attachment', link_file_data)
        print '\nShotgun delivery created.\n'

class IngestFiles(object):
    def __init__(self, **kwargs):
        self.directory = kwargs['directory']
        self.ingest_all_files = kwargs['ingest_all_files']
        self.external_drive = kwargs['external_drive']
        self.alternate_destination = kwargs['alternate_destination']
        self.filenames = kwargs['filenames']
        self.job_name = kwargs['job_name']
 
        self.files_to_ingest = []
        self.ingest_cmds = []
        todays_date = datetime.datetime.now()
        self.in_folder = '/###/%s/###/%s/' % \
                         (self.job_name, 
                         todays_date.strftime('%Y%m%d'))
        self.base_ingest_cmd = 'rsync --archive --human-readable ' \
                               '--copy-links --stats --info=progress2 ' \
                               '###@###'

    def create_ingest_cmds(self):
        if self.ingest_all_files or len(self.filenames) == 1:
            self.remove_problem_chars_from_all_filenames()
        else:
            self.remove_problem_chars_from_chosen_filename()
        self.build_ingest_cmds()

    def remove_problem_chars_from_all_filenames(self):
        """
        removes spaces, colons, and slashes from 
        filenames by running a script on the io machine
        """
        for the_file in self.filenames:
            quoted_file = '"' + the_file + '"'
            cmd = "ssh ###@### \
                  python ###/remove_spaces.py %s '%s'" % \
                  (self.job_name, quoted_file)
            subprocess.Popen(cmd, shell=True).wait()
            self.files_to_ingest.append(''.join(the_file.split()))
    
    def remove_problem_chars_from_chosen_filename(self):
        for i in range(len(self.filenames)):
            print str(i+1) + ') %s' % self.filenames[i]
        try:
            answer = raw_input('\nEnter the number of the file to rsync: ')
            chosen_file = self.filenames[int(answer)-1]
            quoted_file = '"' + chosen_file + '"'
            cmd = "ssh ###@### \
                  python ###/remove_spaces.py %s '%s'" % \
                  (self.job_name, quoted_file)
            subprocess.Popen(cmd, shell=True).wait()
            self.files_to_ingest.append(''.join(chosen_file.split()))
        except:
            sys.exit('\nDafuq?')
            
    def build_ingest_cmds(self):
        for the_file in self.files_to_ingest:
            if self.external_drive and self.alternate_destination:
                ingest_cmd = '%s/###/%s/ %s' % \
                             (self.base_ingest_cmd, self.external_drive[0],
                             self.alternate_destination[0])

            elif self.external_drive:
                ingest_cmd = 'mkdir -p %s && %s' \
                             '/###/%s/ %s/%s/%s/' % \
                             (self.in_folder, self.base_ingest_cmd, 
                             self.drive[0], in_folder, 
                             the_file, drive[0])

            elif self.alternate_destination:
                ingest_cmd = '%s/###/%s/###/%s %s' % \
                             (self.base_ingest_cmd, self.job_name, 
                             the_file, self.alternate_destination[0])
            
            else:
                ingest_cmd = 'mkdir -p %s && %s' \
                             '/###/%s/###/%s %s' % \
                             (self.in_folder, self.base_ingest_cmd,
                             self.job_name, the_file, self.in_folder)
                                        
            self.ingest_cmds.append(ingest_cmd)

class FileParser(object):                                                                                                                                              
    def __init__(self, **kwargs):
        self.from_file = kwargs['from_file']

        self.incrementers = {'symlink': 0, 'mov': 0, 'dpx': 0, 'tif': 0, 
                             'exr': 0, 'vfx': 0, 'scan': 0, 'misc': 0}
        self.all_shot_types = {'1': 'mov', '2': 'vfx', '3': 'dpx', '4': 'exr', 
                               '5': 'tif', '6': 'misc'}

    def create_transfer_cmds(self):
        self.parse_raw_shot_names()
        self.replace_spaces_with_underscores()
        self.ask_user_for_shot_types()
        self.check_if_valid_shot_type()
        self.set_all_scenes_and_jobs()
        self.find_matching_job_and_scene()
        self.build_shot_paths()
        self.create_out_directories()
        self.build_transfer_cmds()

    def parse_raw_shot_names(self):
        if self.from_file:
            with open(self.from_file) as f:
                self.shots = f.readlines()
            f.close()
        else:
            shots = raw_input('\nEnter comma seperated file names:\n')
            self.shots = shots.split(',')

    def replace_spaces_with_underscores(self):
        for shot in self.shots:
            shot = shot.replace(' ', '_')

    def ask_user_for_shot_types(self):
        answer = raw_input('\n1)mov\t' \
                           '2)vfx\t' \
                           '3)dpx\t' \
                           '4)exr\t' \
                           '5)tif\t' \
                           '6)misc' \
                           '\n\nFile type(s): ')
        self.answer = answer.split(',')

    def check_if_valid_shot_type(self):
        noMatch = 0
        self.shot_types = []
        for i in range (len(self.answer)):
            for num, shot_type in self.all_shot_types.iteritems():
                if self.answer[i] == num:
                    self.shot_types.append(shot_type)
                    noMatch = 0
                    break
                else:
                    noMatch += 1
                    if noMatch >= len(self.all_shot_types):
                        print 'Invalid selection: %s ' \
                              '\nEnter a number 1-%s' % \
                              (self.answer[i], len(self.all_shot_types)+1)
                        self.shot_types = []
                        self.ask_user_for_shot_types()
                        self.check_if_valid_shot_type()

    def set_all_scenes_and_jobs(self):
        self.all_scenes = []
        for shot in self.shots:
            self.all_scenes.append({'###': shot[0:6], '###': shot[0:7], 
                                    '###': shot[4:7], '###': shot[0:3],
                                    '###': shot[0:6], '###': shot[0:6],
                                    '###': shot[0:6]})

    def find_matching_job_and_scene(self): 
        self.scenes = []
        self.jobs = []
        try: #incase ###'s ### folder no longer exists
            for job_and_scene in self.all_scenes:
                for job, scene in job_and_scene.iteritems():
                    scenes = os.listdir('/###/' + job + '/###')
                    for s in scenes:
                        if s == scene or s.lower() == scene or s.upper() == scene:
                            self.scenes.append(scene)
                            self.jobs.append(job)
        except:
            pass

    def build_shot_paths(self):
        self.shot_paths = []
        print '\nRunning following commands to find files...'
        for i in range(len(self.shots)):
            for shot_type in self.shot_types:
                find_shot = 'find /###/%s/###/%s/ -name "%s' % \
                            (self.jobs[i], self.scenes[i], self.shots[i])
                if shot_type == 'mov':
                    # -print -quit to exit after first match
                    # f to only look for files
                    find_shot += '.mov" -type f -print -quit'
                else:
                    # d to only look for directories
                    find_shot += '" -type d -print -quit'

                print '\n' + find_shot
                shot_path = subprocess.Popen(find_shot, 
                                             stdout=subprocess.PIPE, 
                                             shell=True).communicate()[0]
                if not shot_path:
                    '\nFile not found %s' % find_shot
                else:
                    self.shot_paths.append(shot_path[:-1]) #remove \n char
                
        print '\n%s files found' % len(self.shot_paths)

    def create_out_directories(self):
        self.dests = []
        todays_date = datetime.datetime.now()
        for job in self.jobs:
            for shot_type in self.shot_types:
                dest = '/###/%s/###/%s/###_%s/%s/' % (job, 
                                                       todays_date.strftime('%Y%m%d'),
                                                       todays_date.strftime('%Y%m%d'),
                                                       shot_type)
                subprocess.Popen('mkdir -p ' + dest, shell=True)
                self.dests.append(dest)
                
    def build_transfer_cmds(self):
        self.transfer_cmds = []
        for i in range(len(self.shot_paths)):
            transfer_cmd = 'rsync --verbose --archive --human-readable ' \
                           '%s %s' % (self.shot_paths[i], self.dests[i])
            self.transfer_cmds.append(transfer_cmd)

class DeliverFiles(object):
    def __init__(self, **kwargs):
        self.directory = kwargs['directory']
        self.external_drive = kwargs['external_drive'],
        self.job_name = kwargs['job_name'],
        self.verbose = kwargs['verbose']
        self.deliver_cmds = []
        self.base_deliver_cmd = 'rsync --archive --human-readable ' \
                                '--copy-links --stats --info=progress2'

    def build_deliver_cmds(self):
        if self.external_drive[0]:
            deliver_cmd = ('%s %s ###@###:/###/%s' % \
                           (self.base_deliver_cmd,
                           self.directory, self.external_drive[0][0]))
        else:
            deliver_cmd = ('%s %s ###@###:' \
                           '/###/%s/###/' % \
                           (self.base_deliver_cmd, 
                           self.directory, self.job_name[0]))
        
        self.deliver_cmds.append(deliver_cmd)

class Transfer(object):
    def __init__(self, **kwargs):
        self.verbose = kwargs['verbose']
        self.transfer_cmds = kwargs['transfer_cmds']
        if not self.transfer_cmds:
            sys.exit('Nothing to transfer.\nAborting.')

    def start_transfer(self):
        self.print_transfer_cmds()
        self.run_transfer_cmds()
        self.calc_total_transfer_time()
        self.print_transfer_status()

    def print_transfer_cmds(self):
        print '\nTRANSFER COMMANDS\n' 
        for transfer_cmd in self.transfer_cmds:
            print transfer_cmd + '\n'

    def run_transfer_cmds(self): 
        self.transfer_fail_cmds = []
        self.start_time = int(time.time())
        for transfer_cmd in self.transfer_cmds:
            transfer_status = subprocess.Popen(transfer_cmd, shell=True).wait()
            if transfer_status != 0:
                self.transfer_fail_cmds.append(transfer_status)
        self.end_time = int(time.time())
 
    def calc_total_transfer_time(self):
        total_time = self.end_time - self.start_time
        self.transfer_time =  time.strftime("%H:%M:%S", 
                                            time.gmtime(total_time))

    def print_transfer_status(self):
        print '\n---------- TRANSFER TIME: %s' \
              % self.transfer_time, '------------'
        if not self.transfer_fail_cmds:
            print '------------ TRANSFER COMPLETED ---------------\n'
            ascii_art.brain()
            self.outcome = 'completed'
        else:
            print '-------------- TRANSFER FAILED --------------\n'
            self.outcome = 'failed'

