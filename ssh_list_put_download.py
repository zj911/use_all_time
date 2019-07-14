# 远程批量上传和下载，执行 ssh cmd
import os
import re
from scp import SCPClient
import csv
import paramiko
import getopt
import sys
import time
import math
import datetime

def run(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def upload(file_name, floder):
    client = get_connect()
    scp = SCPClient(client.get_transport())
    scp.put(file_name, floder)
    client.close()

def download(file_name, floder):
    client = get_connect()
    scp = SCPClient(client.get_transport())
    scp.get(file_name, floder)
    client.close()

def get_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ssh_server, port=ssh_port, username=ssh_name, password=ssh_password)
    return client

def make_dir(folder):
    client = get_connect()
    stdin, stdout, stderr = client.exec_command(str('mkdir {}'.format(folder)))
    print(str('mkdir {}'.format(folder)))
    print('\n******* make remote_folder...\n')
    for line in stdout:
        print(line.strip('\n'))
    client.close()

def exec_cmdline(cmdline):
    client = get_connect()    
    print('\nThe command to be executed is: \n' + cmdline)
    stdin, stdout, stderr = client.exec_command(str('{}'.format(cmdline)))
    print('\n******* exec cmdline...\n')
    info_list = [line.strip('\n') for line in stdout]
    for line in stdout:
        print(line.strip('\n'))    
    client.close()
    return info_list

ssh_server = '172.16.231.17'
ssh_port = '22'
ssh_name = 'root'
ssh_password = 'admin123'

cmdline = sys.argv[1]
# local_folder = sys.argv[2]
# scp_folder = sys.argv[3]


#批量上传或者单独上传
if cmdline == 'put':
    local_folder = '/home/zhaojie/tf/'
    remote_folder = '/D0/zhaojie/'
    if os.path.isdir(local_folder):
        for root,dirs,files in os.walk(local_folder):
            for filespath in files:
                local_file = os.path.join(root, filespath)
                a = local_file.replace(local_folder, "")
                remote_file = os.path.join(remote_folder, a)
                try:
                    upload(local_file, remote_file)
                except Exception as err:
                    make_dir(os.path.split(remote_file)[0])
                    upload(local_file, remote_file)
                print ("upload {} to remote {} ".format(local_file,remote_file) + str(datetime.datetime.now()))
    else:
        upload(local_folder, remote_folder)
        print ("upload {} to remote {} ".format(local_folder,remote_folder) + str(datetime.datetime.now()))


#批量下载或者单独下载
if cmdline == 'get':
    local_folder = '/home/zhaojie/tf'
    remote_folder = '/D0/zhaojie'
    if remote_folder.startswith('/'):
        first_ls = exec_cmdline('ls -R {}'.format(remote_folder))
        path = ''
        for file_list in first_ls:
            print(file_list)
            if file_list.startswith('/') or file_list == '':
                path = file_list + '/'
                continue
            # print('debug')
            file_path = path.replace(':', '') + file_list
            print(file_path)
    else:
        pass

#批量执行
if cmdline == 'exec':
    cmd = 'date'
    cc = exec_cmdline('date')