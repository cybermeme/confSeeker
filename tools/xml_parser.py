#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parses an xml file and waits before returning to the prompt

@author: cybermeme
"""

import sys
import os
import xml.etree.cElementTree as ET

def xml_decode(fileName):
    ''' opens an xml and calls the function for parsing '''
    dataReturn = []
    openFile = ET.ElementTree(file=fileName)
    for elem in openFile.iter():
        print (elem.tag, elem.attrib)


os.system('clear')

xml_decode(sys.argv[1])

input()
print('\n'*2 + 'Back in Prompt\n')