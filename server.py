import socket
import pickle
import struct
import vdtp

LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 5050

while True:
    output,addr = vdtp.recv_sock((LOCAL_IP,LOCAL_PORT))
    print 'Server Output:',output['a']
    print 'Client Address:',addr

