#!/usr/bin/python
import socket
import configparser
import platform
from time import sleep

import common_vars as cvar

global button
if platform.system().lower() != "windows":
	from gpiozero import Button
	# 'button' is our LARGE button, on GPIO2 (i.e. pin 3)
	button = Button(2)


'''
	TODO:
		* Read IP addr/port from config file
'''

global server_addr, server_port

def send_server_command():
	print(f'\tSending code to server.')
	print(f'{server_addr} : {server_port}')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server_addr, int(server_port)))
	s.send('dstp\n')
	data = s.recv(1024)
	s.close()
	

if __name__ == '__main__':
	print("Running Button.py")
	config = configparser.RawConfigParser()
	x = config.read(cvar.CONFIG_FILENAME)
	if len(x)>0:
		print("button.py read the config")
		server_addr = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_ADDR]
		server_port = config[cvar.CONFIG_SECTION][cvar.CONFIG_SERV_PORT]
	else:
		print("button.py couldn't read config file")
	# https://gpiozero.readthedocs.io/en/stable/recipes.html
	if platform.system().lower() != "windows":
		button.when_pressed = send_server_command
	while(True):
		print("button loop")
		sleep(10)
