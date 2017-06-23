# The IncomingRequests class deals with all incoming requests from other peers

class IncomingRequests:
    
    # send back all available files for sharing
    def handleLISTR(self,socket, availableFiles):

        for File in availableFiles:

            socket.request.sendall(bytes(File, 'UTF-8'))
            
    # search for the requested file and send back if this peer has it, if not send back information of the next peer to look to
    def handleSEARCH(self,socket, ip_address, port_number, availableFiles, knownPeers):

        # receive the file name
        data = socket.request.recv(1024)
        fileName = data.decode('UTF-8')

        # receive the TTL
        data = socket.request.recv(1024)
        TTL = data.decode('UTF-8')

        for File in availableFiles:

            if File == fileName:

                fileFound = 1

                break
            
        # if we have the file, let the original peer know
        if fileFound == 1:

            time.sleep(1)
            socket.request.sendall(bytes(ip_address, 'UTF-8'))
            time.sleep(1)
            socket.request.sendall(bytes(port_number, 'UTF-8'))
            time.sleep(1)
            
        # if we do not have the file, send them a blank space
        else:

            time.sleep(1)
            socket.request.sendall(bytes(' ','UTF-8'))
            time.sleep(1)
            socket.request.sendall(bytes(' ','UTF-8'))
            time.sleep(1)

        # send back information of all known peers, along with their information

        socket.request.sendall(bytes(knownPeers[0][0], 'UTF-8'))
        time.sleep(1)
        socket.request.sendall(bytes(knownPeers[0][1], 'UTF-8'))
        time.sleep(1)
        socket.request.sendall(bytes(knownPeers[0][2], 'UTF-8'))
    
    # send back this peers' information, as well as the peers it knows
    def handleDISCOVER(self,socket, peerName, ip_address, port_number, knownPeers):

        data = socket.request.recv(1024)
        TTL = data.decode('UTF-8')

        # send this user's information
        socket.request.sendall(bytes(peerName, 'UTF-8'))
        time.sleep(1)
        socket.request.sendall(bytes(ip_address, 'UTF-8'))
        time.sleep(1)
        socket.request.sendall(bytes(port_number, 'UTF-8'))
        time.sleep(1)

        # also send back information of the peer it knows about
        socket.request.sendall(bytes(knownPeers[0][0], 'UTF-8'))
        time.sleep(1)
        socket.request.sendall(bytes(knownPeers[0][1], 'UTF-8'))
        time.sleep(1)
        socket.request.sendall(bytes(knownPeers[0][2], 'UTF-8'))
    
    # send back the requested file
    def handleGET(self,socket, fileName):

        # receive the name of the file to get
        data = socket.request.recv(1024)
        filename = data.decode('UTF-8')

        sendFile(socket, fileName)
    
    # handles the responsibility of sending a file to a peer. Ex. opening file, encoding, etc.
    def sendFile(self,socket, fileName):

        # open file in binary read mode
        
        f1 = open(fileName, 'rb')
        
        i = 1
        
        sumBytes = 0

        # go through every line in file and send the line over the socket
        for line in f1:
            
            sock.request.sendall(line)
            i = i+1
            sum_bytes = sum_bytes + len(line)

        f1.seek(0, os.SEEK_END)
        size = f1.tell()
        f1.close()
