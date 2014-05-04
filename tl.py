#! /usr/local/bin/python
import sys
import time
import commands
try:
	from pprint import pprint
except:
	print sys.stderr, "No pprint"

log_dir = "./log/"
log_file = "log_oid"
log_ext = "_request.log"
log_ext_respo = "_response.log"


log_filename = log_dir + log_file + log_ext
log_filename_respo = log_dir + log_file + log_ext_respo

snmpdata_list = []

def setLogName(s):
	if s:
		global log_file,log_dir,log_ext, log_ext_respo 
		log_file = s
		global log_filename, log_filename_respo
		log_filename = log_dir + log_file + log_ext
		log_filename_respo = log_dir + log_file + log_ext_respo



def clean_log():
	commands.getstatusoutput("rm -f ./log/*")

def create_command(oid):
	oid = "." + oid
	snmptranslate_command = "snmptranslate -m +all -On " + oid
	return snmptranslate_command

def append_snmpdata_list(s):
	if 'snmpdata' in s:
		snmpdata_list.append(s)

def getTslCmdOutput(string):
	command_str = create_command(string)
	command_result = commands.getoutput(command_str)
	return command_result

def tsl_snmp_oid_list():
	if snmpdata_list:
		tsl_logfile = open(log_filename,'w')
		tsl_logfile_respo = open(log_filename_respo, 'w')
		for i in range(len(snmpdata_list)):
			write_direction = tsl_logfile
			func = snmpdata_list[i]['function']
			if not ( func == "SNMPget" or func == "SNMPset" or func == "SNMPbulk" ):
				write_direction = tsl_logfile_respo
			pdu = snmpdata_list[i]['pdu']
			if 'id' in snmpdata_list[i]['pdu']:
				xid = snmpdata_list[i]['pdu']['id']
			for iOID in range(len(snmpdata_list[i]['snmpdata'])):
				oidResult = getTslCmdOutput(snmpdata_list[i]['snmpdata'][iOID]['oid'])
				print>>write_direction, func, "--", xid,"--", oidResult
		tsl_logfile.close()
		tsl_logfile_respo.close()
