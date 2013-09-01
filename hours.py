#!/usr/bin/env python

import os

command = 'git log --pretty=format:"%ad|%x09%s" > log.txt'
os.system(command)
