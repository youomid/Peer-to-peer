# Client Class responsible for creating peers.

from externalwork import ExternalRequest
from incomingrequests import IncomingRequests

class Client:

    clientName = ''
    ipAddress = ''
    portNumber = ''
    firstPeer = []
    
    knownPeers = []
    availableFiles = []
    
    def __init__(self, name, ip_address, port):
        
        self.clientName = name
        
        self.ipAddress = ip_address

        self.portNumber = port
        
    # add a new peer to the list of known peers, always hold onto the first known peer in case of a RESET command
    def addPeer(self, peerInfo):

        if len(self.firstPeer) == 0:

            self.firstPeer.append(peerInfo)
        
        self.knownPeers.append(peerInfo)
        
    # add a new file to the list of files this peer wants to share
    def addFile(self,fileName):

        self.availableFiles.append(fileName)
        
    # any request that is handled internally (ex. does not require outside communication)
    def handleInternalRequest(self,command):

        i = 0
        
        if command == 'LISTL':

            for File in self.availableFiles:

                print File
    
        elif command == 'RESET':

            del self.knownPeers[:]

            self.knownPeers.append(self.firstPeer)
    
    # any requests that involve connecting and communicating with other peers
    def handleExternalRequest(self,command):

        externalRequest = ExternalRequest()
        
        if command == 'LISTR':

            peer_ip_address = raw_input('Please enter the IP Address you would like to connect to: ')
            peer_port_number = raw_input('Please enter the port number: ')

            externalRequest.handleLISTR(peer_ip_address, peer_port_number)
 
        elif command == 'SEARCH':

            filename = raw_input('Please enter the name of the file you are looking for: ')
            timeToLive = raw_input('Please enter how far you would like to look (TTL) : ')

            peer_ip_address = knownPeers[0][1]
            peer_port_number = knownPeers[0][2]

            externalRequest.handleSEARCH(peer_ip_address, peer_port_number,
                                          file_name, timeToLive)
        
        elif command == 'DISCOVER':

            timeToLive = raw_input('Please enter how far you would like to look (TTL) : ')

            peer_ip_address = knownPeers[0][1]
            peer_port_number = knownPeers[0][2]

            externalRequest.handleSEARCH(peer_ip_address, peer_port_number,
                                         timeToLive)

        elif command == 'GET':

            file_name = raw_input('Please enter the name of the file you are looking for: ')
            peer_ip_address = raw_input('Please enter the IP Address of the peer you would like to get the file from: ')
            peer_port_number = raw_input('Please enter the port number: ')

            externalRequest.handleSEARCH(peer_ip_address, peer_port_number,
                                          file_name)
    # any requests received from other peers
    def handleIncomingRequests(self,command, socket):

        incoming_requests = IncomingRequests()
        
        if command == 'LISTR':
            
            incoming_requests.handleLISTR(socket, self.availableFiles)

        elif command == 'SEARCH':
            
            incoming_requests.handleSEARCH(socket, self.ipAddress, self.portNumber, self.availableFiles, self.knownPeers)

        elif command == 'DISCOVER':
            
            incoming_requests.handleDISCOVER(socket, self.ipAddress, self.portNumber, self.knownPeers)

        elif command == 'GET':
            
            incoming_requests.handleGET(socket, self.fileName)
        
    # get methods

    def getIpAddress(self):
        return self.ipAddress
    def getPortNumber(self):
        return self.portNumber
    
        
