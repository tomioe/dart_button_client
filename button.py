#!/usr/bin/python
import socket
from time import sleep
from gpiozero import Button

# should match IP running server
TCP_IP = '192.168.0.2'
TCP_PORT = 5001
BUFFER_SIZE = 1024

# 'button' is our LARGE button
button = Button(2)


def SendCommandToHost(code):
	print "\tSending %s to server."%code
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(code+"\n")
	data = s.recv(BUFFER_SIZE)
	s.close()
	
while True:
	while True:
		if button.is_pressed:
			SendCommandToHost('dstp')
			sleep(3)
		
		sleep(0.3)
