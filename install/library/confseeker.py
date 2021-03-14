#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cybermeme
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: confseeker

short_description: adds the confseeker path in all .bashrc

version_added: "1.0.0"

description: This module will scan the /etc/passwd file for users home 
directories and then search for .bashrc files, if such a file exists, it 
will add the program path at the end

options:
    homeDirectory:
        description: the location of the home directories in the structure, 
        by default it is '/home'.
        required: false
        type: str
        default: /home
        
    shellConf:
        description: shell config file to add the PATH structure
        required: false
        type: str
        default: .bashrc
        
    passwordFile:
         description: location of the password file (to extract users home 
                                                     directory)
        required: false
        type: str
        default: /etc/passwd   
        
    uidMini:
        description: uid minimum to search for users 
        required: false
        type: int
        default: 500

author:
    - https://github.com/cybermeme (@cybermeme)
'''

EXAMPLES = r'''
# If you have weird users ;-)
- name: Users using ksh
  conseeker:
    shellConf: .kshrc

# UID minimum
- name: If you want to scan after the user 1005
  conseeker:
    uidMini: 1006

'''



# LIBRARIES BEGIN #

import os
from ansible.module_utils.basic import *

# LIBRARIES END #



# VARIABLES BEGIN #

result_ok = False

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


def base_rep_hunting(module):
    """ scan home directory and check if the folder is in passwd file """
    listUser = get_user_home()
    folder_inside = os.listdir(home_config_dir)
    for userScanned in folder_inside:

        for listUserString in listUser:

            if userScanned in listUserString:
                fullPath = (home_config_dir + '/' + userScanned)
                config_file_hunting(fullPath, module)
    return 0

def add_in_bashrc(fullPath, module):
    try:
        f = open(fullPath, "a")
        f.write("export PATH=$PATH:/opt/addSofts/confSeeker")
        f.close()
        global result_ok
        result_ok = True

    except:
        module.fail_json(msg="Can't open file .bashrc")   


def config_file_hunting(filePath, module):
    """ look for .bashrc """
    folder_inside = os.listdir(filePath)
    for files in folder_inside:

        if files == home_config_shell:
            fullPath = filePath + '/' + files

            try:
                f = open(fullPath, "r")
                searchLine = f.read()
                f.close()

                if not 'confSeeker' in searchLine:
                    add_in_bashrc(fullPath, module)

            except:
                module.fail_json(msg="Can't open file .bashrc") 
    return 0


def main():
    """ Definition of modules variables """
    fields = {
        "homeDirectory": {"default": "/home", "required": False, "type": "str"}, 
        "shellConf": {"default": ".bashrc", "required": False, "type": "str"}, 
        "passwordFile": {"default": "/etc/passwd", "required": False, "type": "str"}, 
		"uidMini": {"default": 500, "required": False, "type": "int"},
    }
    module = AnsibleModule(argument_spec=fields)

    global home_config_dir
    global home_config_shell
    global password_file
    global uid_mini

    home_config_dir = module.params.get('homeDirectory')
    password_file = module.params.get('passwordFile')
    uid_mini = module.params.get('uidMini')
    home_config_shell = module.params.get('shellConf')

    base_rep_hunting(module)


    if result_ok:
        module.exit_json(changed=True, msg=module.params)

    else:
        module.exit_json(changed=False, msg=module.params)  

# DEFINITIONS END #



# EXECUTION #

if __name__ == "__main__": 
    main()