#!/usr/bin/python
import socket
import configparser
import platform
from time import sleep

import common_vars as cvar

global button
if platform.system().lower() != "windows":
	from gpiozero import Button, PWMLED
	# 'button' is our LARGE button, on GPIO15 (i.e. pin 10)
	button = Button(15)
	# 'button_led' is our LARGE button's built-in, on GPIO2 (i.e. pin 3)
	button_led = PWMLED(2)


global server_addr, server_port, press_count

def send_server_command():
	global press_count
	press_count += 1
	print(f'Sending code to server.')
	print(f'\t{server_addr} : {server_port}')
	print(f'\tpress count: {press_count}')
	
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.connect((server_addr, int(server_port)))
	#s.send('dstp\n')
	#data = s.recv(1024)
	#s.close()
	

if __name__ == '__main__':
	print("Running Button.py")
	config = configparser.RawConfigParser()
	x = config.read(cvar.CONFIG_FILENAME)
	global press_count
	press_count = 0
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
		if platform.system().lower() != "windows":
			for b in range(100):
				button_led.value = b / 100
				sleep(0.1)
			for b in range(100,1):
				button_led.value = b / 100
				sleep(0.1)
		#print("button loop")
		sleep(3)
