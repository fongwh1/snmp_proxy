#!/usr/bin/python
import sys
import paramiko
import pw

un = pw.xen_user
ps = pw.xen_ps
path = '/usr/local/xnode/'
server_ip = pw.xen_host

def create_cmd(mac,vlanName,vlanID,reset = False):
	if reset:
		action = "reset"
	else:
		action = "set"
	cmd = path+"nc-vif-vlan-config"+" "+str(action)+" "+str(mac)+" "+str(vlanName)+" "+str(vlanID)
	return cmd

def ssh_connect(mac,vlanID,vlanName,reset = False):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	connectSuccess = False
	while(not connectSuccess):
		try:
			ssh.connect(server_ip,username = un,password = ps)
			connectSuccess = True
		except:
			print "connection to dom0 fail, try again:"
			print "MAC:"+str(mac)
	execSuccess = False
	while(not execSuccess):
		try:
			stdin, stdout, stderr = ssh.exec_command(create_cmd(mac,vlanName,vlanID,reset))
			execSuccess = True
		except:
			pass
	feedback = stdout.read()
	print feedback
	eFeedback = feedback.split("vif")
	print str(eFeedback[1])
	while(str(eFeedback[1][0:1]) == "()"):
		print "Try Again:"
		stdin, stdout, stderr = ssh.exec_command(create_cmd(mac,vlanName,vlanID,reset))
		feedback = stdout.read()
		eFeedback = feedback.split("vif")
		try:
			print eFeedback[1]
		except:
#			can't find 'vif' in spliting feedback
			pass
#	while(feedback[0:17] == "Success::set vif()"):
#		print "Try Again:"
#		stdin, stdout, stderr = ssh.exec_command(create_cmd(mac,vlanName,vlanID,reset))
#		feedback = stdout.read()
#		print feedback
	ssh.close()

if __name__=="__main__":
	ssh_connect("00:16:3e:01:02:28",1,"default",True)
	ssh_connect("00:16:3e:01:02:1b",1,"default",True)
	ssh_connect("00:16:3e:01:02:1e",1,"default",True)
	ssh_connect("00:16:3e:01:01:28",1,"default",True)
	ssh_connect("00:16:3e:01:01:0b",1,"default",True)
	ssh_connect("00:16:3e:01:01:0c",1,"default",True)

