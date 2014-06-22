import MySQLdb
import time
from pprint import pprint
from MySQLdb.cursors import SSCursor
import collections
import pw

maxSlot = 2
maxPort = 48*maxSlot + 1

def connectDB():
	conn = MySQLdb.connect(	host = pw.host,
				db = pw.db_table,
				user = pw.user,
				passwd = pw.passwd,
				charset = pw.charset)	
	return conn

def DBVersion():
	c = connectDB()
	cursor = c.cursor()
	cursor.execute("SELECT VERSION()")
	ver = cursor.fetchone()
	print ver
	if c:
		c.close()

def resetVlanTable():
	c = connectDB()
	cursor = c.cursor()
	cursor.execute("DROP TABLE IF EXISTS vlans")
	query = """
		CREATE TABLE vlans(
			id INT,
			VlanId INT,
			VlanName Varchar(20),
			VlanEditType INT,
			VlanMTU INT,
			VlanDot10Said0 INT,
			VlanDot10Said1 INT,
			VlanDot10Said2 INT,
			VlanDot10Said3 INT,
			VlanEditRowStatus INT,
			counts	INT,
			permanent INT
		);

		"""
	cursor.execute(query)
	c.commit()
	c.close()

def initialVlanTable():
	vtpVlanNameTable = [
	{'VlanID':1,'VlanName':'default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x86\xa1','VlanEditRowStatus':4},
	{'VlanID':2,'VlanName':'Control-Hardware','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x86\xa2','VlanEditRowStatus':4},
	{'VlanID':1002,'VlanName':'fddi-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8a','VlanEditRowStatus':4},
	{'VlanID':1003,'VlanName':'token-ring-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8b','VlanEditRowStatus':4},
	{'VlanID':1004,'VlanName':'fddinet-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8c','VlanEditRowStatus':4},
	{'VlanID':1005,'VlanName':'trnet-default','VlanMTU':1500L,'VlanDot10Said':'\x00\x01\x8a\x8d','VlanEditRowStatus':4},
	]
	c = connectDB()
	cursor = c.cursor()
	for k in vtpVlanNameTable:
		query = "INSERT INTO vlans(VlanID, VlanName, VlanEditType, VlanMTU, VlanDot10Said0,VlanDot10Said1,VlanDot10Said2,VlanDot10Said3, VlanEditRowStatus,counts,permanent ) VALUES(%s, '%s', 2, %s, %s,%s,%s,%s, %s, 0, 1);" % (k['VlanID'],k['VlanName'],k['VlanMTU'],str(ord(k['VlanDot10Said'][0])),str(ord(k['VlanDot10Said'][1])),str(ord(k['VlanDot10Said'][2])),str(ord(k['VlanDot10Said'][3])),k['VlanEditRowStatus'])
		cursor.execute(query)
	c.commit()
	c.close()

def resetPortTable():
	c = connectDB()
	cursor = c.cursor()
	cursor.execute("DROP TABLE IF EXISTS ports")
	qCreate = """	CREATE TABLE ports(
			id INT,
			portIndex INT,
			portNum INT,
			portName VARCHAR(30),
			MAC VARCHAR(20),
			vlanID INT,
			AdminStatus TINYINT,
			Duplex TINYINT,
			AdminSpeed INT,
			createDate DATETIME,
			modifiedTime DATETIME)
		"""
	cursor.execute(qCreate)
	c.commit()
	c.close()


def addPorts	(id, 
		portIndex,
		portNum, 
		portName, 
		MAC, 
		vlanID = 1, 
		AdminStatus = 0, 
		Duplex = 2, 
		AdminSpeed = 100000000L
		):

	c = connectDB()
	cursor = c.cursor()
	qAddPort_1 = """	
			INSERT INTO ports(
			id,
			portIndex,
			portNum,
			portName,
			MAC,
			vlanID,
			AdminStatus,
			Duplex,
			AdminSpeed,
			createDate,
			modifiedTime) VALUES(
		"""
	qAddPort_2 = str(id) +","+ str(portIndex) +","+ str(portNum) +",\""+ portName +"\",\""+ MAC +"\","+ str(vlanID) +","+ str(AdminStatus) +","+ str(Duplex) +","+ str(AdminSpeed) + ", NOW(), NOW())"
	qAdd = qAddPort_1 + qAddPort_2
	cursor.execute(qAdd)
	c.commit()
	c.close()

def newPortQuery(	id, 
			portIndex,
			portNum, 
			portName, 
			MAC, 
			vlanID = 1, 
			AdminStatus = 2, 
			Duplex = 2, 
			AdminSpeed = 100000000L
		):
	qAddPort_1 = """	
			INSERT INTO ports(
			id,
			portIndex,
			portNum,
			portName,
			MAC,
			vlanID,
			AdminStatus,
			Duplex,
			AdminSpeed,
			createDate,
			modifiedTime) VALUES(
		"""
	qAddPort_2 = str(id) +","+ str(portIndex) +","+ str(portNum) +",\""+ portName +"\",\""+ MAC +"\","+ str(vlanID) +","+ str(AdminStatus) +","+ str(Duplex) +","+ str(AdminSpeed) + ", NOW(), NOW())"
	qAdd = qAddPort_1 + qAddPort_2
	return qAdd

def initialPortTable():
	c = connectDB()
	cursor = c.cursor()
	MAX_PORT_NUMBER = 344
	s = 1
	p = 1
	slot = 1
	cursor.execute(newPortQuery(2,2,2,"FastEthernet1","00:16:3e:01:00:99"))
	for i in range(3,maxPort+2):
#		if p == 49:
#			s+=1
#			p = 1
#		if s == 6:
#			s+=1
#		if s == 5 and p == 1:
#			p_name = "TenGigabitEthernet"+str(s)+"/"+str(p)
#		elif s == 5 and p == 2:
#			p_name = "TenGigabitEthernet"+str(s)+"/"+str(p)
#		else:
#			p_name = "GigabitEthernet"+str(s)+"/"+str(p)
#		if s == 5 and p == 6:
#			s = 7
#			p = 0'''
		p_name = "GigabitEthernet"+str(slot)+"/"+str(p)
		p_id = i
		p_index = i
		p_num = i	
		p_MAC = "00:16:3e:01:" +format(slot,'02x')+ ":" + format(p,'02x')
		cursor.execute(newPortQuery(p_id,p_index,p_num,p_name,p_MAC))
		p+=1
		if ( p == 49 ):
			p = 1
			slot += 1
	c.commit()
	c.close()

def editPTKeyValue(portIndex, key, value):
	c = connectDB()
	cursor = c.cursor()
	qUpdate = "UPDATE ports SET "+str(key)+" = '"+str(value)+"' WHERE portIndex = '"+str(portIndex)+"'"
	cursor.execute(qUpdate)
	qUpdate = "UPDATE ports SET modifiedTime = NOW() WHERE portIndex = '"+str(portIndex)+"'"
	cursor.execute(qUpdate)
	c.commit()
	c.close()

def getVtpVlanNameTable():
	VNT = {}
	c = connectDB()
	cursor = c.cursor()
	query = "SELECT * From vlans"
	cursor.execute(query)
	result = cursor.fetchall()
	for i in result:	
		vlanItem = {}
		vlanItem['VlanID'] = i[1]
		vlanItem['VlanName'] = i[2].encode('utf-8')
		vlanItem['VlanMTU'] = i[3]
		vlanItem['VlanDot10Said'] = chr(i[4])+chr(i[5])+chr(i[6])+chr(i[7])
		vlanItem['VlanEditRowStatus'] = i[8]
		VNT[int(i[1])] = vlanItem
	c.commit()
	c.close()


def initOIDTable():
	c = connectDB()
	cursor = c.cursor()
	cursor.execute("DROP TABLE IF EXISTS OIDs")
	id = 0
	initOIDTable = [{'oid': '1.3.6.1.2.1.2.2.1.2.2', 'value': 'FastEthernet1'},
              	{'oid': '1.3.6.1.2.1.2.2.1.2.3', 'value': 'GigabitEthernet1/1'},
              	{'oid': '1.3.6.1.2.1.2.2.1.2.4', 'value': 'GigabitEthernet1/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.5', 'value': 'GigabitEthernet1/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.6', 'value': 'GigabitEthernet1/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.7', 'value': 'GigabitEthernet1/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.8', 'value': 'GigabitEthernet1/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.9', 'value': 'GigabitEthernet1/7'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.10',
               'value': 'GigabitEthernet1/8'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.11',
               'value': 'GigabitEthernet1/9'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.12',
               'value': 'GigabitEthernet1/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.13',
               'value': 'GigabitEthernet1/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.14',
               'value': 'GigabitEthernet1/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.15',
               'value': 'GigabitEthernet1/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.16',
               'value': 'GigabitEthernet1/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.17',
               'value': 'GigabitEthernet1/15'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.18',
               'value': 'GigabitEthernet1/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.19',
               'value': 'GigabitEthernet1/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.20',
               'value': 'GigabitEthernet1/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.21',
               'value': 'GigabitEthernet1/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.22',
               'value': 'GigabitEthernet1/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.23',
               'value': 'GigabitEthernet1/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.24',
               'value': 'GigabitEthernet1/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.25',
               'value': 'GigabitEthernet1/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.26',
               'value': 'GigabitEthernet1/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.27',
               'value': 'GigabitEthernet1/25'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.28',
               'value': 'GigabitEthernet1/26'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.29',
               'value': 'GigabitEthernet1/27'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.30',
               'value': 'GigabitEthernet1/28'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.31',
               'value': 'GigabitEthernet1/29'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.32',
               'value': 'GigabitEthernet1/30'},
              	{'oid': '1.3.6.1.2.1.2.2.1.2.33',
               'value': 'GigabitEthernet1/31'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.34',
               'value': 'GigabitEthernet1/32'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.35',
               'value': 'GigabitEthernet1/33'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.36',
               'value': 'GigabitEthernet1/34'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.37',
               'value': 'GigabitEthernet1/35'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.38',
               'value': 'GigabitEthernet1/36'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.39',
               'value': 'GigabitEthernet1/37'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.40',
               'value': 'GigabitEthernet1/38'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.41',
               'value': 'GigabitEthernet1/39'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.42',
               'value': 'GigabitEthernet1/40'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.43',
               'value': 'GigabitEthernet1/41'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.44',
               'value': 'GigabitEthernet1/42'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.45',
               'value': 'GigabitEthernet1/43'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.46',
               'value': 'GigabitEthernet1/44'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.47',
               'value': 'GigabitEthernet1/45'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.48',
               'value': 'GigabitEthernet1/46'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.49',
               'value': 'GigabitEthernet1/47'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.50',
               'value': 'GigabitEthernet1/48'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.51',
               'value': 'GigabitEthernet2/1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.52',
               'value': 'GigabitEthernet2/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.53',
               'value': 'GigabitEthernet2/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.54',
               'value': 'GigabitEthernet2/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.55',
               'value': 'GigabitEthernet2/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.56',
               'value': 'GigabitEthernet2/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.57',
               'value': 'GigabitEthernet2/7'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.58',
               'value': 'GigabitEthernet2/8'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.59',
               'value': 'GigabitEthernet2/9'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.60',
               'value': 'GigabitEthernet2/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.61',
               'value': 'GigabitEthernet2/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.62',
               'value': 'GigabitEthernet2/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.63',
               'value': 'GigabitEthernet2/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.64',
               'value': 'GigabitEthernet2/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.65',
               'value': 'GigabitEthernet2/15'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.66',
               'value': 'GigabitEthernet2/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.67',
               'value': 'GigabitEthernet2/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.68',
               'value': 'GigabitEthernet2/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.69',
               'value': 'GigabitEthernet2/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.70',
               'value': 'GigabitEthernet2/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.71',
               'value': 'GigabitEthernet2/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.72',
               'value': 'GigabitEthernet2/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.73',
               'value': 'GigabitEthernet2/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.74',
               'value': 'GigabitEthernet2/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.75',
               'value': 'GigabitEthernet2/25'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.76',
               'value': 'GigabitEthernet2/26'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.77',
               'value': 'GigabitEthernet2/27'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.78',
               'value': 'GigabitEthernet2/28'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.79',
               'value': 'GigabitEthernet2/29'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.80',
               'value': 'GigabitEthernet2/30'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.81',
               'value': 'GigabitEthernet2/31'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.82',
               'value': 'GigabitEthernet2/32'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.83',
               'value': 'GigabitEthernet2/33'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.84',
               'value': 'GigabitEthernet2/34'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.85',
               'value': 'GigabitEthernet2/35'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.86',
               'value': 'GigabitEthernet2/36'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.87',
               'value': 'GigabitEthernet2/37'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.88',
               'value': 'GigabitEthernet2/38'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.89',
               'value': 'GigabitEthernet2/39'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.90',
               'value': 'GigabitEthernet2/40'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.91',
               'value': 'GigabitEthernet2/41'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.92',
               'value': 'GigabitEthernet2/42'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.93',
               'value': 'GigabitEthernet2/43'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.94',
               'value': 'GigabitEthernet2/44'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.95',
               'value': 'GigabitEthernet2/45'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.96',
               'value': 'GigabitEthernet2/46'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.97',
               'value': 'GigabitEthernet2/47'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.98',
               'value': 'GigabitEthernet2/48'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.99',
               'value': 'GigabitEthernet3/1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.100',
               'value': 'GigabitEthernet3/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.101',
               'value': 'GigabitEthernet3/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.102',
               'value': 'GigabitEthernet3/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.103',
               'value': 'GigabitEthernet3/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.104',
               'value': 'GigabitEthernet3/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.105',
               'value': 'GigabitEthernet3/7'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.106',
               'value': 'GigabitEthernet3/8'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.107',
               'value': 'GigabitEthernet3/9'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.108',
               'value': 'GigabitEthernet3/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.109',
               'value': 'GigabitEthernet3/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.110',
               'value': 'GigabitEthernet3/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.111',
               'value': 'GigabitEthernet3/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.112',
               'value': 'GigabitEthernet3/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.113',
               'value': 'GigabitEthernet3/15'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.114',
               'value': 'GigabitEthernet3/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.115',
               'value': 'GigabitEthernet3/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.116',
               'value': 'GigabitEthernet3/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.117',
               'value': 'GigabitEthernet3/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.118',
               'value': 'GigabitEthernet3/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.119',
               'value': 'GigabitEthernet3/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.120',
               'value': 'GigabitEthernet3/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.121',
               'value': 'GigabitEthernet3/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.122',
               'value': 'GigabitEthernet3/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.123',
               'value': 'GigabitEthernet3/25'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.124',
               'value': 'GigabitEthernet3/26'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.125',
               'value': 'GigabitEthernet3/27'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.126',
               'value': 'GigabitEthernet3/28'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.127',
               'value': 'GigabitEthernet3/29'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.128',
               'value': 'GigabitEthernet3/30'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.129',
               'value': 'GigabitEthernet3/31'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.130',
               'value': 'GigabitEthernet3/32'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.131',
               'value': 'GigabitEthernet3/33'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.132',
               'value': 'GigabitEthernet3/34'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.133',
               'value': 'GigabitEthernet3/35'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.134',
               'value': 'GigabitEthernet3/36'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.135',
               'value': 'GigabitEthernet3/37'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.136',
               'value': 'GigabitEthernet3/38'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.137',
               'value': 'GigabitEthernet3/39'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.138',
               'value': 'GigabitEthernet3/40'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.139',
               'value': 'GigabitEthernet3/41'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.140',
               'value': 'GigabitEthernet3/42'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.141',
               'value': 'GigabitEthernet3/43'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.142',
               'value': 'GigabitEthernet3/44'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.143',
               'value': 'GigabitEthernet3/45'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.144',
               'value': 'GigabitEthernet3/46'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.145',
               'value': 'GigabitEthernet3/47'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.146',
               'value': 'GigabitEthernet3/48'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.147',
               'value': 'GigabitEthernet4/1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.148',
               'value': 'GigabitEthernet4/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.149',
               'value': 'GigabitEthernet4/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.150',
               'value': 'GigabitEthernet4/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.151',
               'value': 'GigabitEthernet4/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.152',
               'value': 'GigabitEthernet4/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.153',
               'value': 'GigabitEthernet4/7'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.154',
               'value': 'GigabitEthernet4/8'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.155',
               'value': 'GigabitEthernet4/9'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.156',
               'value': 'GigabitEthernet4/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.157',
               'value': 'GigabitEthernet4/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.158',
               'value': 'GigabitEthernet4/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.159',
               'value': 'GigabitEthernet4/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.160',
               'value': 'GigabitEthernet4/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.161',
               'value': 'GigabitEthernet4/15'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.162',
               'value': 'GigabitEthernet4/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.163',
               'value': 'GigabitEthernet4/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.164',
               'value': 'GigabitEthernet4/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.165',
               'value': 'GigabitEthernet4/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.166',
               'value': 'GigabitEthernet4/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.167',
               'value': 'GigabitEthernet4/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.168',
               'value': 'GigabitEthernet4/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.169',
               'value': 'GigabitEthernet4/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.170',
               'value': 'GigabitEthernet4/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.171',
               'value': 'GigabitEthernet4/25'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.172',
               'value': 'GigabitEthernet4/26'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.173',
               'value': 'GigabitEthernet4/27'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.174',
               'value': 'GigabitEthernet4/28'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.175',
               'value': 'GigabitEthernet4/29'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.176',
               'value': 'GigabitEthernet4/30'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.177',
               'value': 'GigabitEthernet4/31'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.178',
               'value': 'GigabitEthernet4/32'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.179',
               'value': 'GigabitEthernet4/33'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.180',
               'value': 'GigabitEthernet4/34'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.181',
               'value': 'GigabitEthernet4/35'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.182',
               'value': 'GigabitEthernet4/36'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.183',
               'value': 'GigabitEthernet4/37'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.184',
               'value': 'GigabitEthernet4/38'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.185',
               'value': 'GigabitEthernet4/39'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.186',
               'value': 'GigabitEthernet4/40'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.187',
               'value': 'GigabitEthernet4/41'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.188',
               'value': 'GigabitEthernet4/42'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.189',
               'value': 'GigabitEthernet4/43'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.190',
               'value': 'GigabitEthernet4/44'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.191',
               'value': 'GigabitEthernet4/45'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.192',
               'value': 'GigabitEthernet4/46'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.193',
               'value': 'GigabitEthernet4/47'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.194',
               'value': 'GigabitEthernet4/48'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.195',
               'value': 'TenGigabitEthernet5/1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.196',
               'value': 'TenGigabitEthernet5/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.197',
               'value': 'GigabitEthernet5/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.198',
               'value': 'GigabitEthernet5/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.199',
               'value': 'GigabitEthernet5/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.200',
               'value': 'GigabitEthernet5/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.201',
               'value': 'GigabitEthernet7/1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.202',
               'value': 'GigabitEthernet7/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.203',
               'value': 'GigabitEthernet7/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.204',
               'value': 'GigabitEthernet7/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.205',
               'value': 'GigabitEthernet7/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.206',
               'value': 'GigabitEthernet7/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.207',
               'value': 'GigabitEthernet7/7'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.208',
               'value': 'GigabitEthernet7/8'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.209',
               'value': 'GigabitEthernet7/9'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.210',
               'value': 'GigabitEthernet7/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.211',
               'value': 'GigabitEthernet7/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.212',
               'value': 'GigabitEthernet7/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.213',
               'value': 'GigabitEthernet7/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.214',
               'value': 'GigabitEthernet7/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.215',
               'value': 'GigabitEthernet7/15'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.216',
               'value': 'GigabitEthernet7/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.217',
               'value': 'GigabitEthernet7/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.218',
               'value': 'GigabitEthernet7/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.219',
               'value': 'GigabitEthernet7/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.220',
               'value': 'GigabitEthernet7/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.221',
               'value': 'GigabitEthernet7/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.222',
               'value': 'GigabitEthernet7/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.223',
               'value': 'GigabitEthernet7/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.224',
               'value': 'GigabitEthernet7/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.225',
               'value': 'GigabitEthernet7/25'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.258',
               'value': 'GigabitEthernet8/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.259',
               'value': 'GigabitEthernet8/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.260',
               'value': 'GigabitEthernet8/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.261',
               'value': 'GigabitEthernet8/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.262',
               'value': 'GigabitEthernet8/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.263',
               'value': 'GigabitEthernet8/15'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.264',
               'value': 'GigabitEthernet8/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.265',
               'value': 'GigabitEthernet8/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.266',
               'value': 'GigabitEthernet8/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.267',
               'value': 'GigabitEthernet8/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.268',
               'value': 'GigabitEthernet8/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.269',
               'value': 'GigabitEthernet8/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.270',
               'value': 'GigabitEthernet8/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.271',
               'value': 'GigabitEthernet8/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.272',
               'value': 'GigabitEthernet8/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.273',
               'value': 'GigabitEthernet8/25'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.274',
               'value': 'GigabitEthernet8/26'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.275',
               'value': 'GigabitEthernet8/27'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.276',
               'value': 'GigabitEthernet8/28'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.277',
               'value': 'GigabitEthernet8/29'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.278',
               'value': 'GigabitEthernet8/30'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.279',
               'value': 'GigabitEthernet8/31'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.280',
               'value': 'GigabitEthernet8/32'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.281',
               'value': 'GigabitEthernet8/33'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.282',
               'value': 'GigabitEthernet8/34'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.283',
               'value': 'GigabitEthernet8/35'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.284',
               'value': 'GigabitEthernet8/36'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.285',
               'value': 'GigabitEthernet8/37'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.286',
               'value': 'GigabitEthernet8/38'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.287',
               'value': 'GigabitEthernet8/39'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.288',
               'value': 'GigabitEthernet8/40'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.289',
               'value': 'GigabitEthernet8/41'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.290',
               'value': 'GigabitEthernet8/42'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.291',
               'value': 'GigabitEthernet8/43'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.292',
               'value': 'GigabitEthernet8/44'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.293',
               'value': 'GigabitEthernet8/45'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.294',
               'value': 'GigabitEthernet8/46'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.295',
               'value': 'GigabitEthernet8/47'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.296',
               'value': 'GigabitEthernet8/48'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.297',
               'value': 'GigabitEthernet9/1'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.298',
               'value': 'GigabitEthernet9/2'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.299',
               'value': 'GigabitEthernet9/3'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.300',
               'value': 'GigabitEthernet9/4'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.301',
               'value': 'GigabitEthernet9/5'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.302',
               'value': 'GigabitEthernet9/6'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.303',
               'value': 'GigabitEthernet9/7'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.304',
               'value': 'GigabitEthernet9/8'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.305',
               'value': 'GigabitEthernet9/9'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.306',
               'value': 'GigabitEthernet9/10'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.307',
               'value': 'GigabitEthernet9/11'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.308',
               'value': 'GigabitEthernet9/12'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.309',
               'value': 'GigabitEthernet9/13'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.310',
               'value': 'GigabitEthernet9/14'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.311',
               'value': 'GigabitEthernet9/15'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.312',
               'value': 'GigabitEthernet9/16'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.313',
               'value': 'GigabitEthernet9/17'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.314',
               'value': 'GigabitEthernet9/18'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.315',
               'value': 'GigabitEthernet9/19'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.316',
               'value': 'GigabitEthernet9/20'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.317',
               'value': 'GigabitEthernet9/21'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.318',
               'value': 'GigabitEthernet9/22'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.319',
               'value': 'GigabitEthernet9/23'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.320',
               'value': 'GigabitEthernet9/24'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.321',
               'value': 'GigabitEthernet9/25'},
	      {'oid': '1.3.6.1.2.1.2.2.1.2.322',
               'value': 'GigabitEthernet9/26'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.323',
               'value': 'GigabitEthernet9/27'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.324',
               'value': 'GigabitEthernet9/28'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.325',
               'value': 'GigabitEthernet9/29'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.326',
               'value': 'GigabitEthernet9/30'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.327',
               'value': 'GigabitEthernet9/31'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.328',
               'value': 'GigabitEthernet9/32'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.329',
               'value': 'GigabitEthernet9/33'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.330',
               'value': 'GigabitEthernet9/34'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.331',
               'value': 'GigabitEthernet9/35'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.332',
               'value': 'GigabitEthernet9/36'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.333',
               'value': 'GigabitEthernet9/37'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.334',
               'value': 'GigabitEthernet9/38'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.335',
               'value': 'GigabitEthernet9/39'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.336',
               'value': 'GigabitEthernet9/40'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.337',
               'value': 'GigabitEthernet9/41'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.338',
               'value': 'GigabitEthernet9/42'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.339',
               'value': 'GigabitEthernet9/43'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.340',
               'value': 'GigabitEthernet9/44'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.341',
               'value': 'GigabitEthernet9/45'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.342',
               'value': 'GigabitEthernet9/46'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.343',
               'value': 'GigabitEthernet9/47'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.344',
               'value': 'GigabitEthernet9/48'},
              {'oid': '1.3.6.1.2.1.2.2.1.2.345', 'value': 'Null0'},
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
              {'oid': '1.3.6.1.2.1.2.2.1.3.30', 'value': 6L},
	      {'oid': '1.3.6.1.2.1.2.2.1.3.31', 'value': 6L},
	      {'oid': '1.3.6.1.2.1.2.2.1.3.32', 'value': 6L},
	      {'oid': '1.3.6.1.2.1.2.2.1.3.33', 'value': 6L}]

	query = "CREATE TABLE OIDs (id INT, oid VARCHAR(50),value VARCHAR(30))"
	cursor.execute(query)
	queryInsert = "insert into OIDs (id,oid,value)VALUES"
	
	for item in initOIDTable:
		oid_value = "("+str(id)+",\""+str(item['oid'])+"\",\""+str(item['value'])+"\"),"
		queryInsert = queryInsert+oid_value
		id+=1
	queryInsert = queryInsert[0:-1]
	cursor.execute(queryInsert)
	c.commit()
	c.close()

def bulkIFDescr():
	c = connectDB()
	cursor = c.cursor()
	query = "select portIndex,portName from ports LIMIT "+str(maxPort)+";"
	try:
		IFDescr = []
		cursor.execute(query)
		fdata = cursor.fetchall()
		for row in fdata:
			i = {}
			oid = "1.3.6.1.2.1.2.2.1.2."+str(row[0])
			value = str(row[1])
			i["oid"] = oid
			i["value"] = value
			IFDescr.append(i)
		return IFDescr
	except:
		print "Error:bulkIFDescr"

def bulkOID(oid):
	c = connectDB()
	cursor = c.cursor()
	lookupQuery = "select * from OIDs WHERE oid = \'"+str(oid)+"\' LIMIT 1;"
	try:
		cursor.execute(lookupQuery)
		foundRow = cursor.fetchall()
		if not foundRow:
#			newOID = oid + ".1"
			lookupQuery2 = "select * from OIDs LIMIT 32;"
			cursor.execute(lookupQuery2)
			foundRow = cursor.fetchall()
			return foundRow
	except:
		print "Error occured in bulkOID()"
	if foundRow:
		foundID = foundRow[0][0]
		fQuery = "select * from OIDs where id > "+str(foundID)+" LIMIT 32;"
		cursor.execute(fQuery)
		result = cursor.fetchall()
	c.commit()
	c.close()
	return result

def setDBvtpVlanEditRowStatus(last,value):
	c = connectDB()
	cursor = c.cursor()
	#check if VLANID, last, is already in the 'vlans' table
	lookupQuery = "SELECT * FROM vlans WHERE VlanId = \'"+str(last)+"\';"
	try:
		cursor.execute(lookupQuery)
		foundRow = cursor.fetchall()
	except:
		print "Error in mysql.setDBvtpVlanEditRowStatus(),lookup"
	if not foundRow:
		#vlanID 'last' not exists, insert a new Row into table 'vlans'
		insertQuery = "INSERT into vlans (VlanId, VlanMTU, VlanEditRowStatus,counts,permanent) VALUES("+str(last)+","+str(1500)+","+str(value)+", 0, 0);"
		try:
			cursor.execute(insertQuery)
		except:
			print "Error in mysql.setDBvtpVlanEditRowStatus,insertQuery"
	else:
		#vlanID already exists,update VlanEditRowStatus
		updateQuery = "UPDATE vlans SET VlanMTU = 1500, VlanEditRowStatus = "+str(value)+" WHERE VlanId = '"+str(last)+"';"
		try:
			cursor.execute(updateQuery)
		except:
			print "Error in mysql.setDBvtpVlanEditRowStatus,updateQuery"
	c.commit()
	c.close()

def getDBvtpVlanEditRowStatus(last):
	c = connectDB()
	cursor = c.cursor()
	query = "select VlanEditRowStatus from vlans where VlanId = '"+str(last)+"';"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		result = long(data[0])
		c.commit()
		c.close()
		return result
	except:
		print "Error in getVlanEditRowStatus"
		c.commit()
		c.close()
		return 0L
	
def setDBvtpVlanName(last,value):
	c = connectDB()
	cursor = c.cursor()
	#check if VLANID, last, is already in the 'vlans' table
	lookupQuery = "SELECT * FROM vlans WHERE VlanId = \'"+str(last)+"\';"
	try:
		cursor.execute(lookupQuery)
		foundRow = cursor.fetchall()
	except:
		print "Error in mysql.setDBvtpVlanName(),lookup"
	if not foundRow:
		#vlanID 'last' not exists, insert a new Row into table 'vlans'
		insertQuery = "INSERT into vlans (VlanId, VlanMTU, VlanName,counts, permanent) VALUES("+str(last)+","+str(1500)+",'"+str(value)+"',0,0);"
		try:
			cursor.execute(insertQuery)
		except:
			print "Error in mysql.setDBvtpVlanName,insertQuery"
	else:
		#vlanID already exists,update VlanName
		updateQuery = "UPDATE vlans SET VlanMTU = 1500, VlanName = '"+str(value)+"' WHERE VlanId = '"+str(last)+"';"
		try:
			cursor.execute(updateQuery)
		except:
			print "Error in mysql.setDBvtpVlanName,updateQuery"
	c.commit()
	c.close()

def getDBvtpVlanName(vlanID):
	c = connectDB()
	cursor = c.cursor()
	query = "select VlanName from vlans where VlanId ='"+str(vlanID)+"';"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		vlanName = data[0]
		c.commit()
		c.close()
		return str(vlanName)
	except:
		c.commit()
		c.close()
		return ""

def setDBvtpVlanEditType(last,value):
	c = connectDB()
	cursor = c.cursor()
	#check if VLANID, last, is already in the 'vlans' table
	lookupQuery = "SELECT * FROM vlans WHERE VlanId = \'"+str(last)+"\';"
	try:
		cursor.execute(lookupQuery)
		foundRow = cursor.fetchall()
	except:
		print "Error in mysql.setDBvtpVlanEditType(),lookup"
	if not foundRow:
		#vlanID 'last' not exists, insert a new Row into table 'vlans'
		insertQuery = "INSERT into vlans (VlanId, VlanMTU, VlanEditType,counts, permanent) VALUES("+str(last)+","+str(1500)+","+str(value)+",0, 0);"
		try:
			cursor.execute(insertQuery)
		except:
			print "Error in mysql.setDBvtpVlanEditType,insertQuery"
	else:
		#vlanID already exists,update VlanName
		updateQuery = "UPDATE vlans SET VlanMTU = 1500, VlanEditType = "+str(value)+" WHERE VlanId = '"+str(last)+"';"
		try:
			cursor.execute(updateQuery)
		except:
			print "Error in mysql.setDBvtpVlanEditType,updateQuery"
	c.commit()
	c.close()

def getDBvtpVlanEditType(last):
	c = connectDB()
	cursor = c.cursor()
	query = "select VlanEditType from vlans where VlanId = '"+str(last)+"';"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		result = long(data[0])
		c.commit()
		c.close()
		return result
	except:
		print "Error in getVlanEditType"
		c.commit()
		c.close()
		return 0L


def setDBvtpVlanDot10Said(last,value):
	c = connectDB()
	cursor = c.cursor()
	#check if VLANID(last) is already in the 'vlans' table
	lookupQuery = "SELECT * FROM vlans WHERE VlanId = \'"+str(last)+"\';"
	try:
		cursor.execute(lookupQuery)
		foundRow = cursor.fetchall()
	except:
		print "Error in mysql.setDBvtpVlanDot10Said(),lookup"
	if not foundRow:
		#vlanID 'last' not exists, insert a new Row into table 'vlans'
		insertQuery = "INSERT into vlans (VlanId, VlanMTU, VlanDot10Said0,VlanDot10Said1,VlanDot10Said2,VlanDot10Said3,counts, permanent) VALUES("+str(last)+","+str(1500)+","+str(ord(value[0]))+","+str(ord(value[1]))+","+str(ord(value[2]))+","+str(ord(value[3]))+",0, 0);"
		try:
			cursor.execute(insertQuery)
		except:
			print "Error in mysql.setDBvtpVlanDot10Said,insertQuery"
	else:
		#vlanID already exists,update VlanName
		updateQuery = "UPDATE vlans SET VlanMTU = 1500, VlanDot10Said0 = "+str(ord(value[0]))+", VlanDot10Said1 = "+str(ord(value[1]))+", VlanDot10Said2 = "+str(ord(value[2]))+", VlanDot10Said3 = "+str(ord(value[3]))+" WHERE VlanId = '"+str(last)+"';"
		try:
			cursor.execute(updateQuery)
		except:
			print "Error in mysql.setDBvtpVlanDot10Said,updateQuery"
	c.commit()
	c.close()

def getDBvtpVlanDot10Said(last):
	c = connectDB()
	cursor = c.cursor()
	query = "select VlanDot10Said0, VlanDot10Said1, VlanDot10Said2, VlanDot10Said3 from vlans where VlanId = '"+str(last)+"';"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		Dot10Said = chr(data[0])+chr(data[1])+chr(data[2])+chr(data[3])
		c.commit()
		c.close()
		return Dot10Said
	except:
		print "Error in getVlanDot10Said"
		c.commit()
		c.close()
		return 0

def appendOIDTable(oid,value):
	c = connectDB()
	cursor = c.cursor()
	#check if oid exists
	query = "select * from OIDs where oid = '"+str(oid)+"';"
	cursor.execute(query)
	existOid = cursor.fetchall()
	if not existOid:
		lookupMaxIDQuery = "select max(id) from OIDs;"
		try:
			cursor.execute(lookupMaxIDQuery)
			maxIdCol = cursor.fetchall()
			maxID = maxIdCol[0][0]
			if isinstance(value,long):
				insertOIDQuery = "INSERT into OIDs (id,oid,value)VALUES("+str(maxID+1)+",'"+str(oid)+"',"+str(value)+");"
			elif isinstance(value,int):
				insertOIDQuery = "INSERT into OIDs (id,oid,value)VALUES("+str(maxID+1)+",'"+str(oid)+"',"+str(value)+");"
			elif isinstance(value,str):
				insertOIDQuery = "INSERT into OIDs (id,oid,value)VALUES("+str(maxID+1)+",'"+str(oid)+"','"+str(value)+"');"
			cursor.execute(insertOIDQuery)
		except:
			print "Error in appendOIDTable"
	else:
		if isinstance(value,str):
			updateQuery = "update OIDs set value = '"+value+"' where oid = '"+oid+"';"
		else:
			updateQuery = "update OIDs set value = "+str(value)+" where oid = '"+oid+"';"
		cursor.execute(updateQuery)
	c.close()

def getOIDTableValue(oid):
	c = connectDB()
	cursor = c.cursor()
	searchQuery = "select value from OIDs where oid = '"+str(oid)+"';"
	try:
		cursor.execute(searchQuery)
		data = cursor.fetchone()
		value = data[0]
		try:
			result = long(value)
		except:
			result = value
		c.commit()
		c.close()
		return result
	except:
		c.commit()
		c.close()
		pass

def getDBVmVlan(portIndex):
	c = connectDB()
	cursor = c.cursor()
	query = "select vlanID from ports where portIndex = "+str(portIndex)+";"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		value = data[0]
		result = long(value)
		c.commit()
		c.close()
		return result
	except:
		print "Error in getVmVlan"
		c.commit()
		c.close()
		return 0

def setDBVmVlan(portIndex,vlanId):
	c = connectDB()
	cursor = c.cursor()
	query = "update ports set vlanID = "+str(vlanId)+",modifiedTime = now() where portIndex = '"+str(portIndex)+"';"
	updateCountQuery = "update vlans set counts = counts + 1 where VlanId ='"+str(vlanId)+"';"
	try:
		cursor.execute(query)
		cursor.execute(updateCountQuery)
		c.commit()
		c.close()
	except:
		print "Error in setVmVlan"
		c.commit()
		c.close()

def resetDBVmVlan(portIndex,vlanId):
	c = connectDB()
	cursor = c.cursor()
#	check origin VlanID of the port
	findVlanIDquery = "select VlanId from ports where portIndex = "+str(portIndex)+";"
	try:
		cursor.execute(findVlanIDquery)
		data = cursor.fetchone()
		OldVlanID = data[0]
	except:
		print "Error in resetDBVmVlan"
	query = "update ports set VlanId = "+str(vlanId)+" where portIndex = '"+str(portIndex)+"';"
	updateCountQuery = "update vlans set counts = counts - 1 where VlanId ='"+str(OldVlanID)+"';"
	try:
		cursor.execute(query)
		cursor.execute(updateCountQuery)
	except:
		print "Error in resetVmVlan"
	c.commit()
	c.close()

def deleteUnusedVlan():
	c = connectDB()
	cursor = c.cursor()
	deleteQuery = "delete from vlans where counts = '0' and permanent = '0';"
	try:
		cursor.execute(deleteQuery)
	except:
		print "Error in deleteUnusedVlan"
	c.commit()
	c.close()


def getDBAdminStatus(portIndex):
	c = connectDB()
	cursor = c.cursor()
	query = "select AdminStatus from ports where portIndex = "+str(portIndex)+";"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		value = data[0]
		result = long(value)
		c.commit()
		c.close()
		return result
	except:
		print "Error in getAdminStatus"
		c.commit()
		c.close()
		return 0

def setDBAdminStatus(portIndex, value):
	c = connectDB()
	cursor = c.cursor()
	query = "UPDATE ports SET AdminStatus = "+str(value)+",modifiedTime = now() where portIndex = '"+str(portIndex)+"';"
	try:
		cursor.execute(query)
	except:
		print "Error in setDBAdminStatus"
	c.commit()
	c.close()

def setDBAdminSpeed(portIndex, value):
	c = connectDB()
	cursor = c.cursor()
	query = "UPDATE ports SET AdminSpeed = "+str(value)+",modifiedTime = now() where portIndex = '"+str(portIndex)+"';"
	try:
		cursor.execute(query)
	except:
		print "Error in setDBAdminSpeed"
	c.commit()
	c.close()

def setDBDuplex(portIndex, value):
	c = connectDB()
	cursor = c.cursor()
	query = "UPDATE ports SET Duplex = "+str(value)+",modifiedTime = now() where portIndex = '"+str(portIndex)+"';"
	try:
		cursor.execute(query)
	except:
		print "Error in setDuplex"
	c.commit()
	c.close()

def getPortTableStr(col,portIndex):
	c = connectDB()
	cursor = c.cursor()
	query = "select "+str(col)+" from ports where portIndex ='"+str(portIndex)+"' limit 1;"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		result = data[0]
		result = str(result)
		c.commit()
		c.close()
		return result
	except:
		c.commit()
		c.close()
		return ""

def getPortTableLong(col,portIndex):
	c = connectDB()
	cursor = c.cursor()
	query = "select "+str(col)+" from ports where portIndex ='"+str(portIndex)+"' limit 1;"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		result = data[0]
		result = long(result)
		c.commit()
		c.close()
		return result
	except:
		c.commit()
		c.close()
		return 0L

def getVlanTableLong(col,vlanId):
	c = connectDB()
	cursor = c.cursor()
	query = "select "+str(col)+" from vlans where VlanId ='"+str(vlanId)+"' limit 1;"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		result = data[0]
		result = long(result)
		c.commit()
		c.close()
		return result
	except:
		c.commit()
		c.close()
		return 0L

def getVlanTableStr(col,vlanId):
	c = connectDB()
	cursor = c.cursor()
	query = "select "+str(col)+" from vlans where VlanId ='"+str(vlanId)+"' limit 1;"
	try:
		cursor.execute(query)
		data = cursor.fetchone()
		result = data[0]
		result = str(result)
		c.commit()
		c.close()
		return result
	except:
		c.commit()
		c.close()
		return ""

def getVlanNameList():
	c = connectDB()
	cursor = c.cursor()
	query = "select VlanId from vlans;"
	try:
		l = []
		cursor.execute(query)
		data = cursor.fetchall()
		for i in data:
			l.append(i[0])
		c.commit()
		c.close()
		return l
	except:
		c.commit()
		c.close()
		return []

def getPortIndexList(head = 2,max = 32):
	c = connectDB()
	cursor = c.cursor()
	query = "select portIndex from ports where portIndex > "+str(head)+" Limit "+str(max)+";"
	try:
		result = []
		cursor.execute(query)
		data = cursor.fetchall()
		for item in data:
			result.append(item[0])
		return result
	except:
		print "Error in getPortIndexList"

def str2MACDec(mac):
	macList = mac.split(":")
	result = str()
	for i in range(len(macList)):
		macList[i]=str(int("0x"+macList[i],16))
	result = ".".join(macList)
	return result

def str2MACHexStr(mac):
	macList = mac.split(":")
	result = str()
	for i in range(len(macList)):
#		macList[i]="0x"+macList[i]
		result = result+chr(int("0x"+macList[i],16))
	return result

def bulkD1TPtable(vlan):
	m = []
	pI = []
	s = []
	c = connectDB()
	cursor = c.cursor()
	query = "select portIndex,MAC from ports where vlanID = '"+str(vlan)+"' and not portIndex= '2';"
	try:
		cursor.execute(query)
		fdata = cursor.fetchall()
		for i in fdata:
			decMac = str2MACDec(str(i[1]))
			m.append({"oid":"1.3.6.1.2.1.17.4.3.1.1."+decMac,
			"value":str2MACHexStr(i[1])})
			pI.append({"oid":"1.3.6.1.2.1.17.4.3.1.2."+decMac,
			"value":long(i[0])})
			s.append({"oid":"1.3.6.1.2.1.17.4.3.1.3."+decMac,"value":3L})
		result = []
		result.extend(m)
		result.extend(pI)
		result.extend(s)
		return result
	except:
		return []
		print "Error in D1TPtable"

def bulkBassNum(vlan):
	s = []
	c = connectDB()
	cursor = c.cursor()
	query = "select portIndex from ports where vlanID = '"+str(vlan)+"' and not portIndex= '2';"
	try:
		cursor.execute(query)
		fdata = cursor.fetchall()
		for i in fdata:
			s.append({"oid":"1.3.6.1.2.1.17.1.4.1.2."+str(i[0]),"value":long(i[0])})
		result = []
		result.extend(s)
		return result
	except:
		return []
		print "Error in D1TPtable"

def test():
	c = connectDB()
	cursor = c.cursor()
	query = "INSERT INTO vlans(VlanID, VlanName, VlanEditType, VlanMTU, VlanDot10Said0,VlanDot10Said1,VlanDot10Said2,VlanDot10Said3, VlanEditRowStatus,counts,permanent ) VALUES(1, 'default', 2, 1500, 0,1,134,150, 4, 0, 1);"
	cursor.execute(query)
	sQuery = "select * from vlans"
	cursor.execute(sQuery)
	data = cursor.fetchall()
	pprint(data)
	c.commit()
	c.close()

def resetAll():
	resetPortTable()
	resetVlanTable()
	initialPortTable()
	initialVlanTable()

if __name__ == '__main__':
	setDBVmVlan(6,101)
