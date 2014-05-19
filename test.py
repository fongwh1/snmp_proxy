import sys
import handler
import sshXen
try:
	from pprint import pprint
except:
	sys.exit("install pprint")

#def test():
karg = {
'snmpdata':[{'oid':'1.3.6.1.4.1.9.9.46.1.4.2.1.11.1.113', 'value':4L},{'oid':'1.3.6.1.4.1.9.9.46.1.4.2.1.3.1.113', 'value':1L},{'oid':'1.3.6.1.4.1.9.9.46.1.4.2.1.4.1.113', 'value':'57'},{'oid':'1.3.6.1.4.1.9.9.46.1.4.2.1.6.1.113', 'value':'\x00\x01\x87\x11'}],'community': "private", 'function':"SNMPget", 'xid':1, 'version':1L, 'pdu' : {'error':0L, 'error_index': 0L}}
karg1 = {
'snmpdata':[{'oid':'1.3.6.1.2.1.1.1.0', 'value':0L}],'community': "testbed", 'function':"SNMPget", 'xid':1, 'version':1L, 'pdu' : {'error':0L, 'error_index': 0L}}
karg2 = {
'snmpdata':[{'oid':'1.3.6.1.2.1.2.2.1.2', 'value':0}],'community': "private@2", 'function':"SNMPbulk", 'xid':1, 'version':1L, 'pdu' : {'max_repetitions':0L, 'non_repeaters': 0L}}

karg3 = {
'snmpdata':[{'oid':'1.3.6.1.4.1.9.9.68.1.2.2.1.2.10102', 'value':2L}],'community': "private@2", 'function':"SNMPset", 'xid':1, 'version':1L, 'pdu' : {'error':0L, 'error_index': 0L}}

karg4 = {
'snmpdata':[{'oid':'1.3.6.1.2.1.17.4.3', 'value':0}],'community': "private@101", 'function':"SNMPbulk", 'xid':1, 'version':1L, 'pdu' : {'max_repetitions':0L, 'non_repeaters': 0L}}

karg5 = {
'snmpdata':[{'oid':'', 'value':0}],'community': "private@2", 'function':"SNMPget", 'xid':1, 'version':1L, 'pdu' : {'error':0L, 'error_index': 0L}}



if __name__ == "__main__":
	result = handler.reply(karg1)
	pprint(result)
