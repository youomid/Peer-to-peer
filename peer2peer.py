# Peer-to-peer file sharing program
# Original Version witten in April, 2015

from client import Client
from incomingrequests import IncomingRequests

import socket
import time
import threading
import SocketServer

# handle incoming connections from other peers, start a thread for each connection
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  
    def handle(self):
        
        cur_thread = threading.current_thread()
        thread_name = cur_thread.name

        # receive the command
        data = self.request.recv(1024)
        time.sleep(1)

        try:
            # handle the command after decoding the data
            client.handleIncomingRequests(data.decode('UTF-8'), self)

        finally:

            time.sleep(30)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer,):
    """Nothing to add here, inherited everything necessary from parents"""
    pass

# set up the server 
def setupServer(client):

    server = ThreadedTCPServer((client.getIpAddress(), int(client.getPortNumber())), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    return server

    
# switch case alternative for determining what type of command, internal or external
def checkCommandType(nextCommand):

    return {'LISTL': 'Internal', 'RESET': 'Internal',
            'LISTR': 'External', 'DISCOVER': 'External', 'GET': 'External'}.get(nextCommand, 0)


def main():

    # set up new client
    
    # own information
    client = Client('Alex', 'localhost', '2002')
    
    # first peer it knows of
    client.addPeer(['Robert','localhost','2000'])
    
    # file the peer wants to share
    client.addFile('logo1.png')
    
    # start the server thread to handle incoming data
    
    server = setupServer(client)

    # handle user input
    
    nextCommand = ''

    # program runs until the user's next command is to quit
    while nextCommand != 'QUIT':

        nextCommand = raw_input('Input your next command: ')

        requestType = checkCommandType(nextCommand)

        # process a command that does not require external communication with another peer
        if requestType == 'Internal':

            client.handleInternalRequest(nextCommand)
            
        # process a command that does require external communication with another peer
        elif requestType == 'External':

            client.handleExternalRequest(nextCommand)

    # shutdown server by command
    if nextCommand == 'QUIT':

        server.shutdown()

if __name__ == '__main__':
    main()

