#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: cybermeme
"""


# LIBRARIES BEGIN #

import os

#from ansible.module_utils.basic import AnsibleModule 

from ansible.module_utils.basic import *

# LIBRARIES END #



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

    module.exit_json(changed=False, msg=module.params)  

# DEFINITIONS END #



# EXECUTION #

if __name__ == "__main__": 
    main()