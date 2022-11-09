## Cisco SmartInstall Vunerability Fixer

## Author: Ivan Shires

import netmiko
import os
import sys
import socket
from helpers.switch_class import *

## SmartInstall Port
network_port = 4786

## Switch Credentials
switch_user = os.environ['network_switch_usr']
switch_password = os.environ['network_switch_pwd']

## Versions that do NOT support "no vstack"
bad_versions_file = open("smartinstall_bad_versions.txt","r")
bad_versions = bad_versions_file.readlines()
bad_versions = [item.rstrip() for item in bad_versions]

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y %H-%M")
    return dt_string

def check_network_port(target,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,port))
        if (result == 0):
            return True
        else:
            return False

host = sys.argv[1]

vulnerability_status = check_network_port(host,network_port)

if (vulnerability_status):
    switch = switch_connect(host)
    print(str(get_time()) + " - " + str(host),"is vulnerable!")
    users_connected = switch.get_users_connected()
    if (users_connected > 1):
        print(str(users_connected),"users connected to the switch!")
    else:
        switch_version = switch.get_version()
        if (any(bad_version in switch_version for bad_version in bad_versions)):
            print(str(get_time()) + " - " + str(host),"Requires ACL")
            switch.create_smartinstall_acl()
        else:
            print(str(get_time()) + " - " + str(host),"Running 'no vstack'")
            switch.smartinstall_vstack()    
else:
    print(host,"is OK")