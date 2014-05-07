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
	ssh.connect(server_ip,username = un,password = ps)
	stdin, stdout, stderr = ssh.exec_command(create_cmd(mac,vlanName,vlanID,reset))
	print stdout.read()
	ssh.close()


