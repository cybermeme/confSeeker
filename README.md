# confSeeker
An automation tool for people like me who are bored of having to do the same commands over and over again just to look at and modify a configuration file

## Automatic install
first install :
	- ansible
	- python3
	- tmux
Then:
```bash
$ cd install`
$ ansible-playbook ./setup.yml -u userNameWithAdminPrivileges
```

you can change the installation targets by changing the hosts parameter in setup.yml


## Manual install
	- python3
	- pip3
	- tmux

```bash
$ pip3 install -r ./requirement.txt`
```

### difference between the two types of installations.

Ansible will allow you to deploy the tool on the different servers you administrate.
The manual installation will only be available locally and you will have to manually add the PATH if you wish.
To add the path:

```bash
$ export PATH=$PATH:PathToConfseeker`
```
and for persistence, add this line to the end of your local shell configuration file (e.g. /home/$(whoami)/.bashrc)

## How it works

ConfSeeker calling libtmux, the function to change panels or to change windows. Once the program has been launched, it corresponds to the use of [tmux.](https://tmuxcheatsheet.com/)
The basic program will create the working environment with the libtmux library and will use tools (in the tools directory) to parse the files

For the installation, I used the Ansible tool and in order to be able to add the PATH of confSeeker in the configuration files of the already existing users, I created a module.
This module will look for the list of users in the home directory, will look for the home directories in the /etc/passwd file and if there is a correlation, will add the PATH at the end of this file.
For future users, the line has been added at the end of /etc/profile with a builtin module of Ansible.

## Usage

To start confSeeker, make sure confseeker is not already running.
If not, from the terminal, enter $ tmux attach-session

If no arguments are entered, confseeker will open /etc/motd

```bash
$ ./confSeeker.py help`
`
	Usage : ./confSeeker.py /path/to/file/to/parse`
`
./confSeeker.py help = this message in the commander`
./confSeeker.py diff /path/to/file1 /path/to/file2 = diff 2 files`
./confSeeker.py [close|quit] = close the tool`
```

By default, when running confSeeker with or without sudo depending on the rights of the file to be read, the program will open tmux and split the window into three:
    - At the top right, a cat of the requested file appears, to take over, you just have to hit 'Enter', it is possible by modifying the defaut_list_file_tool variable to open the file with another program (ex: less)
    - At the top left, the file appears after having been parsed to remove comments (lines starting with ';' or '#') and in JSON form if it was an xml file
    - At the bottom (panes having the hand by default), the user is directed automatically in the /etc folder (configurable by modifying the base_folder variable) and can thus carry out its administration functions

When the work is finished, to close the environment, you must call confSeeker with either the close or quit option

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)