#!/usr/bin/python

import os
import sys
import socket
import handler
import mysql
from pprint import pprint
import time
import datetime

fd = ""

t = time.time()
now_datetime = datetime.datetime.fromtimestamp(t).strftime('%Y_%m_%d_%H-%M-%S')
log_path = "./log/"
log = log_path + now_datetime + ".log"
fd = open(log,"a+")

importModules = {
	"pcap"     : "import pcap",
	"dpkt"     : "import dpkt",
	"impacket" : "from impacket import ImpactDecoder, ImpactPacket",
	"scapy"    : "from scapy.all import *"
}

for k, v in importModules.iteritems():
	try:
		#print >>sys.stderr, "Checking module {0:<11} ... ".format('\''+k+'\''),
		exec v
		#print >>sys.stderr, "ok"
	except:
		#print >>sys.stderr, "Need to install %s first" %(k)
		exit(1)

HOST = ''
PORT = 161

UMASK = 0
WORKDIR = "/"
MAXFD = 1024
REDIRECT_TO = ""

def procParams():
	params = """
		PID = %s
		PPID = %s
		PGID = %s
		SID = %s
		UID = %s
		eUID = %s
		real GID = %s
		effective GID = %s
	""" % (	os.getpid(),
		os.getppid(),
		os.getpgrp(),
		os.getsid(0),
		os.getuid(),
		os.geteuid(),
		os.getgid(),
		os.getegid())
	print params

def killRunningProxy():
	pass

def createDaemon():
	if (hasattr(os, "devnull")):
		REDIRECT_TO = os.devnull
	else:
		REDIRECT_TO = "/dev/null"

	try:
		pid = os.fork() #create new process
	except OSError, e:# fail to create process
		raise Exception, "s [%d]" % (e.strerror, e.errno)
	if (pid == 0): # pid == 0 -> in the new child process
		os.setsid() # set this proc into a new session group
		try:
			pid = os.fork()# create the second process which run in the new session group
		except OSError, e:
			raise Exception, "%s [%d]" % (e.strerror,e.errno)
		if (pid == 0): # in the second process
			os.chdir(WORKDIR)
			os.umask(UMASK)
			sys.stdout = fd
			sys.stderr = fd
		else:
			sys.exit(0) # close the first newly forked process
	else:
		os._exit(0) # close the parent proc of the fisrt proc

def checkArgv():
	if not("--debug" in sys.argv):
		createDaemon()
	if ("--reset" in sys.argv):
		mysql.resetAll()
	if ("-o" in sys.argv):
		logName = sys.argv[sys.argv.index("-o") +1]
		print logName
		log = log_path + logName + ".log"
			

def decode(data):
	""" parse snmp raw data to readible data """
	x = SNMP(data)
	data = {}
	f = x.__dict__['fields']
	data['version']   = f['version'].__dict__['val']
	data['community'] = f['community'].__dict__['val']
	data['function']  = f['PDU'].__dict__['name']
	pdu = {}
	function = data['function']
	if function == 'SNMPbulk':
		# Get NonRepeater and MaxRepeater
		pdu["id"]              = f['PDU'].__dict__['fields']['id'].__dict__['val']
		pdu["non_repeaters"]   = f['PDU'].__dict__['fields']['non_repeaters'].__dict__['val']
		pdu["max_repetitions"] = f['PDU'].__dict__['fields']['max_repetitions'].__dict__['val']
	elif function == 'SNMPget':
		# Get id, error, error index
		pdu["id"]          = f['PDU'].__dict__['fields']['id'].__dict__['val']
		pdu["error"]       = f['PDU'].__dict__['fields']['error'].__dict__['val']
		pdu["error_index"] = f['PDU'].__dict__['fields']['error_index'].__dict__['val']
	elif function == 'SNMPresponse':
		# Get id, error, error index 
		pdu["id"]          = f['PDU'].__dict__['fields']['id'].__dict__['val']
		pdu["error"]       = f['PDU'].__dict__['fields']['error'].__dict__['val']
		pdu["error_index"] = f['PDU'].__dict__['fields']['error_index'].__dict__['val']
	elif function == 'SNMPset':
		# Get id, error, error index 
		pdu["id"]          = f['PDU'].__dict__['fields']['id'].__dict__['val']
		pdu["error"]       = f['PDU'].__dict__['fields']['error'].__dict__['val']
		pdu["error_index"] = f['PDU'].__dict__['fields']['error_index'].__dict__['val']
	data['pdu'] = pdu
	snmpdata = []
	# Get all data: oid and value
	for i in f['PDU'].__dict__['fields']['varbindlist']:
		oid   = i.__dict__['fields']['oid'].__dict__['val']
		value = i.__dict__['fields']['value'].__dict__['val']
		snmpdata.append({'oid':oid, 'value':value})
	data['snmpdata'] = snmpdata
	return data

def encode(data):
	svarbindlist = []
	for i in data['snmpdata']:
		svarbindlist.append(SNMPvarbind(oid = i['oid'],value = i['value']))
	result = SNMP(
		version = data['version'],
		community = data['community'],
		PDU = SNMPresponse(
			id = data['pdu']['id'],
			varbindlist = svarbindlist
		)
	)
	return result

def printBoth(data,fd):
	curTime = datetime.datetime.fromtimestamp(t).strftime('[%d/%m/%Y:%H:%M:%S]')
	
	L1 = str(data["community"])+" "+str(data["pdu"]["id"])+" "+curTime+"\""+data["function"][4:]
	for oid in data["snmpdata"]:
		L2 = L1+str(oid['oid'])+"\""+"["+str(oid['value'])+"]"
		if (sys.stdout != fd):
			pprint(L2)
		pprint(L2,fd)
	pprint("",fd)

def main():
	listen_addr = (HOST,PORT)

	UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	print "Running SNMP_Daemon on port ",str(PORT)

	try:
		UDPSock.bind(listen_addr)
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	try:
		while True:
			data, addr = UDPSock.recvfrom(1024)
			data = decode(data)
			printBoth(data,fd)
			print
			data = handler.reply(data)
			printBoth(data,fd)
			print
			data = encode(data)
			UDPSock.sendto(str(data),addr)
	except KeyboardInterrupt:
		UDPSock.close()
		print 'Stop by detected Ctrl-C ... '

if __name__ == "__main__":
#	procParams()
	checkArgv()
	main()
