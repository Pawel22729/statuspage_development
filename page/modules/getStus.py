#!/usr/bin/env python

import paramiko

usr = 'plasak'
pas = open('/home/plasak/.pass').strip()

def connect(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=pas)
    except Exception as e:
        print(e)
    
    return ssh     
    
def exec(cmd, host):
    conn = connect(host)
    try:
        stdin, stdout, stderr = conn.exec_command(cmd)
    except Exception as e:
        print(r)

    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            
