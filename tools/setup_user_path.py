#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Need to be run as root

@author: cybermeme
"""

# LIBRARIES BEGIN #

import os

# LIBRARIES END #



# VARIABLES BEGIN #

uid_mini = 500
password_file = "/etc/passwd"
home_config_shell = '.bashrc'

# VARIABLES END #



# DEFINITIONS BEGIN #

def get_user_home():
    """ grep users directory in /etc/passwd file """
    with open(password_file) as file:
        listRep = []
        for line in file:
            if  int(line.split(":")[2])  >= uid_mini and not 'nologin' in line:
            # home extraction
                listRep += [line.split(":")[5]]
    return listRep


def base_rep_hunting(folder='/home/'):
    """ scan home directory and check if the folder is in passwd file """
    listUser = get_user_home()
    folder_inside = os.listdir(folder)
    for userScanned in folder_inside:
        if userScanned in listUser:
            fullPath = (folder + '/' + userScanned)
            config_file_hunting(fullPath)
    return 0


def config_file_hunting(filePath):
    """ look for .bashrc """
    fileName = os.path.basename(filePath)
    if fileName == home_config_shell:
        fullPath = filePath + '/' + fileName
        try:
            f = open(fullPath, "a")
            f.write("export PATH=$PATH:/opt/addSofts/confSeeker")
            f.close()
        except:
            return 1
    return 0


def main():
    try:
        base_rep_hunting()
    except:
        return 1

# DEFINITIONS END #



# EXECUTION #

if os.getuid() == 0:
    main()
else:
    return "Warning, this program have to be run as root"