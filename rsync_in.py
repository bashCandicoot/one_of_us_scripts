#!/usr/bin/python 
#: Title        :rsync_in
#: Date         :2016-04-13
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :rsyncs dir(s) from IO machine to IN folder
#: Options      :-e, -d, -l, -a, -id
import ascii_art
import argparse
import oou_io
import subprocess

"""
example usage:

    "rsync_in xxx"
    transfer xxx from the io machine 
    create a shotgun delivery for xxx
 
    "rsync_in xxx -d MTD009 -e -a -l /###/xxx/###/###"
    transfer all files for job xxx from an external drive called MTD009 
    to a location called /###/xxx/###/###
    email the user the outcome of the transfer
    create a shotgun delivery for xxx
 
"""


parser = argparse.ArgumentParser()
parser.add_argument("directory",
                    help="directory name/job name that corrosponds to the data coming in")
parser.add_argument("-e", "--send_user_email", 
                    help="email user the status of the transfer", \
                    action="store_true")
parser.add_argument("-d", "--external_drive", \
                    help="ingest from an external drive", \
                    nargs=1)
parser.add_argument("-n", "--no_shotgun_delivery", \
                    help="does not create a shotgun delivery report", \
                    action="store_true")
parser.add_argument("-id", "--locate_user_shotgun_id", \
                    help="explains to the user how to find " \
                    "their shotgun id", \
                    action="store_true")
parser.add_argument("-a",
                    "--ingest_all_files",
                    help="ingest all files within the io IN folder",
                    action="store_true")
parser.add_argument("-l",
                    "--alternate_destination",
                    help="ingest to an alternate destination",
                    nargs=1)
parser.add_argument("-v",
                    "--verbose",
                    help="outputs more detailed transfer information",
                    action="store_true")
args = parser.parse_args()

shotgun_script_name = 'rsync_in'     
shotgun_script_key = '###'

linux_username = oou_io.get_linux_username()
all_job_names = oou_io.get_all_job_names()
job_num, job_name = oou_io.set_job_num_name(all_job_names, args.directory)
filenames = oou_io.list_job_contents_of_io_machine_ingest_directory(args.directory)

ingest = oou_io.IngestFiles(directory = args.directory,
                            external_drive = args.external_drive,
                            ingest_all_files = args.ingest_all_files,
                            alternate_destination = args.alternate_destination,
                            filenames = filenames,
                            job_name = job_name,
                            verbose = args.verbose)
ingest.create_ingest_cmds()

transfer = oou_io.Transfer(transfer_cmds = ingest.ingest_cmds,
                           verbose = args.verbose)
transfer.start_transfer()

if transfer.outcome == 'completed':
    for the_file in ingest.files_to_ingest:
        cmd = 'ssh ###@### \'rm -rf '\
              '/###/%s/###/%s\'' % (job_name, the_file)
        subprocess.Popen(cmd, shell=True).wait()


if not args.no_shotgun_delivery:
    sg_deliv = oou_io.ShotgunDelivery(in_or_out = 'in',
                                      ingested_files = ingest.files_to_ingest,
                                      contents_folder = ingest.in_folder,
                                      locate_user_shotgun_id = args.locate_user_shotgun_id,
                                      linux_username = linux_username, 
                                      job_num = job_num,
                                      job_name = job_name,
                                      script_name = shotgun_script_name,
                                      script_key = shotgun_script_key)
    sg_deliv.create_shotgun_delivery()

if args.send_user_email:
    oou_io.send_email(list_of_recipients = linux_username.split(),
                      subject = 'Transfer status',
                      message = '%s has %s transferring - %s' % \
                                (args.directory,
                                 transfer.outcome,
                                 transfer.transfer_time))
