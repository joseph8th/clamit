#!/usr/bin/env python

import os
import sys
import shutil


def printhelp():
    ''' Method to print help and exit. '''

    print "usage: clamit.py /path/to/clamscan.log [/path/to/quarantine/directory]\n"
    print "Quarantined files will be moved to a directory in the root of the target"
    print "filesystem if no quarantine directory is provided."
    exit(1)


def quarantine(infected):
    ''' Method to quarantine an infected file. '''

    if not os.path.exists(q_path):
        # create the quarantine dir if it doesn't exist
        try:
            os.makedirs(q_path)
        except OSError as e:
            print "OSError({0}): {1}".format(e.errno, e.strerror)
            return False

        # copy the clamscan log file into the quarantine for possible restores
        shutil.copy2(f_path, q_path)

    # move the src file to new dst ...
    shutil.move(infected, q_path)
    return True
            

###### 'main' function ######

if len(sys.argv) < 2:
    printhelp()

# required clamscan log file argument
f_path = os.path.abspath(sys.argv[1])
if not os.path.exists(f_path):
    print "File not found: '{0}'".format(f_path)
    exit(1)

# optional quarantine path argument
if len(sys.argv) == 3:
    q_path = os.path.join(os.path.abspath(sys.argv[2]), 'clam-quarantine')
else:
    q_path = os.path.join(os.getcwd(), 'clam-quarantine')

# process the clamscan log file ...
print "Processing clamscan log file '%s' ..." % (f_path)
print "  --> Quarantine path: '%s'\n" % (q_path)

try:
    f = open(f_path, 'r')
except IOError as e:
    print "IOError({0}): {1}".format(e.errno, e.strerror)
    exit(1)

log_l = list(f)

for line in log_l:
    if "FOUND" in line:
        line = line.split(':')
        print line[1].strip() + "\n  --> " + line[0]

        if not os.path.exists(line[0]):
            print "SKIPPING ... file not found.\n"
        else:                          # get user choice input for each infected file
            choice = raw_input("Delete, Quarantine or Ignore this file? [D/q/i]: ")

            if choice in ('q', 'Q'):       # quarantine
                if quarantine(line[0]):
                    print "Quarantined '" + line[0] + "' ..."
                else:
                    print "FAILED Quarantine operation!"

            elif choice in ('i', 'I'):     # ignore
                print "Ignored '" + line[0] + "' ..."

            else:                          # DEFAULT: delete
                print "Deleted '" + line[0] + "' ..."
                os.remove(line[0])

            print


