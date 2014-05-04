#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import sys
import pprint
import pcap
import dpkt
from impacket import ImpactDecoder, ImpactPacket 
try:
	from scapy.all import *
except:
	print "Install scapy"
	exit(0)

import tl

###############################
#                             #
#  Global                     #
#                             #
###############################


log_dir = "./"
log_file = "log"
log_ext = ".log"

def checkArgv():
	if len(sys.argv) >= 2:
		print "1\n"
		if sys.argv[1].startswith('-'):
			print "2\n"
			option = sys.argv[1][1:]
			print "%s\n" % option
			if 'n' in option:
				print "%s\n" % sys.argv[2]
				global log_file 
				log_file = sys.argv[2]
				tl.setLogName(log_file+"_oid")

checkArgv()


logfile = log_dir + log_file + log_ext 
pcapfilter_dst = "dst port 161 || dst port 162 || dst port 1993"
pcapfilter_src = "src port 161 || src port 162 || src port 1993"
pcapfilter_all = " port 161 || port 162 || port 1993"
# Redirect standard output to file
log = open(logfile, "a+")


###############################
#                             #
#  Function: parse_packet     #
#                             #
###############################
def parse_packet (data):
	decoder = ImpactDecoder.EthDecoder()
	packet = decoder.decode(data)
	ip = packet.child()
	trans = ip.child()
	ip_src = ip.get_ip_src()
	ip_dst = ip.get_ip_dst()
	protocol = ip.get_ip_p()
	if protocol == ImpactPacket.TCP.protocol:
		src_port = trans.get_th_sport()
		dst_port = trans.get_th_dport()
	elif protocol == ImpactPacket.UDP.protocol:
		src_port = trans.get_uh_sport()
		dst_port = trans.get_uh_dport()
	else:
		src_port = ""
		dst_port = ""
	return {
		'src_ip' : ip_src,
		'dst_ip' : ip_dst,
		'src_port' : src_port,
		'dst_port' : dst_port
	}


###############################
#                             #
#  Function: parse_snmp       #
#                             #
###############################
def parse_snmp(data):
	ether = dpkt.ethernet.Ethernet(data)
	x = SNMP(ether.data.data.data)
	# Debug
	# print str(ether).encode('hex')
	# x.show()
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
	data['pdu'] = pdu
	
	snmpdata = []
	# Get all data: oid and value
	for i in f['PDU'].__dict__['fields']['varbindlist']:
		oid   = i.__dict__['fields']['oid'].__dict__['val']
		value = i.__dict__['fields']['value'].__dict__['val']
		snmpdata.append({'oid':oid, 'value':value})
	data['snmpdata'] = snmpdata
	tl.append_snmpdata_list(data)
	return data


###############################
#                             #
#  Function: print_packet     #
#                             #
###############################
def print_packet(pktlen, data, timestamp):
	if not data:
		return
	# Get src/dst IP and Port
	print "in print_packet\n"
	p = parse_packet(data)
	print >>log, "%s(%s) => %s(%s)" %(p['src_ip'], p['src_port'], p['dst_ip'], p['dst_port'])	
	s = parse_snmp(data)
	pprint.pprint(s, log)
	print >>log


###############################
#                             #
#  Function: Main function    #
#                             #
###############################
def main():
	p = pcap.pcapObject()
	# Listen to interface 'em1'
	p.open_live('eth1', 1600, 0, 100)
	# Filter snmp(udp 161, 162), and port 1992
	p.setfilter(pcapfilter_all, 0, 0)

	print >>sys.stderr, 'Press CTRL+C to end capture'
	try:
		while True:
			PResult = p.dispatch(1, print_packet)
	except KeyboardInterrupt:
		print >>sys.stderr # Empty line
		print >>sys.stderr, '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()
		tl.tsl_snmp_oid_list()
		print >>sys.stderr, 'done\n'
	print >>log


if __name__ == '__main__':
	main()
	exit(0)
