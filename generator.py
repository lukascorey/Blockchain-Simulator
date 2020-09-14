#!/usr/bin/env python3
import json
import secrets
import hashlib
import time
import socket
import _thread

# Recognize complexity of question, all things can be argued both ways. Take a position and stick but counterargue and mention major arguments against. 
# Describe several mechanisms, use real world examples from class, readings, etc... 
# Make sure answer is appropriate 
# 2 lectures before break and everything after 
# MC 15 questions most T/F, gonna get practice questions
#
#
#
#
#


'''
Network

Constructor
'''
class Network():


    '''
    ___init___

    initialize the blockchain network

    - { int } difficulty - the proof of work difficulty in the network

    returns None (implicit object return)
    '''
    def __init__( self, difficulty ):
        self.chain      = []
        self.difficulty = 4
        self.directory = []


    '''
    add_block

    add a block to the chain

    - { Block } block - block to add

    returns Bool
    '''
    def add_block( self, block ):
        time.sleep(.1)
        # if genesis block, just add directly
        if len( self.chain ) == 0 and block.index == 0:
            self.chain.append( block )
            print("block accepted")
            return True

        # check that new block is valid and child of current head of the chain
        if self.validate( block, self.chain[ -1 ] ):
            self.chain.append( block )
            print("block accepted")    
            return True

        # if was not the genesis block and could not be validated, then print that it was rejected
        print("block rejected")
        return False

    # adds a port into the directory    
    def add_node(self, port): 
        self.directory.append(port)

    '''
    validate

    validate the correctness of a block

    - { Block } block  - block to be checked
    - { Block } parent - parent block to be checked against

    returns Bool
    '''
    def validate( self, block, parent ):
        
        # block has index, parent_hash, data, hashed, timestamp, nonce, hash
        # TODO: Validate whether a received block is legitimate. You'll need five different checks here.
        #   1. Has something to do with the timestamp.
        valid = 1
        starting_string = ""
        if block.index != 0:
            if block.timestamp <= parent.timestamp:
                valid = 0
            #   2. Has something to do with the hash.
            
            for i in range(int(network.difficulty)): 
                starting_string = starting_string + "0"
            calculated_hash = (hashlib.sha256((str(block.index) + str(parent.hash) + str(block.timestamp) + str(block.nonce)).encode())).hexdigest()
            if (not ( calculated_hash.startswith(starting_string) )):
                valid = 0
            #   3. Has something else to do with the hash.
            if (not (str(calculated_hash) in str(block.hash))): 
                valid = 0
            #   4. Has something to do with the parent.
            if (not (parent.index == block.index - 1)):
                valid = 0
            #   5. Has something else to do with the parent
            if (not (str(parent.hash) in str(block.parent_hash))): 
                valid = 0
            return (valid == 1) # a boolean denoting whether the block is valid

        else: 
            #if it is the genesis node, we cannot check the parent. instead, we only check the hash
            for i in range(int(network.difficulty)): 
                starting_string = starting_string + "0"
            calculated_hash = (hashlib.sha256((str(block.index) + str(block.parent_hash) + str(block.timestamp) + str(block.nonce)).encode())).hexdigest()
            if (not ( calculated_hash.startswith(starting_string) )):
                valid = 0
            if (not (str(calculated_hash) in str(block.hash))): 
                valid = 0
            return (valid == 1)



    '''
    validate_chain

    validate the correctness of the full chain

    returns Bool
    '''
    def validate_chain( self ):
        # TODO: Validate whether the the full chain is legitimate (whether each block is individually legitimate).
        valid = 1

        #iterates over entire chain
        for i in range((len(self.chain))):
            if i  == 0: 
                if (not (self.validate(network.chain[0], "none"))):
                    valid = 0
            else: 
                if (not (self.validate(network.chain[i], network.chain[i-1]))): 
                    valid = 0
        return (valid == 1) # a boolean denoting whether the chain is valid



    '''
    serialize

    serialize the chain into a format for sharing over the wire

    returns String or Bytes
    '''
    def serialize( self ):
        dump = {}
        # TODO: Come up with a way to encode the full chain for sharing with new nodes who join the network. JSON may be useful here.
        for i in range(len(self.chain)):

            #put information for each block into a dict 
            my_dict = {}
            my_dict["index"] = self.chain[i].index
            my_dict["hash"] = self.chain[i].hash
            my_dict["hashed"] = self.chain[i].hashed
            my_dict["parent_hash"] = self.chain[i].parent_hash
            my_dict["timestamp"] = self.chain[i].timestamp
            my_dict["nonce"] = self.chain[i].nonce
            my_dict["data"] = self.chain[i].data

            #put dict into a dictionary of blocks
            dump[i] = (my_dict)

        #run json dumb on dict of dicts     
        ultra_dump = json.dumps(dump)
        return ultra_dump # a string or bytestring


    '''
    deserialize

    deserialize the chain from the wire and store

    returns None
    '''
    def deserialize( self, chain_repr ):
        # TODO: Reverse the behavior of serialize.

        #run json loads on on string 
        load = json.loads(chain_repr)
        #empty chain
        self.chain = []

        #iterate through dictionaries in the dictionary, each represents one block
        for i in load:
            block = Block(load[i]["index"], load[i]["parent_hash"], load[i]["data"])
            block.index = load[i]["index"]
            block.hash = load[i]["hash"]
            block.hashed = load[i]["hashed"]
            block.parent_hash = load[i]["parent_hash"]
            block.timestamp = load[i]["timestamp"]
            block.nonce = load[i]["nonce"]
            block.data = load[i]["data"]

            #put each block into the chain, they are in order from the dict     
            self.chain.append(block)        
        return None


    '''
    __str__

    string representation of the full chain for printing

    returns String
    '''
    def __str__( self ):
        sc = '\nNo. of Blocks: {l}\n'.format( l = len( self.chain ) )

        offset = len( str( len( self.chain ) ) )
        for i, block in enumerate( self.chain ):
            sc += '\tBlock {n}. {h}\n'.format( n = str( i ).rjust( offset ), h = str( block ) )

        sc += '\n'

        return sc


'''
Block

Constructor
'''
class Block():


    '''
    ___init___

    initialize a block

    - { int } index  - the block index in the chain
    - { str } parent - the hash of the parent block
    - { str } data   - the data to be inserted into the block

    returns None (implicit object return)
    '''
    def __init__( self, index, parent, data ):
        self.index       = index
        self.parent_hash = parent
        self.data        = data  # NB: You're welcome to put anything or nothing into the chain.

        self.hashed      = False


    '''
    hash

    mine a (valid) hash for the block

    - { int } difficulty - the difficulty to be met, from the network

    returns String
    '''
    def hash( self, difficulty ):
        # TODO: Implement hashing of block until difficulty is exceeded.
        #       Use the SHA256 hash function (from hashlib library).
        #       The hash should be over the index, hash of parent, a unix epoch timestamp in elapsed seconds (time.time()), a random nonce (from secrets library) and the data.
        #       We will refer to all of these contents except the data as a "header".
        #       It is recommended that you store and use the hex representation of the hash, from hash.hexdigest().
        #
        # HINTS
        #
        #       "[U]ntil difficulty is exceeded" means at least the specified number of leading zeros are present in the
        #       hash as the "proof of work." You'll have to keep hashing with different nonces till you get one that works.
        #
        #       You may query the random nonce once and increment it each try.

        # set variables 
        index = self.index
        parent_hash = self.parent_hash

        #create starting string of 0s to test hash
        starting_string = ""
        for i in range(int(network.difficulty)): 
            starting_string = starting_string + "0"

        hash_string = ""

        # hash until hash_string starts with the right number of 0s
        while (not (str(hash_string).startswith(starting_string))):
            time_stamp = time.time()
            nonce = int(secrets.token_hex(), 16)
            hash_string = (hashlib.sha256((str(index) + str(parent_hash) + str(time_stamp) + str(nonce)).encode())).hexdigest()

            

        #set the correct timestamp, nonce, and hash
        self.timestamp = time_stamp
        self.nonce     = nonce
        self.hash      = hash_string

        #set hashed to true 
        self.hashed = True

        return self.hash


    '''
    __str__

    string representation of the block for printing

    returns String
    '''
    def __str__( self ):
        return self.hash


'''
generate

generate (mine) a new block

TODO: Determine input(s) and output(s).
'''
def generate(parent_block):
    #just need parent block to generate new one, 
    block = Block((parent_block.index + 1), parent_block.hash, 'New Block' ) 

    #hash with network difficulty 
    block.hash( network.difficulty)
    return block


'''
genesis

generate (mine) the genesis block

returns None
'''
def genesis():
    genesis = Block( 0, 'none', 'Genesis Block' )
    genesis.index = 0
    genesis.parent_hash = "none"
    genesis.hash( network.difficulty )
    network.add_block( genesis )

    return None


'''
broadcast

broadcast mined block to network

TODO: Determine input(s) and output(s).
'''
def broadcast(block):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORTS = network.directory        # Port to listen on (non-privileged ports are > 1023)

    #put block into dictionary
    my_dict = {}
    my_dict["index"] = block.index
    my_dict["hash"] = block.hash
    my_dict["hashed"] = block.hashed
    my_dict["parent_hash"] = block.parent_hash
    my_dict["timestamp"] = block.timestamp
    my_dict["nonce"] = block.nonce
    my_dict["data"] = block.data

    #make string with json
    dump = json.dumps(my_dict)
    #iterate through other ports to send to
    for port in PORTS: 

        #make socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            s.send(dump.encode('utf-8'))
            
    # TODO: Broadcast newly generated block to all other nodes in the directory.
    pass


'''
query_chain

query the current status of the chain

TODO: Determine input(s) and output(s).
'''
def query_chain():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORTS = network.directory       # Port to listen on (non-privileged ports are > 1023)
    chains = {}
    loads = {}
    longest_chain = 0

    #iterate through directory
    for port in PORTS: 

        #connect to socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            print("requesting chain")
            s.send("requesting chain".encode('utf-8'))

            # put the string and dictionary into loads and chains respectively, indexed by port
            loads[port] = (s.recv(4096).decode('utf-8'))
            chains[port] = json.loads(loads[port])

            #keep track of longest dictionary port value 
            if longest_chain == 0: 
                longest_chain = port
            elif (len(chains[longest_chain]) < (len(chains[port]))):
                longest_chain = port

    #deserialize the longest chain and make the network chain            
    network.deserialize(loads[longest_chain])

    #if we got a messed up chain, reject it and set to empty 
    if (not (network.validate_chain())):
        network.chain = []

    pass


'''
listen_broadcast

listen for broadcasts of new blocks

TODO: Determine input(s) and output(s).
'''
def listen_broadcast(socket):
    

    c, addr = socket.accept()
    # wait for message to be sent 
    while True:
        msg = c.recv(4096)
    #checks if message has been received, only runs following code upon submission of a vote
        if msg:

            #turns message into utf-8 
            msg = msg.decode('utf-8')

            msg = json.loads(msg)
        
            #print(msg)
            #clientsocket.send("received".encode('utf-8'))

            #break out of while loop 
            break

    #Close connection
    #socket.close()

    # take information out of dictionary and put into block
    block = Block(msg['index'], msg['parent_hash'], msg['data'])
    block.index = msg['index']
    block.hash = msg["hash"]
    block.hashed = msg["hashed"]
    block.parent_hash = msg["parent_hash"]
    block.timestamp = msg['timestamp']
    block.nonce = msg['nonce']
    block.data = msg['data']
  
    return block



'''
listen_query

list for requests for current chain status

TODO: Determine input(s) and output(s).


         
'''
def listen_query(socket):
    c, addr = socket.accept()
    while True:
        msg = c.recv(4096)
    #checks if message has been received, only runs following code upon submission of a vote
        if msg:

            #turns message into utf-8 
            msg = msg.decode('utf-8')
            print("got message: " + msg)
            if ("requesting chain" in msg): 
                time.sleep(.5)
                c.send((network.serialize()).encode('utf-8'))
                return True
            #break out of while loop 
            break
    return False





if __name__ == '__main__':
    # hoist the network up to the global context
    # makes it easier to use with both tcp/http

    global network
    network = Network( 4 )
    network.add_node(65431) #honest
    network.add_node(65430) #dishonest 

    s = socket.socket()
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    #listens for two connections 
    s.bind((HOST, PORT))
    s.listen(20)
    genesis()
    #print("made genesis block")
    broadcast(network.chain[0])
    #listen for honest block
    print("listening for honest")
    network.add_block(listen_broadcast(s))
    print("listening for dishonest")
    #dishonest node trying to create, wont work
    network.add_block(listen_broadcast(s))
    print("listening for honest2")
    #honest node trying to create, should work
    network.add_block(listen_broadcast(s))

    network.add_node(65429)
    print("listening for query")
    listen_query(s)

    
    print(network)
    if (network.validate_chain()):
        print("blockchain has been validated")
    else: 
        print("blockchain not valid")
    s.close()

        
