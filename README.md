# Peer-to-Peer-Program
A Peer-to-Peer program written in Python using threading, socket programming, object oriented programming.

Commands:

  LISTL - Lists all the files the peer is willing to share.
  
  RESET - Resets the list of known peers back to just the first peer it knew.
  
  LISTR - Request all the files another peer is willing to share.
  
  SEARCH - Search for a file by connecting to the first peer, and then connecting to all the other peers. Returns back a list of all
           the peers that have the file.
           
  DISCOVER - Search for new peers and store the information into the list of known peers.
  
  GET - Request a specific file from a peer.
  
This program can be used on a single computer by running multiple instances of the peer2peer.py file, however each instance must have different client information, specifically, the section of code below:

    client = Client('Alex', 'localhost', '2002')

    client.addPeer(['Robert','localhost','2000']) 

    client.addFile('logo1.png')

An example would be using the following client set up for three instances.

FIRST PEER (ALEX):

    client = Client('Alex', 'localhost', '1000')

    client.addPeer(['Sally','localhost','1001']) 

    client.addFile('logo1.png')
    
SECOND PEER (SALLY):

    client = Client('Sally', 'localhost', '1001')

    client.addPeer(['Robert','localhost','1002']) 

    client.addFile('logo2.png')
    
THIRD PEER (ROBERT):

    client = Client('Robert', 'localhost', '1002')

    client.addPeer(['Alex','localhost','1000']) 

    client.addFile('logo3.png')
    
If you wish to run this on separate computers, you simply need to change the ip address when setting up the client from 'localhost' to
the ip address of the computer it's running on.


