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

def getLastNum(oid):
	oidList = []
	oidList = oid.split(".")
	last = oidList.pop()
	return last



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
	

def getvtpVlanName(lastFirst):
	result = mysql.getDBvtpVlanName(lastFirst)
	return result

def getvtpVlanEditRowStatus(lastFirst):
	try:
		result = mysql.getDBvtpVlanEditRowStatus(lastFirst)
	except:
		result = 4 #set default to status "createAndGo"
	return result

def getvtpVlanEditType(lastFirst):
	try:
		result = mysql.getDBvtpVlanEditType(lastFirst)
	except:
		result = 0
	return result

def getvtpVlanEditName(lastFirst):
	try:
		result = mysql.getDBvtpVlanName(lastFirst)
	except:
		result = '\x81\x00'
	return result

def getpVlanEditDot10Said(lastFirst):
	try:
		result = mysql.getDBvtpVlanDot10Said(lastFirst)
	except:
		result = '\x81'
	return result

def getPortTableAdminStatus(lastFirst):
	result = mysql.getDBAdminStatus(lastFirst)
	return result

def getVmVlan(lastFirst):
	result = mysql.getDBVmVlan(lastFirst)
	return result

def getSysDescr():
	mysql.deleteUnusedVlan() # clear unused Vlan when Boss invokes sysDescr
	SD = "Cisco IOS Software, Catalyst 4500 L3 Switch Software (cat4500e-ENTSERVICESK9-M), Version 12.2(54)SG, RELEASE SOFTWARE (fc3)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2010 by Cisco Systems, Inc.\r\nCompiled Sun 27-Jun-10 09:28"
	return SD

cswitch_attr = {
	"1.3.6.1.2.1.1.1.0": getSysDescr,	
	"1.3.6.1.4.1.9.9.46.1.4.1.1.3.1":"boss.ee.testbed.ncku.edu.tw",
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

}



def bulkVlanNameTable(argv):
	name = []
	mtu = []
	dot10said = []
	response = []
	a = mysql.getVlanNameList()  #vtpVlanNameTable.keys()
	b = []
	for i in a:
		b.append(int(i))
	b = sorted(b)
	for intKey in b:
		key = str(intKey)
		nameOID = ".".join(["1.3.6.1.4.1.9.9.46.1.3.1.1.4.1",key])
		mtuOID = ".".join(["1.3.6.1.4.1.9.9.46.1.3.1.1.5.1",key])
		d10saidOID = ".".join(["1.3.6.1.4.1.9.9.46.1.3.1.1.6.1",key])
#
		nameData = mysql.getVlanTableStr("VlanName",intKey)
		mtuData = mysql.getVlanTableLong("VlanMTU",intKey)
		d10saidData = mysql.getDBvtpVlanDot10Said(intKey)
#
		name.append({'oid':nameOID,'value':nameData})
		mtu.append({'oid':mtuOID,'value':mtuData})
		dot10said.append({'oid':d10saidOID,'value':d10saidData})
	response.extend(name)
	response.extend(mtu)
	response.extend(dot10said)
	response.extend(vtpVlanNameAppendix)
	return response[0:32]

def bulkVmVlan(argv):
	suf = [{'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.3', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.4', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.5', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.6', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.7', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.8', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.9', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.10', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.11', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.12', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.13', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.14', 'value': 2L},
              {'oid': '1.3.6.1.4.1.9.9.68.1.2.2.1.3.15', 'value': 2L}]
	result = []
	oid = argv["snmpdata"][0]["oid"]
	if ( oid == "1.3.6.1.4.1.9.9.68.1.2.2.1.2"):
		portL = mysql.getPortIndexList()
	else:
		l = oid.split(".")
		last = l.pop()
		portL = mysql.getPortIndexList(last)
	for i in portL:
		strOid = "1.3.6.1.4.1.9.9.68.1.2.2.1.2" + "." + str(i)
		value = mysql.getPortTableLong("vlanID",i)
		oid_value = {"oid":strOid,"value":value}
		result.append(oid_value)
	result.extend(suf)
	return  result[0:32]


def bulkIFDescr(argv):
	OID = argv['snmpdata'][0]['oid']
	s = [{'oid': '1.3.6.1.2.1.2.2.1.2.345', 'value': 'Null0'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.346', 'value': 'Vlan1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.347', 'value': 'unrouted VLAN 1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.348',
               'value': 'unrouted VLAN 1002'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.349',
               'value': 'unrouted VLAN 1004'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.350',
               'value': 'unrouted VLAN 1005'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.351',
               'value': 'unrouted VLAN 1003'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.352', 'value': 'Vlan2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.367', 'value': 'unrouted VLAN 2'},
	      {'oid': '1.3.6.1.2.1.2.2.1.3.2', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.3', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.4', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.5', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.6', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.7', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.8', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.9', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.10', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.11', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.12', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.13', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.14', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.15', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.16', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.17', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.18', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.19', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.20', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.21', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.22', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.23', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.24', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.25', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.26', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.27', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.28', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.29', 'value': 6L},
              {'oid': '1.3.6.1.2.1.2.2.1.3.30', 'value': 6L}]
	IFlist = mysql.bulkIFDescr()
	IFlist.extend(s)
	start = 0
	for i in range(len(IFlist)):
		if(OID == IFlist[i]["oid"]):
			start = i+1
			break
	return IFlist[start:start+32]

def bulkVlanTrunkPortDynamicStatus(argv):
#	it is a value of 2 with all those ports except 195 in real, can be consided combine with the MySQL tables 'ports'
	a = [{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.3","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.4","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.5","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.6","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.7","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.8","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.9","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.10","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.11","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.12","value":1L},
	{"oid":"1.3.6.1.4.1.9.9.46.1.6.1.1.15.13","value":1L},
	]
	oid = argv["snmpdata"][0]["oid"]
	head = 3
	if oid == "1.3.6.1.4.1.9.9.46.1.6.1.1.14":
		snmpdataList = []
		for i in range(head,head+32):
			snmpOid = {}
			snmpOid["oid"] = ".".join(["1.3.6.1.4.1.9.9.46.1.6.1.1.14",str(i)])
			snmpOid["value"] = 2L
			snmpdataList.append(snmpOid)
	else:
		head = int(getLastNum(oid))+1
		snmpdataList = []
		if head+32 > mysql.maxPort:
			end = mysql.maxPort+2
		else:
			end = head+32
		for i in range(head,end):
			snmpOid = {}
			snmpOid["oid"] = ".".join(["1.3.6.1.4.1.9.9.46.1.6.1.1.14",str(i)])
			snmpOid["value"] = 2L
			snmpdataList.append(snmpOid)
	snmpdataList.extend(a)
	return snmpdataList[0:32]

def bulkDot1TpFdbTable(argv):
	a = [
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.2','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.3','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.4','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.5','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.6','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.7','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.8','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.9','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.10','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.11','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.12','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.13','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.14','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.15','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.16','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.17','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.18','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.19','value':'0.0'},
	]
	OID = argv['snmpdata'][0]['oid']
	com = argv['community']
	comList = com.split("@")
	sVlan = comList.pop()
	oidList = mysql.bulkD1TPtable(sVlan)
	oidList.extend(a)
	start = 0
	for i in range(len(oidList)):
		if(OID == oidList[i]["oid"]):
			start = i+1
			break
	return oidList[start:start+32]

def bulkBassNumPorts(argv):
	a = [
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.2','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.3','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.4','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.5','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.6','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.7','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.8','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.9','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.10','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.11','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.12','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.13','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.14','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.15','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.16','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.17','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.18','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.19','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.20','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.21','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.22','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.23','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.24','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.25','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.26','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.27','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.28','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.29','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.30','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.31','value':'0.0'},
	{'oid':'1.3.6.1.2.1.17.1.4.1.3.32','value':'0.0'},
	]
	OID = argv['snmpdata'][0]['oid']
	com = argv['community']
	comList = com.split("@")
	sVlan = comList.pop()
	oidList = mysql.bulkBassNum(sVlan)
	oidList.extend(a)
	start = 0
	for i in range(len(oidList)):
		if(OID == oidList[i]["oid"]):
			start = i+1
			break
	return oidList[start:start+32]


bulk_resp = {	"1.3.6.1.2.1.2.2.1.2":bulkIFDescr,
		"1.3.6.1.4.1.9.9.46.1.3.1.1.4":bulkVlanNameTable,
		"1.3.6.1.4.1.9.9.68.1.2.2.1.2":bulkVmVlan,
		"1.3.6.1.4.1.9.9.46.1.6.1.1.14":bulkVlanTrunkPortDynamicStatus,
		"1.3.6.1.2.1.17.1.4.1.2":bulkBassNumPorts,
		"1.3.6.1.2.1.17.4.3":bulkDot1TpFdbTable,
}

	
def SETvtpVlanEditOperation(prefix,last,value):
	oid = prefix+"."+last
	cswitch_attr[oid] = value
	return cswitch_attr[oid]

def SETvtpVlanEditBufferOwner(prefix,last,value):
	oid = prefix + "." + last
	cswitch_attr[oid] = value
	return cswitch_attr[oid]

from threading import Thread

def remote_set_vlan(mac,vName,vID,reset = False):
	sshXen.ssh_connect(mac,vName,vID,reset)



def SETvmVlan(prefix,last,value):
	oid = prefix + "." + last
#	cswitch_attr[oid] = value
	vName = mysql.getDBvtpVlanName(value)
	MAC = mysql.getPortTableStr("MAC",last)
	vlanID = value
	if vlanID == 1:
		reset = True
		mysql.resetDBVmVlan(last,vlanID)
	else:
		reset = False
		mysql.setDBVmVlan(last,vlanID)

	if last == "10201":
		pass
	elif last == "10202":
		pass
	else:
		t = Thread(target = remote_set_vlan,args = (MAC,vName,vlanID,reset))
		t.start()
	return value

def SETifAdminStatus(prefix,last,value):
	oid = prefix + "." + last
#	cswitch_attr[oid] = value
	mysql.setDBAdminStatus(last,value)
	return value

def SETportAdminSpeed(prefix,lastTwo,lastFirst,value):
	oid = ".".join([prefix,lastTwo,lastFirst])
#	cswitch_attr[oid] = value
	mysql.setDBAdminSpeed(lastFirst,value)
	return value

def SETportDuplex(prefix,lastTwo,lastFirst,value):
	oid = ".".join([prefix,lastTwo,lastFirst])
#	cswitch_attr[oid] = value
	mysql.setDBDuplex(lastFirst,value)
	return value

#''' example:{102:{11:4,4:'36',3:1,1:\x00\x01\x87\x06}} '''


#11.1
def SETvtpVlanEditRowStatus(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		mysql.setDBvtpVlanEditRowStatus(lastFirst,value)
	except:
		pass
#	cswitch_attr[oid] = value
	return value 

#3.1
def SETvtpVlanEditType(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		mysql.setDBvtpVlanEditType(lastFirst,value)
	except:
		pass
#	cswitch_attr[oid] = value
	return value
#4.1
def SETvtpVlanEditName(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		mysql.setDBvtpVlanName(lastFirst,value)
	except:
		pass
#	cswitch_attr[oid] = value
	return value
#6.1
def SETvtpVlanEditDot10Said(prefix,lastFirst,value):
	oid = ".".join([prefix,lastFirst])
	try:
		mysql.setDBvtpVlanDot10Said(lastFirst,value)
	except:
		pass
#	cswitch_attr[oid] = value
	return value

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
				oid['value']=cswitch_attr[oid['oid']]()
			except:
				try:
					oid['value']=cswitch_attr[oid['oid']]#directly from the list
				except:
					sOid = oid['oid'].split(".")
					p = sOid.pop()
					newOid = ".".join(sOid)#pop the last num 
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
	oid_response_function_map[argv['oid']](argv)



if __name__ == "__main__":
	bulkIFDescr()
