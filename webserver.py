#!/usr/bin/python
# Guadalupe Delgado

from socket import *
import sys
import time
import thread
import subprocess
import select

# this function reads the command line arguments and sets up the server
# the server will begin listening once it is setup
def server_activation():

#creates a list to store port numbers
	ports = []

	# adds each port to the list
	x = 1
	while x < len(sys.argv):
		temp = sys.argv[x]
		ports.append(temp)
		print "Port " + sys.argv[x] + " has been queued."
		x += 1

	# creates the server ports and sockets
	serverPort = int(ports[0])
	serverSocket = socket(AF_INET,SOCK_STREAM)


	# stops program if invalid port is used
	print ""
	try:
		serverSocket.bind(('',serverPort))
		print "Server listening..."
	except:
		print "This port cannot be bound. You must have the appropriate permissions."
		print "Please retry with a different port."
		sys.exit()
	serverSocket.listen(1)
	print ""

# begins receiving the message and returns server headers
# sends the file after headers
	while 1:
		connectionSocket, addr = serverSocket.accept()
		incoming_stream = connectionSocket.recv(1024)
		while incoming_stream.find("\r\n\r\n")==-1:
			incoming_stream = incoming_stream + connectionSocket.recv(2048)
		print incoming_stream
		if "GET" in incoming_stream:
			reqFile = incoming_stream.find("GET") + 5
		elif "HEAD" in incoming_stream:
			reqFile = incoming_stream.find("HEAD") + 6
		reqFileHTTP = incoming_stream.find("HTTP/1") - 1
		fileName = incoming_stream[reqFile:reqFileHTTP]
		F_in = open(fileName)
		content = F_in.read()
		content_length = len(content)
		header_build = header_creation(200, "ALIVE", content_length)
		connectionSocket.send(header_build)
		connectionSocket.send(content)
		F_in.close()


# creates the headers for sending to the client
# takes care of common status codes
def header_creation(status_code,connection_status,c_len):
	header = ''
	if status_code == 200:
		header = "HTTP/1.1 200 OK\r\n"
	elif status_code == 404:
		header = "HTTP/1.1 404 Not Found\r\n"
	elif status_code == 304:
		header = "HTTP/1.1 304 Not Modified\r\n"
	elif status_code == 400:
		header = "HTTP/1.1 400 Bad Request\r\n"
	current_time = time.strftime("%a, %d %b %Y %H:%M", time.localtime())
	header += 'Date: ' + current_time + '\r\n' +  'Sever: webserver.py\r\n'+ 'Content-Length: ' + str(c_len)+'\r\n'+ connection_status+'\r\n\r\n'
	return header

def main():
	server_activation()
	header_creation()
main()
