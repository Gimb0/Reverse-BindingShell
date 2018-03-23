# Reverse-BindingShell

Reverse or binding shell written in Python3.

Works on Windows, Linux, Mac if python3 is installed.


Running the programs looks something like:

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
  


It is necessary to run the program that will be listening for a connection first.
