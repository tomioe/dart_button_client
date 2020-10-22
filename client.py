#!/usr/bin/python
import socket
from time import sleep
from gpiozero import Button
from matrix_keypad import RPi_GPIO

# should match IP running server
TCP_IP = '192.168.0.2'
TCP_PORT = 5001
BUFFER_SIZE = 1024

# 'button' is our LARGE button
button = Button(2)

kp = RPi_GPIO.keypad(columnCount = 4)
digit = None

attempt = "0000"
passcode = "1912"
counter = 0


def SendCommandToHost(code):
	print "\tSending %s to server."%code
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(code+"\n")
	data = s.recv(BUFFER_SIZE)
	s.close()
	
while True:

	digit = None
	while digit == None:
		if button.is_pressed:
			SendCommandToHost('dstp')
		digit = kp.getKey()
	

	if digit == "*":
		# convert the attempt string to an integer
		att_val = int(attempt)
		#print att_val
		# check if between 0 and 180 (valid dart scores)
		if att_val >= 0 and att_val <= 180:
			SendCommandToHost(str(att_val))
			attempt="0000"
		elif att_val == 3283:
			SendCommandToHost("WLTP")
		elif att_val == 8466:
			SendCommandToHost("TOM")
		elif att_val == 8029:
			SendCommandToHost("TOBY")
	# the sign '#' deletes currently entered attempt
	elif digit == "#":
		attempt = "0000"
	else:
		# Print the result
		print "Digit Entered:       %s"%digit
		attempt = (attempt[1:] + str(digit))  
		print "Attempt value:       %s"%attempt	

	sleep(0.2)
