import os
import sys
import argparse
import pcap
import dpkt
import socket
import binascii
from construct import *
from subprocess import call
from dpkt.compat import compat_ord


#From the dpkt site
def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)

#From the dpkt site    
def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


#Parse then print the packet data
def print_packet(raw_data):
	if not raw_data:
		return

            try:
                ether_packet = dpkt.ethernet.Ethernet(raw)
                print("Ethernet info: ", mac_addr(ether_packet.src), mac_addr(ether_packet.dst))
            except:
                print("Not Ethernet")

	except(dpkt.dpkt.NeedData,dpkt.dpkt.UnpackError):
		return
	

         ip = ether_packet.data
         if isinstance(ip , dpkt.ip.IP):
             #print("IP: from %s to %s " % (inet_to_str(ip_packet.src), inet_to_str(ip_packet.dst)))
             # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
	    do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
	    more_fragments = bool(ip.off & dpkt.ip.IP_MF)
	    fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
	
	    #print the ip info
	    print('IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
	    (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))
        else:
            return
	

        
	if isinstance(ip.data , dpkt.tcp.TCP):
		#get the tcp data
                tcp = ip.data
		
		
		#print the tcp data
		print('TCP: (src port=%d dest port=%d seqnum=%d ACK=%d flags=%d)\n' % (tcp.sport, tcp.dport, tcp.seq, tcp.ack, tcp.flags))
		

		
		#check if its HTTP from machine to server, i.e., a request
		
		if (tcp.dport == 80) and len(tcp.data) > 0:
			#unpack the HTTP request packet
			try:
				#Print The HTTP Data: URL, Method, and Headers
                                
				http= dpkt.http.Request(tcp.data)
				print('************************HTTP Request Packet Data***********************\n')
				print(http.headers)
				print(http.uri)
				print(http.method) 
			except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
				print('Could not unpack HTTP Request data')
		else:
			if tcp.sport== (80 or 443) and len(tcp.data) > 0:
				#unpack the HTTP response packet
				try:
					http=dpkt.http.Response(tcp.data)
					print('************************HTTP Response Packet Data***********************\n')
					print(http.headers)
				except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
					print('Could not unpack HTTP Response data')
			else:
				#Just print the TCP packet raw data
				print('**************TCP PACKET DATA***************************\n')
				print(tcp.data)
				print('****************************************************\n')
		
			
		

	if isinstance(ip.data, dpkt.udp.UDP):
		#get the udp data
		udp = ip.data
		#print the UDP data: src and dest port
		print('UDP: (src port=%d dest port=%d )\n' % (udp.sport, udp.dport))
		#now print the rest of the packt data
		print('**************UDP PACKET DATA***************************\n')
		print('%s \n' %binascii.b2a_qp(udp.data, True, True, True))
		print('****************************************************\n')
		
def main():

	out_p = "Should I enter monitor mode? %s or %s: " % ('n', 'y')
	testcase=True
	monmode=False
	
	while testcase:
		userinput=input(out_p)
		if userinput not in ['Y', 'y', 'N', 'n']:
			print("Please answer Y (yes) or N (no) ")
			continue
		if userinput == 'Y' or userinput =='y':
			monmode=True
			testcase=False
		if userinput =='N' or userinput =='n':
			monmode=False
			testcase=False

	pcapobj = pcap.pcap(name=None, promisc=True, immediate=True)
	print('Press CTRL+C to end capture')

	try:
		for timestamp, raw_buf in pcapobj:
			print_packet(raw_buf)
	except KeyboardInterrupt:
		print('packet statistics: %d packets received, %d packets dropped, %d packets dropped by the interface' %pcapobj.stats())
		
if __name__ == '__main__':
	main()

