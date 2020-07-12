import argparse
import sys, time
from socket import *
import socket

"""
Modified by Pratima Kandel
UDP/TCP Port Scanner
""" 

def scan_ports(host, start_port, end_port, protocol):
    #setup
	print("Scanning: " + host +" From port: " +str(start_port) +" To Port: " +str(end_port))

    #Set the IP
	remote_ip=host
    #Scan Ports	
	for port in range(start_port, end_port+1):
		#TCP port scanner
		if(protocol == "TCP"):
			try:
				socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
				result = socket1.connect_ex((remote_ip, port))
				socket1.settimeout(1.0)
				if result == 0:
					print("Port Open: " + str(port))
				else:
					print("Port Not Open", port)
				socket1.close()
			except socket.error:
				print("Couldn't connect to server")
			except socket.timeout:
				print("Timed out")
				
    
		else:
			#UDP port scanner
			try:
				socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			except socket.error:
				print("Couln't connect to serevr")
			message = 'PING ' + str(0) + ' ' + str(time.time())
			em = str.encode(message)
			socket1.sendto(em,(remote_ip, port))
			socket1.settimeout(1.0)
			try:
				modifiedMessage, serverAddress = socket1.recvfrom(2048)
				print("Port Open:", port)
			except socket.timeout:
				print("Request Timed out - Port not open")		
                
#parsing stuff you dont have to change
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Remote Port Scanner')
    parser.add_argument('--host', action="store", dest="host", default='127.0.0.1')
    parser.add_argument('--start-port', action="store", dest="start_port", default=1, type=int)
    parser.add_argument('--end-port', action="store", dest="end_port", default=100, type=int)
    parser.add_argument('--protocol', action="store", dest="protocol", default="TCP")
#parse args
    given_args = parser.parse_args()
    host, start_port, end_port, protocol = given_args.host, given_args.start_port, given_args.end_port, given_args.protocol
    scan_ports(host, start_port, end_port, protocol)
