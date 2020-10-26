#!/usr/bin/python
import socket
from time import sleep
from gpiozero import Button
import configparser

# 'button' is our LARGE button, on GPIO2 (i.e. pin 3)
button = Button(2)

'''
	TODO:
		* Read IP addr/port from config file
'''

def send_server_command():
	print(f'\tSending code to server.')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# FIXME!
	s.connect((TCP_IP, TCP_PORT))
	s.send('dstp\n')
	data = s.recv(1024)
	s.close()
	

if __name__ == '__main__':
	config = configparser.RawConfigParser()
	x = config.read(cvar.CONFIG_FILENAME)
    	if len(x)>0:
		else:
			print("button.py couldn't read config file")
	# https://gpiozero.readthedocs.io/en/stable/recipes.html
	button.when_pressed = send_server_command
