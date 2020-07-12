from socket import *
import socket 
import time
from functools import reduce
 
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
num_pings = 10

sequence_number = 1

while sequence_number <= num_pings:
	send_time = time.time()
	#t = time.strftime("%I:%M:%S", send_time)
	message = 'PING ' + str(sequence_number) + ' ' + str(send_time) 
	em = str.encode(message)
	clientSocket.sendto(em,(serverName, serverPort))
	clientSocket.settimeout(1.0)
	try:
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		rtt = round(time.time() * 1000 - send_time * 1000, 3)
		msg_len = len(modifiedMessage)
		msg = modifiedMessage.decode("utf-8").split(" ")
		print(str(msg_len) + " bytes " + "from " + serverName + ":" + str(serverPort) + ' ' + "seq=" + msg[1] + " rtt=" + str(rtt))
	except socket.timeout:
		print("Request timed out")
	sequence_number = sequence_number + 1
clientSocket.close()
