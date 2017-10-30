import socket
import pickle

soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 5050

soc.bind((LOCAL_IP,LOCAL_PORT))

while True:
	data,addr = soc.recvfrom(1024)
        recvData = pickle.loads(data)
        print addr,":",recvData
