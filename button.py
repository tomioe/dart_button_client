#!/usr/bin/python
import socket
import configparser
import platform
from time import sleep

import common_vars as cvar

'''
	TODO:
	* Long press for config reset (clear cvar and just return)
	* Enable the LED and start pulsing
'''




global server_addr
global server_port
global press_count

# def send_server_command():
# 	global press_count
# 	press_count = press_count + 1
# 	print(f'Sending code to server.')
# 	print(f'\t{server_addr}: {server_port}')
# 	print(f'\tpress count: {press_count}')
	
# 	dartServerAddress = (server_addr, int(server_port))
# 	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# 		s.connect(dartServerAddress)
# 		s.sendall("dstp\n".encode('utf-8'))
# 		response = s.recv(1024)
	

global button
if platform.system().lower() != "windows":
	from gpiozero import Button, PWMLED

	# 'button' is our LARGE button, on GPIO15 (i.e. pin 10)
	button = Button(15)

	# 'button_led' is our LARGE button's built-in, on GPIO2 (i.e. pin 3)
	button_led = PWMLED(2)

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

	# set GPIO
	while(True):
		if platform.system().lower() != "windows":
			for a in range(1,100,2):
				print(a)
				# button_led.value = b / 100
				sleep(0.02)
			for b in range(100,1,-2):
				print(b)
				# button_led.value = b / 100
				sleep(0.02)
		#print("button loop")
		sleep(2)
