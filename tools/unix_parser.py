#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
print a file by removing the comment lines and wait
    before returning to the prompt

@author: cybermeme
"""
import os
import sys


def clean_line(data):
    ''' remove the lines beginning with # or ;; '''
    if not data.startswith('#') and not data.startswith(';;'):
        return data.replace("\n","")
    else:
        pass

# nettoyage des fichiers == grep -v '^#' | grep -v '^$'
def clean_file(file):
    ''' opens a file calls the function to remove comments and displays 
        the result with the line number '''
    dataReturn = ''
    compteur = 0
    try:
        openFile = open(file, "r")
        data = openFile.readlines()
        for lines in data:
            compteur += 1
            dataClean = clean_line(lines.strip())
            if dataClean != None and dataClean != '':
                joliData = ('Ligne ' + str(compteur)).ljust(12,'-')
                print(joliData, dataClean)
        f.close()
    except:
        return 1
    return 0



os.system('clear')
clean_file(sys.argv[1])
input()
print('\n'*2 + 'Back in Prompt\n')