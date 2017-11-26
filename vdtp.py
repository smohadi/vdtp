# Client module
import socket
import pickle
from random import *
import struct
import time
seqSent = []
# Required functions
# Send_packet
# Receive_packet
# Construct_packet



# flowId    - 8 bits
# seq       - 6 bits
# reliable  - 1 bits
# lastFrag  - 1 bit
# data   - 1450 bytes (max)

# Fragment Data into chunks of 1000 bytes
def fragmentData(serialData,reliable):
    FRAG_SIZE = 1450
    flowId = randint(1,255)
    print 'Flow Id:',flowId
    if len(serialData) > FRAG_SIZE:
        print "Fragmenting Data"
        retBuf = []
        current = 0
        seq = 0
        lastFrag = 0
        while current < len(serialData):
            if current + FRAG_SIZE > len(serialData):
                lastFrag = 1
            if seq > 63:
                seq = 0
            #print seq,lastFrag
            seqHdr = (seq<<2) + (reliable << 1) + lastFrag
            #print seqHdr
            header = struct.pack('BB',flowId,seqHdr)
            retBuf.append(header + serialData[current:current+FRAG_SIZE])
            current += FRAG_SIZE
            seq += 1
    else:
        header = struct.pack('BB',flowId,reliable << 1 + 1)
        #print len(header)
        retBuf = [header + serialData]
    return retBuf

def ackthread(ack,addr,sk):
    ackData = pickle.dumps(ack)
    ackList = fragmentData(ackData,1)
    for item in ackList:
        sk.sendto(item,addr)
    ack = []
    return 0

def retransmission(ackRcv,addr,sk)
    for i in range(len(ackRcv)):
        if ackRcv[i] in seqSent:
            seqSent.remove(ackRcv[i])
    
    return 0

def send(data,addr,reliable=0):
    
    serialData = pickle.dumps(data)
    print 'Original Data Length:',len(serialData)

    # Fragment application layer packet to 1000 byte chunks
    fragDataList = fragmentData(serialData,reliable)
    
    
    flowId,seq,reliable,lastFrag = extractHeader(data[0:2])
    Global seqSent = seqSent.append(seq)

    # Attach header to individual messages
    # Send individual messages
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # Create ackThread for reliability
    #if reliable == 1:
        #ackThread(fragDataList,sk)

    for item in fragDataList: 
        print 'Item Length:',len(item)
        sk.sendto(item,addr)

def extractHeader(hdr):

    flowId = struct.unpack('B',hdr[0])
    flowId = flowId[0]

    seqHdr = struct.unpack('B',hdr[1])
    seqHdr = seqHdr[0]
    lastFrag = seqHdr & 1
    reliable = (seqHdr >> 1) & 1
    seq = (seqHdr >> 2) & 1
    return flowId,int(seq),reliable,lastFrag

def recv_sock(addr):

    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ackSk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sk.bind(addr)
    output = ''
    flowIdList = {}   
    close_time=time.time()+0.2 ###for 200 msec delay 
    ack = []

    while True:
        data,addr = sk.recvfrom(1500)
        length = len(data)
        #print length
        flowId,seq,reliable,lastFrag = extractHeader(data[0:2])
        ack.append(seq)
        
        if reliable==1:
            if flowIdList.has_key((addr,flowId)):
                flowIdList[(addr,flowId)][seq] = data[2:length]
            else:
                flowIdList[(addr,flowId)] = {}
                flowIdList[(addr,flowId)][seq] = data[2:length]

            if lastFrag == 1:
                for x in range(0,64):
                    if flowIdList[(addr,flowId)].has_key(x):
                        output += flowIdList[(addr,flowId)][x]
                    else:
                        del flowIdList[(addr,flowId)]
                        break
                returnBuf = pickle.loads(output) 
                
        retransmission(returnBuf,addr,sk)
            
        else
        # In order delivery
            if flowIdList.has_key((addr,flowId)):
                flowIdList[(addr,flowId)][seq] = data[2:length]
            else:
                flowIdList[(addr,flowId)] = {}
                flowIdList[(addr,flowId)][seq] = data[2:length]

            if lastFrag == 1:
                for x in range(0,64):
                    if flowIdList[(addr,flowId)].has_key(x):
                        output += flowIdList[(addr,flowId)][x]
                    else:
                        del flowIdList[(addr,flowId)]
                        break
                returnBuf = pickle.loads(output)
                output = ''
                return returnBuf,addr
            if time.time()>close_time:
                ackthread(ack,addr,sk)



