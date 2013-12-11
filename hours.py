#!/usr/bin/env python

import os, csv
from collections import OrderedDict
from dateutil import parser
from pprint import pprint


command = 'git log --pretty=format:"%ad|%x09%s" --since="2013-06-07" > log.txt'

os.system(command)

commits = []

with open('log.txt', 'rb') as fh:
    reader = csv.reader(fh, delimiter='|')
    for timestamp, cm in reader:
        timestamp = parser.parse(timestamp)
        cm = cm[1:]
        commits.append((timestamp, cm))

commits.reverse()

# First item in the list is first commit
# All commits in chronological order


dates = OrderedDict()
for commit in commits:
    timestamp, message = commit
    date = timestamp.date()
    if not date in dates:
        dates[date] = [commit,]
    else:
        dates[date].append(commit)

def getInt(msg):
    initial = raw_input(msg)
    while True:
        if initial.isdigit():
            break
        else:
            initial = raw_input(msg)
    return int(initial)


hours = 0

mode = raw_input('Manual or automatic counting?: ')
if mode.lower() == 'manual':
    manual = True
elif mode.lower() == 'automatic':
    manual = False
else:
    print 'Error! Input either "manual" or "automatic"'
    exit(1)

for date in dates:
    print '%d hours so far' % hours
    print date.strftime('%A %B %d')
    print '=' * len(str(date))

    start = dates[date][0][0]
    end = dates[date][-1][0]
    delta = (end-start).seconds/60.0/60.0
    print '%s - %s = %r hours\n' % (end.strftime('%H:%M %p'), start.strftime('%H:%M %p'), round(delta, 2))

    for commit in dates[date]:
        timestamp, message = commit
        print timestamp.strftime('%I:%M:%S %p or %H') + '\t' + message
    print '\n'
    if manual:
        section = getInt('Today\'s hours: ')
        hours += section
        dates[date].append(section)
    else:
        hours += delta
        dates[date].append(delta)
    os.system('clear')

os.system('clear')
print '%r total hours!' % hours
for date in dates:
    section = dates[date][-1]
    print date, '\t%r hours' % section