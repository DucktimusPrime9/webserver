#!/usr/bin/python
# Guadalupe Delgado

# checks if webserver.py and wget will generate the same file

#Algorithm
#1 run my code and save to file 1
#2 run wget and save to file 2
#3 run diff to check-crash if different

# run in loop
# wget file
# diff file

import subprocess
import random

port_num = raw_input("Enter the port number of the server.\n") # uses port that server is using
file_read = open("filenames.txt") # opens the file for reading
filename_list = file_read.readlines() # reads in the file names
file_read.close() # close file

#print type(port_num)
#print type(file_list)
#print file_list

print "\nBEGIN FILE TEST\n"

for thefilename in filename_list:
	thefilename = thefilename.strip() # remove the carriage returns
	host = "localhost:"+port_num+"/"+thefilename # use localhost as wget destination
	#print host
	wget = ["wget",host]
	subprocess.call(wget) # wget each file from server
	wget_file = thefilename + ".1" # wget appends .1 on linux for same directory
	#print wget_file
	diff = ["diff",thefilename,wget_file]
	subprocess.call(diff) # should print differences using diff
