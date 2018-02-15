#!/usr/bin/python 
#: Title        :rsync_out
#: Date         :2016-03-07
#: Author       :Steve Green
#: Email        :steve@weacceptyou.com
#: Description  :transfers symlinks to the OUT folder
#: Options      :-f, -e, -id, -io, -v

import argparse
import oou_io
"""
example usage:

    "shotgun_out /###/xxx"
    rsync directory xxx to the io machine 
    create a shotgun delivery for xxx

    "shotgun_out /###/xxx -d MTD009 -e"
    rsync directory xxx to an external drive called xxx 
    email the user the outcome of the rsync transfer
    create a shotgun delivery for xxx

"""

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--from_file", \
                    help="reads symlinks from file",
                    nargs=1)
parser.add_argument("-e", "--send_user_email", 
                    help="email the user the status of the transfer", \
                    action="store_true")
parser.add_argument("-id", "--locate_user_shotgun_id", \
                    help="explains to the user how to find " \
                         "their shotgun id", \
                    action="store_true")
parser.add_argument("-v",
                    "--verbose",
                    help="outputs more detailed transfer information",
                    action="store_true")
args = parser.parse_args()

shotgun_script_name = 'rsync_out'
shotgun_script_key = '###'

file_parser = oou_io.FileParser(from_file = args.from_file)
file_parser.create_transfer_cmds()

transfer = oou_io.Transfer(transfer_cmds = file_parser.transfer_cmds, 
                           verbose = args.verbose)

transfer.start_transfer()

if args.send_user_email:                                   
    oou_io.send_email(list_of_recipients = linux_username.split(),
                      subject = 'Transfer status',
                      message = '%s has %s transferring - %s' % \
                                (args.directory,
                                 transfer.outcome,
                                 transfer.transfer_time))
