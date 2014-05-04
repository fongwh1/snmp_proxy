import MySQLdb
import time
from pprint import pprint
from MySQLdb.cursors import SSCursor
import collections
import pw

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
			VlanMTU INT,
			VlanDot10Said0 INT,
			VlanDot10Said1 INT,
			VlanDot10Said2 INT,
			VlanDot10Said3 INT,
			VlanEditRowStatus INT
		)

		"""
	cursor.execute(query)
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
	print vtpVlanNameTable
	for k in vtpVlanNameTable:
		query = "INSERT INTO vlans(VlanID, VlanName, VlanMTU, VlanDot10Said0,VlanDot10Said1,VlanDot10Said2,VlanDot10Said3, VlanEditRowStatus ) VALUES(%s, '%s', %s, %s,%s,%s,%s, %s)" % (k['VlanID'],k['VlanName'],k['VlanMTU'],str(ord(k['VlanDot10Said'][0])),str(ord(k['VlanDot10Said'][1])),str(ord(k['VlanDot10Said'][2])),str(ord(k['VlanDot10Said'][3])),k['VlanEditRowStatus'])
		cursor.execute(query)
		print ord(k['VlanDot10Said'][0]),ord(k['VlanDot10Said'][1]),ord(k['VlanDot10Said'][2]),ord(k['VlanDot10Said'][3])
		print chr(ord(k['VlanDot10Said'][0])),chr(ord(k['VlanDot10Said'][1])),chr(ord(k['VlanDot10Said'][2])),chr(ord(k['VlanDot10Said'][3]))
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
#	print qAddPort
	c.close()

def newPortQuery(	id, 
			portIndex,
			portNum, 
			portName, 
			MAC, 
			vlanID = 1, 
			AdminStatus = 0, 
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
	MAX_PORT_NUMBER = 50
	for i in range(1,MAX_PORT_NUMBER+1):
		p_id = i
		p_index = 10100 + i
		p_num = i
		p_name = "GigabitEthernet1/0/" + str(i)
		p_MAC = "00:16:3e:01:01:" + format(i,'02x')
		cursor.execute(newPortQuery(p_id,p_index,p_num,p_name,p_MAC))
	c.close()

def editPTKeyValue(portIndex, key, value):
	c = connectDB()
	cursor = c.cursor()
	qUpdate = "UPDATE ports SET "+str(key)+" = '"+str(value)+"' WHERE portIndex = '"+str(portIndex)+"'"
	cursor.execute(qUpdate)
	qUpdate = "UPDATE ports SET modifiedTime = NOW() WHERE portIndex = '"+str(portIndex)+"'"
	cursor.execute(qUpdate)
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
	pprint(VNT)
	c.close()


def initOIDTable():
	c = connectDB()
	cursor = c.cursor()
	cursor.execute("DROP TABLE IF EXISTS OIDs")
	id = 0
	initOIDTable = [{'oid': '1.3.6.1.2.1.2.2.1.2.1', 'value': 'Vlan1'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.2', 'value': 'Vlan2'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.5137', 'value': 'StackPort1'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.5138', 'value': 'StackSub-St1-1'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.5139', 'value': 'StackSub-St1-2'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10101','value': 'GigabitEthernet1/0/1'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10102','value': 'GigabitEthernet1/0/2'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10103','value': 'GigabitEthernet1/0/3'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10104','value': 'GigabitEthernet1/0/4'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10105','value': 'GigabitEthernet1/0/5'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10106','value': 'GigabitEthernet1/0/6'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10107','value': 'GigabitEthernet1/0/7'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10108','value': 'GigabitEthernet1/0/8'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10109','value': 'GigabitEthernet1/0/9'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10110','value': 'GigabitEthernet1/0/10'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10111','value': 'GigabitEthernet1/0/11'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10112','value': 'GigabitEthernet1/0/12'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10113','value': 'GigabitEthernet1/0/13'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10114','value': 'GigabitEthernet1/0/14'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10115','value': 'GigabitEthernet1/0/15'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10116','value': 'GigabitEthernet1/0/16'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10117','value': 'GigabitEthernet1/0/17'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10118','value': 'GigabitEthernet1/0/18'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10119','value': 'GigabitEthernet1/0/19'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10120','value': 'GigabitEthernet1/0/20'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10121','value': 'GigabitEthernet1/0/21'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10122','value': 'GigabitEthernet1/0/22'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10123','value': 'GigabitEthernet1/0/23'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10124','value': 'GigabitEthernet1/0/24'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10125','value': 'GigabitEthernet1/0/25'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10126','value': 'GigabitEthernet1/0/26'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10127','value': 'GigabitEthernet1/0/27'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10128','value': 'GigabitEthernet1/0/28'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10129','value': 'GigabitEthernet1/0/29'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10130','value': 'GigabitEthernet1/0/30'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10131','value': 'GigabitEthernet1/0/31'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10132','value': 'GigabitEthernet1/0/32'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10133','value': 'GigabitEthernet1/0/33'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10134','value': 'GigabitEthernet1/0/34'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10135','value': 'GigabitEthernet1/0/35'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10136','value': 'GigabitEthernet1/0/36'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10137','value': 'GigabitEthernet1/0/37'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10138','value': 'GigabitEthernet1/0/38'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10139','value': 'GigabitEthernet1/0/39'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10140','value': 'GigabitEthernet1/0/40'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10141','value': 'GigabitEthernet1/0/41'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10142','value': 'GigabitEthernet1/0/42'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10143','value': 'GigabitEthernet1/0/43'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10144','value': 'GigabitEthernet1/0/44'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10145','value': 'GigabitEthernet1/0/45'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10146','value': 'GigabitEthernet1/0/46'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10147','value': 'GigabitEthernet1/0/47'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10148','value': 'GigabitEthernet1/0/48'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10149','value': 'GigabitEthernet1/0/49'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10150','value': 'GigabitEthernet1/0/50'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10201','value': 'TenGigabitEthernet1/0/1'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.10202','value': 'TenGigabitEthernet1/0/2'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.12001', 'value': 'Null0'},
		{'oid': '1.3.6.1.2.1.2.2.1.2.12002', 'value': 'FastEthernet0'},
		{'oid': '1.3.6.1.2.1.2.2.1.3.1', 'value': 53L},
		{'oid': '1.3.6.1.2.1.2.2.1.3.2', 'value': 53L},
		{'oid': '1.3.6.1.2.1.2.2.1.3.5137', 'value': 53L},
		{'oid': '1.3.6.1.2.1.2.2.1.3.5138', 'value': 53L},
		{'oid': '1.3.6.1.2.1.2.2.1.3.5139', 'value': 53L}]

	query = "CREATE TABLE OIDs (id INT, oid VARCHAR(50),value VARCHAR(30))"
	cursor.execute(query)
	queryInsert = "insert into OIDs (id,oid,value)VALUES"
	
	for item in initOIDTable:
		oid_value = "("+str(id)+",\""+str(item['oid'])+"\",\""+str(item['value'])+"\"),"
		queryInsert = queryInsert+oid_value
		id+=1
	queryInsert = queryInsert[0:-1]
	#print (queryInsert)
	cursor.execute(queryInsert)
	c.close()

def bulkOID(oid):
	c = connectDB()
	cursor = c.cursor()
	lookupQuery = "select * from OIDs WHERE oid LIKE \'"+str(oid)+"\' LIMIT 1;"
	try:
		cursor.execute(lookupQuery)
		foundRow = cursor.fetchall()
		if not foundRow:
			print "NULL"
			newOID = oid + ".1"
			lookupQuery2 = "select * from OIDs WHERE oid LIKE \'"+str(newOID)+"\' LIMIT 1;"
			cursor.execute(lookupQuery2)
			foundRow = cursor.fetchall()
	except:
		print "Error occured in bulkOID()"
	pprint(foundRow)
	if foundRow:
		foundID = foundRow[0][0]
		fQuery = "select * from OIDs where id >= "+str(foundID)+" LIMIT 32;"
		cursor.execute(fQuery)
		result = cursor.fetchall()
	print "mysql.bulkOID"
	c.close()
	return result

if __name__ == '__main__':
	initOIDTable()
	bulkOID("1.3.6.1.2.1.2.2.1.2.10127")
