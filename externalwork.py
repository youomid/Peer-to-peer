# Socket Class responsible for communicating with a peer, by first sending an external request

import socket

class ExternalRequest:
        
    # set up a socket and connect using the provided ip address and port number, and send the command to the peer
    def connectSocket(self,ipAddress, portNumber, command):
        global sock
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        server_address = (ipAddress, int(portNumber))

        sock.connect(server_address)

        # send the command to be handled by the peer
        sock.sendall(bytes(command, 'UTF-8'))
        time.sleep(1)
        
    # to get a list of the peers' available files, prepare a receiver to get the data and decode it
    def handleLISTR(self,ipAddress, portNumber):

        self.connectSocket(ipAddress, portNumber,'LISTR')

        # expect to receive data back, a list of their available files
        data = sock.recv(5000)
        
        print (data.decode('UTF-8'))
        
    # search for a specific file by connecting up to a number of peers depending on the time to live
    def handleSEARCH(self,ipAddress, portNumber, fileName, TTL):

        connectSocket(ipAddress, portNumber,'SEARCH')

        # send the peer the name of the file we are looking for, and
        # how far to look (TTL)
        sock.sendall(bytes(filename,'UTF-8'))
        time.sleep(1)
        sock.sendall(bytes(TTL, 'UTF-8'))
        time.sleep(1)

        while int(TTL) != 0:
            
            temp = [0, 0]
            temp2 = [0, 0, 0]

            # if the peer has the file, it will return its ip address (temp[0])
            # and its port number (temp[1]). If not found, the peer will return ' '
            data = sock.recv(5000)
            temp[0] = data.decode('UTF-8')

            data = sock.recv(5000)
            temp[1] = data.decode('UTF-8')

            # information for the next peer to connect to

            data = sock.recv(5000)
            temp2[0] = data.decode('UTF-8')

            data = sock.recv(5000)
            temp2[1] = data.decode('UTF-8')

            data = sock.recv(5000)
            temp2[2] = data.decode('UTF-8')

            # check if file is found
            if (temp[0] != ' ') and (temp[1] != ' '):
                
                print('File found at ')
                print('IP Address: %s' % temp[0])
                print(' Port Number: %s' % temp[1])
                
            TTL = int(TTL) - 1

            # connect to the ip address and port number this peer provided of the peer
            # it knows about
            if (temp2[0] != peerName) and (TTL != 0):

                TTL = handleSEARCH(temp2[1], temp2[2], filename, str(TTL))
                
            return TTL
            
    # look for new peers and add to the list of known peers
    def handleDISCOVER(self,ipAddress, portNumber, TTL):

        connectSocket(ipAddress, portNumber,'DISCOVER')
        # send information to the peer on how far to look
        sock.sendall(bytes(TTL, 'UTF-8'))
        
        while int(TTL) != 0:
            
            temp = [0, 0, 0]
            temp2 = [0, 0, 0]
            
            data = sock.recv(5000)
            temp[0] = data.decode('UTF-8')
            
            data = sock.recv(5000)
            temp[1] = data.decode('UTF-8')
            
            data = sock.recv(5000)
            temp[2] = data.decode('UTF-8')
            
            # information for the next peer to connect to
             
            data = sock.recv(5000)
            temp2[0] = data.decode('UTF-8')
            
            data = sock.recv(5000)
            temp2[1] = data.decode('UTF-8')
            
            data = sock.recv(5000)
            temp2[2] = data.decode('UTF-8')
            
            # check if we already know this peer
            
            match_found = 0

            for peer in knownPeers:

                if peer == temp[0]:

                    match_found = 1

            # if we discover a new peer, add to list
            
            if match_found == 0:
                
                knownPeers.append(temp)
                
            TTL = int(TTL) - 1

            # we search untill TTL is 0, or untill we circle back to ourself
            
            if (temp2[0] != peerName) and (TTL != 0):
                
                TTL = handleDISCOVER(temp2[1],temp2[2], str(TTL))
                
            return TTL

    # request a specific file from a peer
    def handleGET(self,ipAddress, portNumber, fileName):

        connectSocket(ipAddress, portNumber,'GET')

        time.sleep(1)
        sock.sendall(bytes(fileName, 'UTF-8'))
        time.sleep(1)

        receiveFile()
    
    # method responsible for receiving the file and saving it
    def receiveFile(self):

        # open file to write to, in binary format
        f1 = open('RECEIVED_FILE', 'wb')
        print ('Creating and opening file RECEIVED_FILE ')
        
        i = 1
        sumBytes = 0
        
        # Receive the file in small chunks of data and write it to RECEIVED_FILE
        # set data to initial value 
        data = b'9999'
        size = 0

        while data:
            
            data = sock.recv(5000)

            #
            if data:
                
                # check to see if the data chunk is about to send the size of the file
                # if so, the next data received is the size of the file
                
                if 'size' in data.decode('cp866', 'replace'):
                    
                    data = sock.recv(5000)
                    size = data.decode()
                    
                # checks to see if the file was not found
                
                if data != bytes('File not found','UTF-8'):
                    
                    # if received data, then write data to the RECEIVED_FILE file
                    
                    f1.write(data)
                    i = i + 1
                    sum_bytes = sum_bytes + len(data)
                    
                    print (' Received chunk ', i ,' with ', len(data), ' bytes ',
                          ' total bytes = ', sumBytes)
                else:
                    
                    print ('File not found')
            else:
                
                print ('Received line with no data')
                print ('Total bytes = ', sumBytes)
                
        print ' '
        print 'Received file with ', sum_bytes, ' bytes ', 'Closing RECEIVED_FILE file..'
        

    
        
        
