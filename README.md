# Reverse-BindingShell

## Description
This is a reverse or binding shell written in Python3. I have gotten it to work on Windows, Mac, and Linux systems. This program was made as an exercise but can be used to remotely manage another host. It is not to be used without authorization.

## Usage
Linux and mac systems:
"python3 Shell_[Client or Server].py [options]"

Both python programs have built in help to run the program. 

Shell_Client.py help:

	usage: Shell_Client.py [-h] [-l | -c] [-s SERVER] [-p PORT]

	optional arguments:

	  -h, --help            show this help message and exit

      -l, --listen          Listen for reverse shell.

	  -c, --connect         Connect to binding shell

	  -s SERVER, --server SERVER
                          Server to connect to.
	  -p PORT, --port PORT  Port to connect to or listen on


Shell_Server.py help:

	usage: Shell_Server.py [-h] [-b | -r] [-s SERVER] [-p PORT]

	optional arguments:

	  -h, --help            show this help message and exit
	
	  -b, --bind            Bind shell to port.
	
	  -r, --reverse         Reverse shell.
	
	  -s SERVER, --server SERVER
						Server to connect to. [Only used for reverse shell]
	  -p PORT, --port PORT  Port to connect to.
