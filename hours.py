#!/usr/bin/env python

import os, csv
from dateutil import parser


command = 'git log --pretty=format:"%ad|%x09%s" > log.txt'
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

