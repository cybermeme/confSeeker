#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
com-commander is the main software of confseeker

mind that I implement variables names in camelcase and constantes and fonctions
name with '_' even if it is not bests practices it is easier to me to read the code

@author: cybermeme
"""

# LIBRARIES BEGIN #

import libtmux
import os
import sys
import pickle
import random

# LIBRARIES END #




# If Ansible path in path, keep this path, else get the own directory
if '/opt/addSofts/confSeeker/tools/' in os.environ['PATH']:
    base_tool_dir = ('/opt/addSofts/confSeeker/tools/')
else:
    base_tool_dir = (os.getcwd() + '/tools/')



# VARIABLES BEGIN #

temporary_confseeker_file = '/tmp/confSeeker.tmp'
base_folder = '/etc'
default_file = '/etc/motd'
defaut_list_file_tool = (base_tool_dir + 'cat_file.py')
#defaut_list_file_tool = 'less'

# VARIABLES END #



# DEFINITIONS BEGIN #

def random_number():
    return random.getrandbits(16)


def ersase_config():
    """efface la configuration dans un fichier"""
    try:
        os.system('rm ' + temporary_confseeker_file)
        return 0
    except:
        exit("erasing Error")


def save_config(dataSave):
    """sauvegarde la configuration dans un fichier"""
    try:
        with open(temporary_confseeker_file, 'ab') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(dataSave)
            return 0
    except:
        exit("Saving Error")


def load_config():
    """charge la configuration depuis un fichier"""
    with open(temporary_confseeker_file, 'rb') as fichier:
        mon_depickler = pickle.Unpickler(fichier)
        dataLoad = []
        while True:
            try:
                dataLoad += [mon_depickler.load()]
            except:
                break
        print('Data Read'.center(45, '*'))
        return dataLoad


def file_base_definition():
    '''' if no argument /etc ... we print the motd '''
    try:
        return sys.argv[1]
    except:
        return default_file


def creation_two_panes_first_zone(folder=base_folder):
    ''' opens a tmux server and prepares the display 
        by cutting out the panes '''
    global leftPane
    global underPane
    global rightPane
    server = libtmux.Server()
    session = server.new_session('com_comander')
    window = session.select_window('com_comander')
    leftPane = window.attached_pane
    underPane = window.split_window()
    rightPane = window.split_window(vertical=False)
    window.select_pane('%1') #choose which pane will have the hand
    underPane.send_keys('cd ' + folder + '; clear')
    save_config(session)


def load_from_file(file):
    ''' opens a file and returns the contents '''
    data = ''
    try:
        f = open(file, "r")
        data = f.read()
        f.close()
    except:
        pass
    return data


def triage(file):
    ''' sorts the type of configuration file and sends
        it to the right parser '''
    first_line = load_from_file(file)
    
    if first_line.startswith('<?xml'):
        leftPane.send_keys(base_tool_dir + 'xml_parser.py '+ file)
        
    else:
        leftPane.send_keys(base_tool_dir + 'unix_parser.py '+ file)


def creation_two_panes(file1 = '', file2 = ''):
    ''' launches the creation_two_panes of the tmux display and 
        launches the display in the panes '''
    creation_two_panes_first_zone()
    
    if file1 and file2:
        rightPane.send_keys(defaut_list_file_tool + ' ' + (file1))
        leftPane.send_keys(defaut_list_file_tool + ' ' + (file2))
        underPane.send_keys('diff ' + file1 + ' ' + file2)
        
    else:
        #print in the right panes
        rightPane.send_keys(defaut_list_file_tool + ' ' +\
                            (file_base_definition()))
        #print in the left panes
        triage(file_base_definition())
    #open tmux and attach the session
    os.system('tmux attach-session')


def close_session():
    ''' Close the window '''
    server = libtmux.Server()
    session = load_config()
    print(window)
    session.kill_window()


def exit_session():
    ''' Close the software '''
    server = libtmux.Server()
    ersase_config()
    server.kill_session('com_comander')


def com_comander():
    ''' main function parsing the arguments '''
    if len(sys.argv) == 4 and sys.argv[1] == "diff":
        creation_two_panes(sys.argv[2], sys.argv[3])
        
    elif len(sys.argv) == 2 and (sys.argv[1] == "help" or sys.argv[1] == "-h"):
        help_com_comander()
  
    elif len(sys.argv) == 2 and sys.argv[1] == "close":
        close_session()
        
    else:
        #if no session create one
        try:
            creation_two_panes()
        #if session parse the arguments
        except:
            com_comander_parser()


def com_comander_parser():
    ''' parse the arguments
        I chose to do it manually rather than using argparse in order to be 
        able to launch the environment without argument.'''
        
    if len(sys.argv) == 2 and sys.argv[1] == "quit":
        exit_session() 
        
    elif len(sys.argv) == 2 and sys.argv[1] == "help":
        help_com_comander() 


def help_com_comander():
    ''' Print the help message '''
    print('\n\tUsage : ' + sys.argv[0] + ' /path/to/file/to/parse\n\n' \
          + sys.argv[0] + ' help = this message in the commander\n' \
          + sys.argv[0] + ' diff /path/to/file1 /path/to/file2 = diff 2 files\n' \
          + sys.argv[0] + ' close = close the window\n' \
          + sys.argv[0] + ' quit = close the tool\n')

# DEFINITIONS END #



# START #

# If sudo, set UID 0 to keep the good rights to open files
uid = os.getuid()

if uid == 0:
    os.setuid(uid) 

#Let's go
com_comander()

