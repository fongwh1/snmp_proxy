#!/usr/bin/python
import sys
import paramiko
import pw
import time

un = pw.xen_user
ps = pw.xen_ps
path = '/usr/local/xnode/'
server_ip = pw.xen_host

maxConnectionTimes = 25

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
	timesCount = 0
	while(not execSuccess):
		try:
			stdin, stdout, stderr = ssh.exec_command(create_cmd(mac,vlanName,vlanID,reset))
			execSuccess = True
		except:
			pass
		time.sleep(1.5)
		timesCount+=1
		if timesCount == maxConnectionTimes:
			break

	feedback = stdout.read()
	print feedback
	eFeedback = feedback.split("vif")
	while(str(eFeedback[1][0:1]) == "()"):
		print "Try Again:"
		stdin, stdout, stderr = ssh.exec_command(create_cmd(mac,vlanName,vlanID,reset))
		feedback = stdout.read()
		print feedback
		eFeedback = feedback.split("vif")
	ssh.close()

if __name__=="__main__":
	pass
