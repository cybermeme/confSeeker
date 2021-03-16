# Tools Directory

## In this directory are the tools to display or parse documents

* cat_file.py performs the equivalent of the cat command but waits for a 'Return' to give up a prompt (the only use is to have a cleaner display).
* unix_parser.py will, in addition to cat_file.py, remove comment lines starting with '#' or ';'.
* xml_parser.py will, in addition to cat_file.py, remove comments from the xml file and display the remaining tags in JSON format (beware that this does not preserve the indentation, so you must check the original)

