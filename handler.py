#/usr/bin/python
import sshXen
import sys
try:
	from pprint import pprint
except:
	sys.exit("no pprint")
import mysql


def popOID(oid):
	l = oid.split(".")
	l.pop()
	newOid = ".".join(l)
	return newOid

vtpVlanNameTable = {
"1":{'VlanID':1,'VlanName':'default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x86\xa1','VlanEditRowStatus':4,'VlanEditType':1},
"2":{'VlanID':2,'VlanName':'Control-Hardware','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x86\xa2','VlanEditRowStatus':4,'VlanEditType':1},
"1002":{'VlanID':1002,'VlanName':'fddi-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8a','VlanEditRowStatus':4,'VlanEditType':2},
"1003":{'VlanID':1003,'VlanName':'token-ring-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8b','VlanEditRowStatus':4,'VlanEditType':3},
"1004":{'VlanID':1004,'VlanName':'fddinet-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8c','VlanEditRowStatus':4,'VlanEditType':4},
"1005":{'VlanID':1005,'VlanName':'trnet-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8d','VlanEditRowStatus':4,'VlanEditType':5},
}

vtpVlanNameAppendix = [{'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.7.1.1003', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.8.1.1004', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.8.1.1005', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.9.1.1004', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.9.1.1005', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.10.1.1003', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.11.1.1', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.11.1.2', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.11.1.1002', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.11.1.1003', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.11.1.1004', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.11.1.1005', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.12.1.1', 'value': 0L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.3.1.1.12.1.2', 'value': 0L}]
	
#vtpVlanEditBufferOwner = "" #vtpVlanEditBufferOwner

portTable = {
"1":{},
"2":{},
"10101":{"portNumL":10101,"portNumS":1,"pPortName":"GigabitEthernet1/0/1","MAC":"00:16:3e:01:01:01","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10102":{"portNumL":10102,"portNumS":2,"pPortName":"GigabitEthernet1/0/2","MAC":"00:16:3e:01:01:02","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10103":{"portNumL":10103,"portNumS":3,"pPortName":"GigabitEthernet1/0/3","MAC":"00:16:3e:01:01:03","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10104":{"portNumL":10104,"portNumS":4,"pPortName":"GigabitEthernet1/0/4","MAC":"00:16:3e:01:01:04","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10105":{"portNumL":10105,"portNumS":5,"pPortName":"GigabitEthernet1/0/5","MAC":"00:16:3e:01:01:05","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10106":{"portNumL":10106,"portNumS":6,"pPortName":"GigabitEthernet1/0/6","MAC":"00:16:3e:01:01:06","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10107":{"portNumL":10107,"portNumS":7,"pPortName":"GigabitEthernet1/0/7","MAC":"00:16:3e:01:01:07","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10108":{"portNumL":10108,"portNumS":8,"pPortName":"GigabitEthernet1/0/8","MAC":"00:16:3e:01:01:08","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10109":{"portNumL":10109,"portNumS":9,"pPortName":"GigabitEthernet1/0/9","MAC":"00:16:3e:01:01:09","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10110":{"portNumL":10110,"portNumS":10,"pPortName":"GigabitEthernet1/0/10","MAC":"00:16:3e:01:01:0a","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10111":{"portNumL":10111,"portNumS":11,"pPortName":"GigabitEthernet1/0/11","MAC":"00:16:3e:01:01:0b","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10112":{"portNumL":10112,"portNumS":12,"pPortName":"GigabitEthernet1/0/12","MAC":"00:16:3e:01:01:0c","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10113":{"portNumL":10113,"portNumS":13,"pPortName":"GigabitEthernet1/0/13","MAC":"00:16:3e:01:01:0d","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10114":{"portNumL":10114,"portNumS":14,"pPortName":"GigabitEthernet1/0/14","MAC":"00:16:3e:01:01:0e","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10115":{"portNumL":10115,"portNumS":15,"pPortName":"GigabitEthernet1/0/15","MAC":"00:16:3e:01:01:0f","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10116":{"portNumL":10116,"portNumS":16,"pPortName":"GigabitEthernet1/0/16","MAC":"00:16:3e:01:01:10","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10117":{"portNumL":10117,"portNumS":17,"pPortName":"GigabitEthernet1/0/17","MAC":"00:16:3e:01:01:11","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10118":{"portNumL":10118,"portNumS":18,"pPortName":"GigabitEthernet1/0/18","MAC":"00:16:3e:01:01:12","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10119":{"portNumL":10119,"portNumS":19,"pPortName":"GigabitEthernet1/0/19","MAC":"00:16:3e:01:01:13","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10120":{"portNumL":10120,"portNumS":20,"pPortName":"GigabitEthernet1/0/20","MAC":"00:16:3e:01:01:14","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10121":{"portNumL":10121,"portNumS":21,"pPortName":"GigabitEthernet1/0/21","MAC":"00:16:3e:01:01:15","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10122":{"portNumL":10122,"portNumS":22,"pPortName":"GigabitEthernet1/0/22","MAC":"00:16:3e:01:01:16","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10123":{"portNumL":10123,"portNumS":23,"pPortName":"GigabitEthernet1/0/23","MAC":"00:16:3e:01:01:17","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10124":{"portNumL":10124,"portNumS":24,"pPortName":"GigabitEthernet1/0/24","MAC":"00:16:3e:01:01:18","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10125":{"portNumL":10125,"portNumS":25,"pPortName":"GigabitEthernet1/0/25","MAC":"00:16:3e:01:01:19","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10126":{"portNumL":10126,"portNumS":26,"pPortName":"GigabitEthernet1/0/26","MAC":"00:16:3e:01:01:1a","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10127":{"portNumL":10127,"portNumS":27,"pPortName":"GigabitEthernet1/0/27","MAC":"00:16:3e:01:01:1b","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10128":{"portNumL":10128,"portNumS":28,"pPortName":"GigabitEthernet1/0/28","MAC":"00:16:3e:01:01:1c","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10129":{"portNumL":10129,"portNumS":29,"pPortName":"GigabitEthernet1/0/29","MAC":"00:16:3e:01:01:1d","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10130":{"portNumL":10130,"portNumS":30,"pPortName":"GigabitEthernet1/0/30","MAC":"00:16:3e:01:01:1e","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10131":{"portNumL":10131,"portNumS":31,"pPortName":"GigabitEthernet1/0/31","MAC":"00:16:3e:01:01:1f","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10132":{"portNumL":10132,"portNumS":32,"pPortName":"GigabitEthernet1/0/32","MAC":"00:16:3e:01:01:20","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10133":{"portNumL":10133,"portNumS":33,"pPortName":"GigabitEthernet1/0/33","MAC":"00:16:3e:01:01:21","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10134":{"portNumL":10134,"portNumS":34,"pPortName":"GigabitEthernet1/0/34","MAC":"00:16:3e:01:01:22","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10135":{"portNumL":10135,"portNumS":35,"pPortName":"GigabitEthernet1/0/35","MAC":"00:16:3e:01:01:23","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10136":{"portNumL":10136,"portNumS":36,"pPortName":"GigabitEthernet1/0/36","MAC":"00:16:3e:01:01:24","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10137":{"portNumL":10137,"portNumS":37,"pPortName":"GigabitEthernet1/0/37","MAC":"00:16:3e:01:01:25","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10138":{"portNumL":10138,"portNumS":38,"pPortName":"GigabitEthernet1/0/38","MAC":"00:16:3e:01:01:26","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10139":{"portNumL":10139,"portNumS":39,"pPortName":"GigabitEthernet1/0/39","MAC":"00:16:3e:01:01:27","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10140":{"portNumL":10140,"portNumS":40,"pPortName":"GigabitEthernet1/0/40","MAC":"00:16:3e:01:01:28","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10141":{"portNumL":10141,"portNumS":41,"pPortName":"GigabitEthernet1/0/41","MAC":"00:16:3e:01:01:29","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10142":{"portNumL":10142,"portNumS":42,"pPortName":"GigabitEthernet1/0/42","MAC":"00:16:3e:01:01:2a","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10143":{"portNumL":10143,"portNumS":43,"pPortName":"GigabitEthernet1/0/43","MAC":"00:16:3e:01:01:2b","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10144":{"portNumL":10144,"portNumS":44,"pPortName":"GigabitEthernet1/0/44","MAC":"00:16:3e:01:01:2c","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10145":{"portNumL":10145,"portNumS":45,"pPortName":"GigabitEthernet1/0/45","MAC":"00:16:3e:01:01:2d","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10146":{"portNumL":10146,"portNumS":46,"pPortName":"GigabitEthernet1/0/46","MAC":"00:16:3e:01:01:2e","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10147":{"portNumL":10147,"portNumS":47,"pPortName":"GigabitEthernet1/0/47","MAC":"00:16:3e:01:00:2f","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10148":{"portNumL":10148,"portNumS":48,"pPortName":"GigabitEthernet1/0/48","MAC":"00:16:3e:01:01:30","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10149":{"portNumL":10149,"portNumS":49,"pPortName":"GigabitEthernet1/0/49","MAC":"00:16:3e:01:01:31","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10150":{"portNumL":10150,"portNumS":50,"pPortName":"GigabitEthernet1/0/50","MAC":"00:16:3e:01:01:32","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10201":{"portNumL":10201,"portNumS":101,"pPortName":"TenGigabitEthernet1/0/1","MAC":"00:16:3e:01:00:71","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L},
"10202":{"portNumL":10202,"portNumS":102,"pPortName":"TenGigabitEthernet1/0/2","MAC":"00:16:3e:01:00:72","VLANID":1,"AdminStatus":0,"Duplex":2,"AdminSpeed":100000000L}
}
def getvtpVlanName(lastFirst):
	if lastFirst in vtpVlanNameTable.keys():
		return vtpVlanNameTable[lastFirst]['VlanName']
	else:
		print lastFirst
		return 0

def getvtpVlanEditRowStatus(lastFirst):
	try:
		result = vtpVlanNameTable[lastFirst]['VlanEditRowStatus']
	except:
		result = 4 #set default to status "createAndGo"
	return result

def getvtpVlanEditType(lastFirst):
	try:
		result = vtpVlanNameTable[lastFirst]['VlanEditType']
	except:
		result = 0
	return result

def getvtpVlanEditName(lastFirst):
	try:
		result = vtpVlanNameTable[lastFirst]['VlanName']
	except:
		result = '\x81\x00'
	return result

def getpVlanEditDot10Said(lastFirst):
	try:
		result = vtpVlanNameTable[lastFirst]['VlanDot10Said']
	except:
		result = '\x81'
	return result

def getPortTableAdminStatus(lastFirst):
	return portTable[lastFirst]['AdminStatus']
def getVmVlan(lastFirst):
	return portTable[lastFirst]['VLANID']

cswitch_attr = {
	"1.3.6.1.2.1.1.1.0": 'Cisco IOS Software, C2960S Software (C2960S-UNIVERSALK9-M), Version 12.2(55)SE3, RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2011 by Cisco Systems, Inc.\r\nCompiled Thu 05-May-11 16:56 by prod_rel_team',
#	"1.3.6.1.2.1.1.1.0":'Cisco IOS Software, Catalyst 4500 L3 Switch Software (cat4500-ENTSERVICESK9-M), Version 12.2(54)SG, RELEASE SOFTWARE (fc3)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2010 by Cisco Systems, Inc.\r\nCompiled Sun 27-Jun-10 00:29 b',
	"1.3.6.1.4.1.9.9.46.1.4.1.1.3.1":"boss.testbed.ncku.edu.tw",
	
#diff packet statics with port, each oid below should append a portNumL
	"1.3.6.1.4.1.9.9.46.1.3.1.1.4.1":getvtpVlanName,
	"1.3.6.1.2.1.2.2.1.7":getPortTableAdminStatus,
	"1.3.6.1.4.1.9.5.1.4.1.1.9.0":'\x81\x00',
	"1.3.6.1.4.1.9.5.1.4.1.1.9.1":100000000L,
	"1.3.6.1.4.1.9.5.1.4.1.1.10.0":'\x81\x00',
	"1.3.6.1.4.1.9.5.1.4.1.1.10.1":2L,
	"1.3.6.1.4.1.9.9.46.1.4.1.1.2.1": 2L,
	"1.3.6.1.4.1.9.9.46.1.6.1.1.13":2L,
	"1.3.6.1.4.1.9.9.68.1.2.2.1.2":getVmVlan,

	"1.3.6.1.2.1.2.2.1.10":1213091L,
	"1.3.6.1.2.1.2.2.1.11": 0L,
	"1.3.6.1.2.1.2.2.1.12":'\x81\x00',
	'1.3.6.1.2.1.2.2.1.13': 0L,
	'1.3.6.1.2.1.2.2.1.14': 8L,
	'1.3.6.1.2.1.2.2.1.15': 0L,
	'1.3.6.1.2.1.2.2.1.16': 255945157L,
	'1.3.6.1.2.1.2.2.1.17': 463939L,
	'1.3.6.1.2.1.2.2.1.18': '\x81\x00',
	'1.3.6.1.2.1.2.2.1.19': 0L,
	'1.3.6.1.2.1.2.2.1.20': 0L,
	'1.3.6.1.2.1.2.2.1.21': '\x81\x00',

	"1.3.6.1.4.1.9.9.46.1.4.1.1.1.1":2L,


	"1.3.6.1.4.1.9.9.46.1.4.2.1.11.1":getvtpVlanEditRowStatus,
	"1.3.6.1.4.1.9.9.46.1.4.2.1.3.1":getvtpVlanEditType,
	"1.3.6.1.4.1.9.9.46.1.4.2.1.4.1":getvtpVlanEditName,
	"1.3.6.1.4.1.9.9.46.1.4.2.1.6.1":getpVlanEditDot10Said,

	"1.3.6.1.4.1.9.9.46.1.6.1.1.4":'\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf9\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',

	"1.3.6.1.4.1.9.9.46.1.6.1.1.17":'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
}



def bulkVlanNameTable(argv):
	print "bulkVlanNameTable"
	name = []
	mtu = []
	dot10said = []
	response = []
	a = vtpVlanNameTable.keys()
	b = []
	pprint(vtpVlanNameTable)
	for i in a:
		b.append(int(i))
	b = sorted(b)
	for intKey in b:
		key = str(intKey)
		nameOID = ".".join(["1.3.6.1.4.1.9.9.46.1.3.1.1.4.1",key])
		mtuOID = ".".join(["1.3.6.1.4.1.9.9.46.1.3.1.1.5.1",key])
		d10saidOID = ".".join(["1.3.6.1.4.1.9.9.46.1.3.1.1.6.1",key])
		print nameOID
		print mtuOID
		print d10saidOID
		name.append({'oid':nameOID,'value':vtpVlanNameTable[key]['VlanName']})
		mtu.append({'oid':mtuOID,'value':vtpVlanNameTable[key]['VlanMTU']})
		dot10said.append({'oid':d10saidOID,'value':vtpVlanNameTable[key]['VlanDot10Said']})
	pprint(name)
	pprint(mtu)
	pprint(dot10said)
	response.extend(name)
	response.extend(mtu)
	response.extend(dot10said)
	response.extend(vtpVlanNameAppendix)
	return response[0:32]

# original cisco port info
vlanTrunkPortDynamicStatus=[{'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10101', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10102', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10103', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10104', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10105', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10106', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10107', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10108', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10109', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10110', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10111', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10112', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10113', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10114', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10115', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10116', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10117', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10118', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10119', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10120', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10121', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10122', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10123', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10124', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10125', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10126', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10127', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10128', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10129', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10130', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10131', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10132', 'value': 2L}]

vlanTrunkPortDynamicStatus2=[{'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10133', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10134', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10135', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10136', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10137', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10138', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10139', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10140', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10141', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10142', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10143', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10144', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10145', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10146', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10147', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10148', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10149', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10150', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10201', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.14.10202', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10101', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10102', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10103', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10104', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10105', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10106', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10107', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10108', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10109', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10110', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10111', 'value': 1L},
              {'oid': '1.3.6.1.4.1.9.9.46.1.6.1.1.15.10112', 'value': 1L}]

dot1BassNumPortsP1 = [{'oid': '1.3.6.1.2.1.17.1.4.1.2.1', 'value': 10101L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.2', 'value': 10102L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.3', 'value': 10103L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.5', 'value': 10105L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.4', 'value': 10104L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.6', 'value': 10106L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.7', 'value': 10107L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.8', 'value': 10108L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.9', 'value': 10109L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.10', 'value': 10110L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.11', 'value': 10111L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.12', 'value': 10112L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.13', 'value': 10113L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.14', 'value': 10114L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.15', 'value': 10115L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.16', 'value': 10116L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.17', 'value': 10117L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.18', 'value': 10118L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.19', 'value': 10119L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.20', 'value': 10120L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.21', 'value': 10121L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.22', 'value': 10122L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.23', 'value': 10123L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.24', 'value': 10124L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.25', 'value': 10125L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.26', 'value': 10126L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.27', 'value': 10127L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.28', 'value': 10128L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.29', 'value': 10129L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.30', 'value': 10130L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.31', 'value': 10131L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.32', 'value': 10132L},
]

dot1BassNumPorts36P1 = [{'oid': '1.3.6.1.2.1.17.1.4.1.2.33', 'value': 10133L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.34', 'value': 10134L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.35', 'value': 10135L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.36', 'value': 10136L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.37', 'value': 10137L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.38', 'value': 10138L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.39', 'value': 10139L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.40', 'value': 10140L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.41', 'value': 10141L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.42', 'value': 10142L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.43', 'value': 10143L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.44', 'value': 10144L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.45', 'value': 10145L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.46', 'value': 10146L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.47', 'value': 10147L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.48', 'value': 10148L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.49', 'value': 10149L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.50', 'value': 10150L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.51', 'value': 10201L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.2.52', 'value': 10202L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.1', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.2', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.3', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.5', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.6', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.7', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.8', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.9', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.10', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.11', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.12', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.13', 'value': '0.0'},
]

dot1BassNumPortsP2 = [{'oid': '1.3.6.1.2.1.17.1.4.1.2.48', 'value': 10148L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.3.48', 'value': '0.0'},
              {'oid': '1.3.6.1.2.1.17.1.4.1.4.48', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.1.4.1.5.48', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.2.1.0', 'value': 3L},
              {'oid': '1.3.6.1.2.1.17.2.2.0', 'value': 32770L},
              {'oid': '1.3.6.1.2.1.17.2.3.0', 'value': 219227000L},
              {'oid': '1.3.6.1.2.1.17.2.4.0', 'value': 10L},
              {'oid': '1.3.6.1.2.1.17.2.5.0',
               'value': '\x80\x02\x00\x15cP>@'},
              {'oid': '1.3.6.1.2.1.17.2.6.0', 'value': 12L},
              {'oid': '1.3.6.1.2.1.17.2.7.0', 'value': 48L},
              {'oid': '1.3.6.1.2.1.17.2.8.0', 'value': 2000L},
              {'oid': '1.3.6.1.2.1.17.2.9.0', 'value': 200L},
              {'oid': '1.3.6.1.2.1.17.2.10.0', 'value': 100L},
              {'oid': '1.3.6.1.2.1.17.2.11.0', 'value': 1500L},
              {'oid': '1.3.6.1.2.1.17.2.12.0', 'value': 2000L},
              {'oid': '1.3.6.1.2.1.17.2.13.0', 'value': 200L},
              {'oid': '1.3.6.1.2.1.17.2.14.0', 'value': 1500L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.1.48', 'value': 48L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.2.48', 'value': 128L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.3.48', 'value': 5L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.4.48', 'value': 1L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.5.48', 'value': 4L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.6.48',
               'value': '\x80\x02\x00\x15cP>@'},
              {'oid': '1.3.6.1.2.1.17.2.15.1.7.48', 'value': 8L},
              {'oid': '1.3.6.1.2.1.17.2.15.1.8.48',
               'value': '\x80\x02@\xf4\xec%$\x00'},
              {'oid': '1.3.6.1.2.1.17.2.15.1.9.48', 'value': '\x80\x18'},
              {'oid': '1.3.6.1.2.1.17.2.15.1.10.48', 'value': 1L},
              {'oid': '1.3.6.1.2.1.17.4.1.0', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.4.2.0', 'value': 300L},
              {'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.24.118.92.229',
               'value': '\x00\x16\x18v\\\xe5'},
              {'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.24.118.93.10',
               'value': '\x00\x16\x18v]\n'}]

dot1dTpFdbTable1 = [
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.41','value':'\x00\x16\x3e\x01\x01\x29'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.2','value':'\x00\x16\x3e\x01\x01\x02'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.3','value':'\x00\x16\x3e\x01\x01\x03'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.4','value':'\x00\x16\x3e\x01\x01\x04'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.5','value':'\x00\x16\x3e\x01\x01\x05'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.6','value':'\x00\x16\x3e\x01\x01\x06'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.7','value':'\x00\x16\x3e\x01\x01\x07'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.8','value':'\x00\x16\x3e\x01\x01\x08'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.9','value':'\x00\x16\x3e\x01\x01\x09'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.10','value':'\x00\x16\x3e\x01\x01\x0a'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.11','value':'\x00\x16\x3e\x01\x01\x0b'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.12','value':'\x00\x16\x3e\x01\x01\x0c'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.13','value':'\x00\x16\x3e\x01\x01\x0d'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.14','value':'\x00\x16\x3e\x01\x01\x0e'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.15','value':'\x00\x16\x3e\x01\x01\x0f'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.16','value':'\x00\x16\x3e\x01\x01\x10'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.17','value':'\x00\x16\x3e\x01\x01\x11'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.18','value':'\x00\x16\x3e\x01\x01\x12'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.19','value':'\x00\x16\x3e\x01\x01\x13'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.20','value':'\x00\x16\x3e\x01\x01\x14'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.21','value':'\x00\x16\x3e\x01\x01\x15'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.22','value':'\x00\x16\x3e\x01\x01\x16'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.23','value':'\x00\x16\x3e\x01\x01\x17'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.24','value':'\x00\x16\x3e\x01\x01\x18'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.25','value':'\x00\x16\x3e\x01\x01\x19'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.26','value':'\x00\x16\x3e\x01\x01\x1a'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.27','value':'\x00\x16\x3e\x01\x01\x1b'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.28','value':'\x00\x16\x3e\x01\x01\x1c'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.29','value':'\x00\x16\x3e\x01\x01\x1d'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.30','value':'\x00\x16\x3e\x01\x01\x1e'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.31','value':'\x00\x16\x3e\x01\x01\x1f'},

{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.32','value':'\x00\x16\x3e\x01\x01\x20'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.33','value':'\x00\x16\x3e\x01\x01\x21'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.34','value':'\x00\x16\x3e\x01\x01\x22'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.35','value':'\x00\x16\x3e\x01\x01\x23'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.36','value':'\x00\x16\x3e\x01\x01\x24'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.37','value':'\x00\x16\x3e\x01\x01\x25'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.38','value':'\x00\x16\x3e\x01\x01\x26'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.39','value':'\x00\x16\x3e\x01\x01\x27'},
{'oid': '1.3.6.1.2.1.17.4.3.1.1.0.22.62.1.1.40','value':'\x00\x16\x3e\x01\x01\x28'},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.41','value':41L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.2','value':2L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.3','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.4','value':4L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.5','value':5L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.6','value':6L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.7','value':7L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.8','value':8L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.9','value':9L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.10','value':10L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.11','value':11L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.12','value':12L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.13','value':13L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.14','value':14L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.15','value':15L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.16','value':16L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.17','value':17L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.18','value':18L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.19','value':19L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.20','value':20L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.21','value':21L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.22','value':22L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.23','value':23L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.24','value':24L},

{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.25','value':25L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.26','value':26L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.27','value':27L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.28','value':28L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.29','value':29L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.30','value':30L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.31','value':31L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.32','value':32L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.33','value':33L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.34','value':34L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.35','value':35L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.36','value':36L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.37','value':37L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.38','value':38L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.39','value':39L},
{'oid': '1.3.6.1.2.1.17.4.3.1.2.0.22.62.1.1.40','value':40L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.41','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.2','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.3','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.4','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.5','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.6','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.7','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.8','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.9','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.10','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.11','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.12','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.13','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.14','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.15','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.16','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.17','value':3L},

{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.18','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.19','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.20','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.21','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.22','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.23','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.24','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.25','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.26','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.27','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.28','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.29','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.30','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.31','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.32','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.33','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.34','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.35','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.36','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.37','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.38','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.39','value':3L},
{'oid': '1.3.6.1.2.1.17.4.3.1.3.0.22.62.1.1.40','value':3L}
]

TFTP1Appendix = [
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.1', 'value': 1L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.2', 'value': 2L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.3', 'value': 3L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.4', 'value': 4L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.5', 'value': 5L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.6', 'value': 6L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.7', 'value': 7L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.8', 'value': 8L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.9', 'value': 9L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.10', 'value': 10L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.11', 'value': 11L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.12', 'value': 12L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.13', 'value': 13L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.14', 'value': 14L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.15', 'value': 15L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.16', 'value': 16L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.17', 'value': 17L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.18', 'value': 18L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.19', 'value': 19L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.20', 'value': 20L},
]


def P1TFTBulk(argv):
	result = []
	lastLast = argv['snmpdata'][0]['oid']
	if lastLast == '1.3.6.1.2.1.17.4.3':
		for i in range(32):
			print i
			result.append(dot1dTpFdbTable1[i])
		return result
	lastIndex = 0
	startAppending = False
	appendCount = 0
	for i in range(len(dot1dTpFdbTable1)):
		if dot1dTpFdbTable1[i]['oid'][0] == ".":
			dot1dTpFdbTable1[i]['oid'] = dot1dTpFdbTable1[i]['oid'][1:]
		if startAppending:
			if appendCount == 32:
				break
			else:
				result.append(dot1dTpFdbTable1[i])
				appendCount += 1
				if appendCount == 32:
					return result
		if lastLast == dot1dTpFdbTable1[i]['oid']:
			startAppending = True
	d = 32 - appendCount
	for i in range(len(TFTP1Appendix)):
		if TFTP1Appendix[i]['oid'][0] == ".":
			TFTP1Appendix[i]['oid'] = TFTP1Appendix[i]['oid'][1:]
	for i in range(d):
		try:
			result.append(TFTP1Appendix[i])
		except:
			pass
	return result

dot1dTpFdbTable101 = [{'oid': '1.3.6.1.2.1.17.4.4.1.1.4', 'value': 4L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.26', 'value': 26L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.31', 'value': 31L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.2.4', 'value': 1510L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.2.26', 'value': 1510L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.2.31', 'value': 1510L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.3.4', 'value': 4064L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.3.26', 'value': 4797L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.3.31', 'value': 3534L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.4.4', 'value': 1682912L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.4.26', 'value': 1682860L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.4.31', 'value': 1800198L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.5.4', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.5.26', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.5.31', 'value': 0L},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.1', 'value': 'Vl1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.2', 'value': 'Vl2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5137', 'value': 'StackPort1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5138',
               'value': 'StackSub-St1-1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5139',
               'value': 'StackSub-St1-2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10101', 'value': 'Gi1/0/1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10102', 'value': 'Gi1/0/2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10103', 'value': 'Gi1/0/3'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10104', 'value': 'Gi1/0/4'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10105', 'value': 'Gi1/0/5'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10106', 'value': 'Gi1/0/6'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10107', 'value': 'Gi1/0/7'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10108', 'value': 'Gi1/0/8'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10109', 'value': 'Gi1/0/9'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10110', 'value': 'Gi1/0/10'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10111', 'value': 'Gi1/0/11'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10112', 'value': 'Gi1/0/12'}]

dot1dTpFdbTable102 = [{'oid': '1.3.6.1.2.1.17.4.4.1.1.24', 'value': 24L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.1.51', 'value': 51L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.2.24', 'value': 1510L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.2.51', 'value': 1510L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.3.24', 'value': 4511L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.3.51', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.4.24', 'value': 1682359L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.4.51', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.5.24', 'value': 0L},
              {'oid': '1.3.6.1.2.1.17.4.4.1.5.51', 'value': 0L},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.1', 'value': 'Vl1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.2', 'value': 'Vl2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5137', 'value': 'StackPort1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5138',
               'value': 'StackSub-St1-1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5139',
               'value': 'StackSub-St1-2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10101', 'value': 'Gi1/0/1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10102', 'value': 'Gi1/0/2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10103', 'value': 'Gi1/0/3'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10104', 'value': 'Gi1/0/4'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10105', 'value': 'Gi1/0/5'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10106', 'value': 'Gi1/0/6'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10107', 'value': 'Gi1/0/7'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10108', 'value': 'Gi1/0/8'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10109', 'value': 'Gi1/0/9'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10110', 'value': 'Gi1/0/10'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10111', 'value': 'Gi1/0/11'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10112', 'value': 'Gi1/0/12'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10113', 'value': 'Gi1/0/13'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10114', 'value': 'Gi1/0/14'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10115', 'value': 'Gi1/0/15'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10116', 'value': 'Gi1/0/16'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10117', 'value': 'Gi1/0/17'}]

dot1dTpFdbTable1002 =  [{'oid': '1.3.6.1.2.1.31.1.1.1.1.1', 'value': 'Vl1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.2', 'value': 'Vl2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5137', 'value': 'StackPort1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5138',
               'value': 'StackSub-St1-1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5139',
               'value': 'StackSub-St1-2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10101', 'value': 'Gi1/0/1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10102', 'value': 'Gi1/0/2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10103', 'value': 'Gi1/0/3'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10104', 'value': 'Gi1/0/4'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10105', 'value': 'Gi1/0/5'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10106', 'value': 'Gi1/0/6'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10107', 'value': 'Gi1/0/7'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10108', 'value': 'Gi1/0/8'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10109', 'value': 'Gi1/0/9'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10110', 'value': 'Gi1/0/10'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10111', 'value': 'Gi1/0/11'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10112', 'value': 'Gi1/0/12'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10113', 'value': 'Gi1/0/13'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10114', 'value': 'Gi1/0/14'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10115', 'value': 'Gi1/0/15'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10116', 'value': 'Gi1/0/16'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10117', 'value': 'Gi1/0/17'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10118', 'value': 'Gi1/0/18'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10119', 'value': 'Gi1/0/19'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10120', 'value': 'Gi1/0/20'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10121', 'value': 'Gi1/0/21'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10122', 'value': 'Gi1/0/22'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10123', 'value': 'Gi1/0/23'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10124', 'value': 'Gi1/0/24'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10125', 'value': 'Gi1/0/25'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10126', 'value': 'Gi1/0/26'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10127', 'value': 'Gi1/0/27'}]

dot1dTpFdbTable1003 = [{'oid': '1.3.6.1.2.1.31.1.1.1.1.1', 'value': 'Vl1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.2', 'value': 'Vl2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5137', 'value': 'StackPort1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5138',
               'value': 'StackSub-St1-1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5139',
               'value': 'StackSub-St1-2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10101', 'value': 'Gi1/0/1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10102', 'value': 'Gi1/0/2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10103', 'value': 'Gi1/0/3'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10104', 'value': 'Gi1/0/4'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10105', 'value': 'Gi1/0/5'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10106', 'value': 'Gi1/0/6'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10107', 'value': 'Gi1/0/7'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10108', 'value': 'Gi1/0/8'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10109', 'value': 'Gi1/0/9'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10110', 'value': 'Gi1/0/10'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10111', 'value': 'Gi1/0/11'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10112', 'value': 'Gi1/0/12'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10113', 'value': 'Gi1/0/13'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10114', 'value': 'Gi1/0/14'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10115', 'value': 'Gi1/0/15'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10116', 'value': 'Gi1/0/16'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10117', 'value': 'Gi1/0/17'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10118', 'value': 'Gi1/0/18'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10119', 'value': 'Gi1/0/19'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10120', 'value': 'Gi1/0/20'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10121', 'value': 'Gi1/0/21'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10122', 'value': 'Gi1/0/22'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10123', 'value': 'Gi1/0/23'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10124', 'value': 'Gi1/0/24'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10125', 'value': 'Gi1/0/25'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10126', 'value': 'Gi1/0/26'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10127', 'value': 'Gi1/0/27'}]

dot1dTpFdbTable1004 = [{'oid': '1.3.6.1.2.1.31.1.1.1.1.1', 'value': 'Vl1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.2', 'value': 'Vl2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5137', 'value': 'StackPort1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5138',
               'value': 'StackSub-St1-1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5139',
               'value': 'StackSub-St1-2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10101', 'value': 'Gi1/0/1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10102', 'value': 'Gi1/0/2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10103', 'value': 'Gi1/0/3'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10104', 'value': 'Gi1/0/4'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10105', 'value': 'Gi1/0/5'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10106', 'value': 'Gi1/0/6'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10107', 'value': 'Gi1/0/7'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10108', 'value': 'Gi1/0/8'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10109', 'value': 'Gi1/0/9'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10110', 'value': 'Gi1/0/10'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10111', 'value': 'Gi1/0/11'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10112', 'value': 'Gi1/0/12'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10113', 'value': 'Gi1/0/13'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10114', 'value': 'Gi1/0/14'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10115', 'value': 'Gi1/0/15'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10116', 'value': 'Gi1/0/16'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10117', 'value': 'Gi1/0/17'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10118', 'value': 'Gi1/0/18'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10119', 'value': 'Gi1/0/19'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10120', 'value': 'Gi1/0/20'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10121', 'value': 'Gi1/0/21'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10122', 'value': 'Gi1/0/22'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10123', 'value': 'Gi1/0/23'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10124', 'value': 'Gi1/0/24'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10125', 'value': 'Gi1/0/25'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10126', 'value': 'Gi1/0/26'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10127', 'value': 'Gi1/0/27'}]

dot1dTpFdbTable1005 = [{'oid': '1.3.6.1.2.1.31.1.1.1.1.1', 'value': 'Vl1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.2', 'value': 'Vl2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5137', 'value': 'StackPort1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5138',
               'value': 'StackSub-St1-1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.5139',
               'value': 'StackSub-St1-2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10101', 'value': 'Gi1/0/1'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10102', 'value': 'Gi1/0/2'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10103', 'value': 'Gi1/0/3'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10104', 'value': 'Gi1/0/4'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10105', 'value': 'Gi1/0/5'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10106', 'value': 'Gi1/0/6'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10107', 'value': 'Gi1/0/7'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10108', 'value': 'Gi1/0/8'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10109', 'value': 'Gi1/0/9'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10110', 'value': 'Gi1/0/10'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10111', 'value': 'Gi1/0/11'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10112', 'value': 'Gi1/0/12'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10113', 'value': 'Gi1/0/13'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10114', 'value': 'Gi1/0/14'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10115', 'value': 'Gi1/0/15'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10116', 'value': 'Gi1/0/16'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10117', 'value': 'Gi1/0/17'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10118', 'value': 'Gi1/0/18'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10119', 'value': 'Gi1/0/19'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10120', 'value': 'Gi1/0/20'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10121', 'value': 'Gi1/0/21'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10122', 'value': 'Gi1/0/22'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10123', 'value': 'Gi1/0/23'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10124', 'value': 'Gi1/0/24'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10125', 'value': 'Gi1/0/25'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10126', 'value': 'Gi1/0/26'},
              {'oid': '1.3.6.1.2.1.31.1.1.1.1.10127', 'value': 'Gi1/0/27'}]

def getdot1dTpFdbTable(argv):
	if argv['community'] == 'private@1':
		return P1TFTBulk(argv)
	elif argv['community'] == 'private@2':
		return P1TFTBulk(argv)
	elif argv['community'] == 'testbed@1':
		return P1TFTBulk(argv)
	elif argv['community'] == 'testbed@2':
		return P1TFTBulk(argv)
	elif argv['community'] == 'private@101':
		return dot1dTpFdbTable101
	elif argv['community'] == 'private@102':
		return dot1dTpFdbTable102
	elif argv['community'] == 'private@1002':
		return dot1dTpFdbTable1002
	elif argv['community'] == 'private@1003':
		return dot1dTpFdbTable1003
	elif argv['community'] == 'private@1004':
		return dot1dTpFdbTable1004
	else:
		return dot1dTpFdbTable1005

def getDot1BassNumPorts(argv):
	if argv['community'] == "private@1":
		return dot1BassNumPortsP1
	else :
		return dot1BassNumPortsP1

def bulkVmVlan(argv):
	result = []
	portL = [10101, 10102, 10103, 10104, 10105, 10106, 10107, 10108, 10109, 10110, 10111, 10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119, 10120, 10121, 10122, 10123, 10124, 10125, 10126, 10127, 10128, 10129, 10130, 10131, 10132]
	for i in portL:
		strOid = "1.3.6.1.4.1.9.9.68.1.2.2.1.2" + "." + str(i)
		value = portTable[str(i)]["VLANID"]
		oid_value = {"oid":strOid,"value":value}
		result.append(oid_value)
	return  result


def bulkVmVlan10132(argv):
	result = []
	portL = [10132, 10133, 10134, 10135, 10136, 10137, 10138, 10139, 10140, 10141, 10142, 10143, 10144, 10145, 10146, 10147, 10148, 10149,10150,10201,10202]
	for i in portL:
		strOid = "1.3.6.1.4.1.9.9.68.1.2.2.1.2" + "." + str(i)
		value = portTable[str(i)]["VLANID"]
		oid_value = {"oid":strOid,"value":value}
		result.append(oid_value)
	suf = [{'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10101', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10102', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10103', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10104', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10105', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10106', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10107', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10108', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10109', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10110', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10111', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10112', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10113', 'value': 2L}]
	for a in suf:
		result.append(a)
	return  result

def bulkIFDescr(argv):
	inOID = argv['snmpdata'][0]['oid']
	fetchData = mysql.bulkOID(inOID)
	result = []
	for i in fetchData:
		newItem = {}
		newItem['oid'] = str(i[1])
		try:
			newItem['value'] = long(i[2])
		except:
			newItem['value'] = str(i[2])
		result.append(newItem)
	print "bulkIFDescr()"
	return result

bulk_resp = {	"1.3.6.1.2.1.2.2.1.2":bulkIFDescr,
#		"1.3.6.1.2.1.2.2.1.2.10127":cisco_ifDescr_2,
		"1.3.6.1.4.1.9.9.46.1.3.1.1.4":bulkVlanNameTable,
		"1.3.6.1.4.1.9.9.68.1.2.2.1.2":bulkVmVlan,
		"1.3.6.1.4.1.9.9.68.1.2.2.1.2.10132":bulkVmVlan10132,
		"1.3.6.1.4.1.9.9.46.1.6.1.1.14":vlanTrunkPortDynamicStatus,
		"1.3.6.1.4.1.9.9.46.1.6.1.1.14.10132":vlanTrunkPortDynamicStatus2,
		"1.3.6.1.2.1.17.1.4.1.2":getDot1BassNumPorts,
		"1.3.6.1.2.1.17.1.4.1.2.32":dot1BassNumPorts36P1,
		"1.3.6.1.2.1.17.4.3":getdot1dTpFdbTable,
}

	
def SETvtpVlanEditOperation(prefix,last,value):
	oid = prefix+"."+last
	cswitch_attr[oid] = value
	print oid
	return cswitch_attr[oid]

def SETvtpVlanEditBufferOwner(prefix,last,value):
	oid = prefix + "." + last
	cswitch_attr[oid] = value
	print oid
	return cswitch_attr[oid]

from threading import Thread

def remote_set_vlan(mac,vName,vID,reset = False):
	sshXen.ssh_connect(mac,vName,vID,reset)



def SETvmVlan(prefix,last,value):
	oid = prefix + "." + last
	cswitch_attr[oid] = value
	vName = vtpVlanNameTable[str(value)]['VlanName']
	MAC = portTable[last]["MAC"]
	vlanID = value
	if vlanID == 1:
		reset = True
	else:
		reset = False
	if last == "10201":
		pass
	elif last == "10202":
		pass
	else:
		t = Thread(target = remote_set_vlan,args = (MAC,vName,vlanID,reset))
		t.start()
#	sshXen.ssh_connect(portTable[last]["MAC"],vName,value)
	print "value:" + str(value)+","+"vlanName:" + str(vName)+","+"portIndex:"+str(last)+","+"MAC:"+portTable[last]["MAC"]
	portTable[last]["VLANID"] = value
	return portTable[last]["VLANID"]

def SETifAdminStatus(prefix,last,value):
	oid = prefix + "." + last
	cswitch_attr[oid] = value
	portTable[last]["AdminStatus"] = value
	return portTable[last]["AdminStatus"]

def SETportAdminSpeed(prefix,lastTwo,lastFirst,value):
	oid = ".".join([prefix,lastTwo,lastFirst])
	cswitch_attr[oid] = value
	portTable[last]["AdminSpeed"] = value
	return cswitch_attr[oid]

def SETportDuplex(prefix,lastTwo,lastFirst,value):
	oid = ".".join([prefix,lastTwo,lastFirst])
	cswitch_attr[oid] = value
	portTable[lastFirst]["Duplex"] = value
	return cswitch_attr[oid]

#''' example:{102:{11:4,4:'36',3:1,1:\x00\x01\x87\x06}} '''


#11.1
def SETvtpVlanEditRowStatus(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		vtpVlanNameTable[lastFirst]['VlanEditRowStatus'] = value
	except:
		vtpVlanNameTable[lastFirst] = {}
		vtpVlanNameTable[lastFirst]['VlanEditRowStatus'] = value
		vtpVlanNameTable[lastFirst]['VlanMTU'] = 1500L
	cswitch_attr[oid] = value
	print vtpVlanNameTable
	return vtpVlanNameTable[lastFirst]['VlanEditRowStatus']
#3.1
def SETvtpVlanEditType(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		vtpVlanNameTable[lastFirst]['VlanEditType'] = value
	except:
		vtpVlanNameTable[lastFirst] = {}
		vtpVlanNameTable[lastFirst]['VlanEditType'] = value
		vtpVlanNameTable[lastFirst]['VlanMTU'] = 1500L
	cswitch_attr[oid] = value
	print vtpVlanNameTable
	return cswitch_attr[oid]
#4.1
def SETvtpVlanEditName(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		vtpVlanNameTable[lastFirst]['VlanName'] = value
	except:
		vtpVlanNameTable[lastFirst] = {}
		vtpVlanNameTable[lastFirst]['VlanName'] = value
		vtpVlanNameTable[lastFirst]['VlanMTU'] = 1500L
	cswitch_attr[oid] = value
	return cswitch_attr[oid]
#6.1
def SETvtpVlanEditDot10Said(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		vtpVlanNameTable[lastFirst]['VlanDot10Said'] = value
	except:
		vtpVlanNameTable[lastFirst] = {}
		vtpVlanNameTable[lastFirst]['VlanDot10Said'] = value
		vtpVlanNameTable[lastFirst]['VlanMTU'] = 1500L
	cswitch_attr[oid] = value
	return cswitch_attr[oid]

setFunctionLast = {
"1.3.6.1.4.1.9.9.46.1.4.1.1.1":SETvtpVlanEditOperation,
"1.3.6.1.4.1.9.9.46.1.4.1.1.3":SETvtpVlanEditBufferOwner,
"1.3.6.1.4.1.9.9.68.1.2.2.1.2":SETvmVlan,
"1.3.6.1.2.1.2.2.1.7":SETifAdminStatus,
# Vlan, VlanName
"1.3.6.1.4.1.9.9.46.1.4.2.1.11.1":SETvtpVlanEditRowStatus,
"1.3.6.1.4.1.9.9.46.1.4.2.1.3.1":SETvtpVlanEditType,
"1.3.6.1.4.1.9.9.46.1.4.2.1.4.1":SETvtpVlanEditName,
"1.3.6.1.4.1.9.9.46.1.4.2.1.6.1":SETvtpVlanEditDot10Said,
}

setFunctionLastTwo = {
"1.3.6.1.4.1.9.5.1.4.1.1.9.1":SETportAdminSpeed,
"1.3.6.1.4.1.9.5.1.4.1.1.10.1":SETportDuplex,
}


setFunction = {
}

def __setFunction(oid,value):
	sOid = oid.split(".")# split oid by "."
	lastA = sOid.pop()# save last num
	lastB = sOid.pop()# save second last num
	prefix = ".".join(sOid)# the original oid without last 2 numbers
	if prefix in setFunctionLastTwo.keys():# check prefix+B+A
		result = setFunctionLastTwo[prefix](prefix,lastB,lastA,value)
		return result
	prefix = prefix+"."+lastB
	if prefix in setFunctionLast.keys():# check prefixB+A
		result = setFunctionLast[prefix](prefix,lastA,value)
		return result
	prefix = prefix + "." + lastA
	try:# check prefixBA
		return setFunction[prefix](prefix,value)
	except:# else, return directly from the list table
		cswitch_attr[oid] = value
		return value


#def reply(snmpdata, community, function, xid, version, **kwargs):
def reply(kwargs):
	argv = {}
	argv['community'] = kwargs['community']
	argv['snmpdata'] = kwargs['snmpdata']
	argv['function'] = kwargs['function']
	argv['version'] = kwargs['version']
	if argv['function'] == "SNMPget":
		argv['error'] = kwargs['pdu']['error']
		argv['error_index'] = kwargs['pdu']['error_index']
		result = snmpGetValue(argv)
	elif argv['function'] == "SNMPset":
		argv['error'] = kwargs['pdu']['error']
		argv['error_index'] = kwargs['pdu']['error_index']
		result = snmpSetValue(argv)
	elif argv['function'] == "SNMPbulk":
		argv['max_repetitions'] = kwargs['pdu']['max_repetitions']
		argv['non_repeaters'] = kwargs['pdu']['non_repeaters']
		result = snmpBulkValue(argv)
	elif argv['function']== "SNMPnext":
		pass
	else:
		print "unknown snmp function"
		pass
#	result = oid_response_function_map[argv['snmpdata'][0]['oid']](argv)
	if result:
#	add "." in front of each oid ; change function to SNMPrespone		
		for oid in result['snmpdata']:
			oid['oid'] = "."+oid['oid']
		result['function'] = "SNMPresponse"
		result['pdu'] = kwargs['pdu']
		return result

def snmpGetValue(argv):
	a = argv
	if isinstance(a['snmpdata'],list):
		for oid in a['snmpdata']:
			try:
				oid['value']=cswitch_attr[oid['oid']]
			except:
				sOid = oid['oid'].split(".")
				p = sOid.pop()
				newOid = ".".join(sOid)
				try:
					oid['value'] = cswitch_attr[newOid](p)
				except:
					try:
						oid['value'] = cswitch_attr[newOid]
					except:
						oid['value'] = '' # meaningless 
	for o in a['snmpdata']:
		if o['oid'][0] == '.':
			o['oid'] = o['oid'][1:]
	return a



def snmpBulkValue(argv):
	a = argv
	fullOID = a['snmpdata'][0]['oid']
	newOID = popOID(fullOID)
	if a['snmpdata'][0]['oid'] in bulk_resp.keys():#check if the oid is in the bulkList
		try:
			b = bulk_resp[a['snmpdata'][0]['oid']](a)#try calling a function
			a['snmpdata'] = b
		except:
			a['snmpdata'] = bulk_resp[a['snmpdata'][0]['oid']]#try a hardcoded list
	elif newOID in bulk_resp.keys():
		try:
			b = bulk_resp[newOID](a)#try calling a function
			a['snmpdata'] = b
		except:
			a['snmpdata'] = bulk_resp[newOID]#try a hardcoded list
	elif a['snmpdata'][0]['oid'][0:18] == "1.3.6.1.2.1.17.4.3":# for MAC dot1TpFdbTable
		b = bulk_resp["1.3.6.1.2.1.17.4.3"](a)
		a['snmpdata'] = b
	for o in a['snmpdata']:# in case too much '.' insert in the head of OID
		if o['oid'][0] == '.':
			o['oid'] = o['oid'][1:]
	return a

def snmpSetValue(argv):
	if isinstance(argv['snmpdata'],list):
		for oid in argv['snmpdata']:
			oid['value'] = __setFunction(oid['oid'],oid['value'])
	for o in argv['snmpdata']:
		if o['oid'][0] == '.':
			o['oid'] = o['oid'][1:]
	return argv

def main():
	argv = {}
	if len(sys.argv) < 2:
		sys.exit("usage:python handler.py XXX XXX")
	else:
		#a complete command:$ python handler.py oid function xid(id) value 
		argv['oid'] = sys.argv[1]
		argv['function'] = sys.argv[2]
		argv['xid'] = sys.argv[3]
		argv['value'] = sys.argv[4]
		if sys.argv[2] == "SNMPget":
			argv['error'] = sys.argv[5]
			argv['error_index'] = sys.argv[6]
		elif sys.argv[2] == "SNMPset":
			pass
		elif sys.argv[2] == "SNMPbulk":
			argv['max_reptition'] = sys.argv[5]
			argv['non_repeaters'] = sys.argv[6]
		elif	sys.argv[2] == "SNMPnext":
			pass
		else:
			sys.exit("non-known function")
#	pprint(argv)
	oid_response_function_map[argv['oid']](argv)



if __name__ == "__main__":
	bulkIFDescr()
