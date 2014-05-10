#!/usr/bin/python

import sys
import socket
import handler
#import receiver
from pprint import pprint
import time
import datetime

t = time.time()

now_datetime = datetime.datetime.fromtimestamp(t).strftime('%Y_%m_%d_%H-%M-%S')
print now_datetime
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
#		print >>sys.stderr, "Checking module {0:<11} ... ".format('\''+k+'\''),
		exec v
#		print >>sys.stderr, "ok"
	except:
#		print >>sys.stderr, "Need to install %s first" %(k)
		exit(1)

HOST = ''
PORT = 161

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
			print "1"
			data, addr = UDPSock.recvfrom(1024)
			data = decode(data)
			pprint(data)
			pprint(data,fd)
			print
			print
			data = handler.reply(data)
			pprint(data)
			pprint(data,fd)
			print
			print
			data = encode(data)
			UDPSock.sendto(str(data),addr)
	except KeyboardInterrupt:
		UDPSock.close()
		print 'Stop by detected Ctrl-C ... '

if __name__ == "__main__":
	main()
