## Cisco SmartInstall Vunerability Fixer

## Author: Ivan Shires

import netmiko
import os
import sys
import socket
from helpers.switch_class import *

## SmartInstall Port
network_port = 4786

## Logging Directory
logging_directory = "/opt/service-SmartInstall-vuln-fixer"

## Switch Credentials
#switch_user = os.environ['network_switch_usr']
#switch_password = os.environ['network_switch_pwd']


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
    print(host,"is vulnerable!")

else:
    print(host,"is OK")