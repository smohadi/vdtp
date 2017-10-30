# Client module
import socket
import pickle
# Required functions
# Send_packet
# Receive_packet
# Construct_packet
#

# Fragment Data into chunks of 1000 bytes
def fragmentData(serialData):
    if len(serialData) > 1000:
        retBuf = []
        current = 0
        while current < len(serialData):
            retBuf.append(serialData[current:current+1000])
            current += 1000
    else:
        retBuf = [serialData]
    return retBuf
def createBasicPacket():
    return
def send(data,sk):
    serialData = pickle.dumps(data)

    # Create a basic packet
    #basicData = createDataPacket()

    # Combine basicData and serialData
    # cData = combineData(basicData,serialData)

    # Fragment application layer packet to 1000 byte chunks
    #fragDataList = fragmentData(basicData,serialData)

    # Attach header to individual messages
    # Send individual messages
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sk.sendto(serialData,addr)

