

"""OSC Test Script
Written by Aaron Chamberlain Dec. 2013
The purpose of this script is to make a very simple communication structure to the popular 
application touchOSC. This is achieved through the pyOSC library. However, since the pyOSC 
documentation is scarce and only one large example is included, I am going to strip down 
the basic structures of that file to implement a very simple bi-directional communication.
"""

#!/usr/bin/env python

import socket, OSC, re, time, threading, math

receive_address = '192.168.0.81', 8000 #Mac Adress, Outgoing Port
send_address = '192.168.0.3', 9000 #iPhone Adress, Incoming Port

servoAngle = 0

##########################
#	OSC
##########################

# Initialize the OSC server and the client.
s = OSC.OSCServer(receive_address)
c = OSC.OSCClient()
c.connect(send_address)

s.addDefaultHandlers()

# define a message-handler function for the server to call.
def test_handler(addr, tags, stuff, source):
	print "---"
	print "received new osc msg from %s" % OSC.getUrlStr(source)
	print "with addr : %s" % addr
	print "typetags %s" % tags
	print "data %s" % stuff
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "return message %s" % msg
	print "---"

def make_handler(servoname):
	def moveSlider_handler(addr, tags, stuff, source):
		print "message received:"
		msg = OSC.OSCMessage()
		msg.setAddress(addr)
		msg.append(stuff)
		c.send(msg)
		print "X Value is: " 
		print stuff[0] 
		#sendToServo(servoname, stuff[0])

	return moveSlider_handler	

def button_handler(addr, tags, stuff, source):
	print "message received:"
	msg = OSC.OSCMessage()
	msg.setAddress(addr)
	msg.append(stuff)
	c.send(msg)
	print "X Value is: " 
	print stuff[0] 


# adding my functions
s.addMsgHandler("/1/fader4", make_handler(8))
s.addMsgHandler("/1/fader3", make_handler(7))
s.addMsgHandler("/1/toggle3", button_handler)
s.addMsgHandler("/1/toggle4", button_handler)
# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
	print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()

# Loop while threads are running.
try :
	while 1 :
		time.sleep(10)
 
except KeyboardInterrupt :
	print "\nClosing OSCServer."
	s.close()
	print "Waiting for Server-thread to finish"
	st.join()
	print "Done"