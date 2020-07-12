# UDPPingerServer.py
import random
import time
from socket import *
# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', 12000))
print("The server is Ready")
while True:
 # Generate random number in the range of 0 to 10
 rand = random.randint(0, 10)
 # Receive the client packet along with the address it is coming from
 message, address = serverSocket.recvfrom(1024)

 message = message.upper()
 msg = message.decode("utf-8").split(" ")
 time1 = time.localtime(float(msg[2])) 
 print("Receive: " + msg[0] +' ' + msg[1] + ' ' + time.strftime("%I:%M:%S", time1))
 # If rand is less is than 4, we consider the packet lost and do not respond
 if rand < 4:
   continue
 # Otherwise, the server responds
 serverSocket.sendto(message, address)
 print("Sent: " + msg[0] + ' ' + msg[1] + ' ' + time.strftime("%I:%M:%S", time1))
