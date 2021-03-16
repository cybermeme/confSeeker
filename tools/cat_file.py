#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shows a file and waits before returning to the prompt

@author: cybermeme
"""

import os
import sys


def load_from_file(file):
    ''' open a file and print in like cat command '''
    data = ''
    try:
        f = open(file, "r")
        data = f.read()
        f.close()

    except:
        pass
    print(data)


os.system('clear')
load_from_file(sys.argv[1])
input()
print('\n'*2 + 'Back in Prompt\n')