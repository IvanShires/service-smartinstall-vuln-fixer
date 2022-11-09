from netmiko import ConnectHandler
import os
from datetime import datetime

## Switch Credentials
switch_user = os.environ['network_switch_usr']
switch_password = os.environ['network_switch_pwd']

## Logging Directory
logging_directory = "/opt/service-SmartInstall-vuln-fixer/"

def get_time():
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y %H-%M")
    return dt_string

class switch_connect:
    def __init__(self,switch_ipaddr):
        self.switch_ipaddr = switch_ipaddr
        self.info = self.get_information()

    def get_information(self):
        command = "show version"
        device = {
            "device_type": "cisco_ios",
            "host": str(self.switch_ipaddr),
            "username": str(switch_user),
            "password": str(switch_password),
            "timeout": 30,
        }
        with ConnectHandler(**device) as net_connect:
            self.output = net_connect.send_command(command,use_textfsm=True)
        return self.output

    def smartinstall_vstack(self):
        commands = [
            'no vstack',
            ]

        device = {
            "device_type": "cisco_ios",
            "host": str(self.switch_ipaddr),
            "username": str(switch_user),
            "password": str(switch_password),
            "session_log": logging_directory + str(self.switch_ipaddr) + "-" + str(get_time()) + ".txt",
            "timeout": 30,
        }
        with ConnectHandler(**device) as net_connect:
            self.output = net_connect.send_config_set(commands)
            self.output += net_connect.save_config()

    def create_smartinstall_acl(self):
        commands = [
            'access-list 100 deny tcp any any eq 4786',
            'access-list 100 deny udp any any eq 4786',
            'access-list 100 permit ip any any',
            'interface GigabitEthernet1',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet2',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 1/1/1', ## 3750x/3650/3850 with uplink module.. maybe 3750E with SFP usage
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 1/1/2', ## 3750x/3650/3850 with uplink module.. maybe 3750E with SFP usage
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 1/1', ## 3560x with uplink module 
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 1/2', ## 3560x with uplink module
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 0/47',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 0/48',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 1/0/47', ## 3750x/3750e
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface GigabitEthernet 1/0/48',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface FastEthernet 1/1', ## 3560 using SFP ports
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface FastEthernet 1/2', ## 3560 using SFP ports
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface FastEthernet 0/47', ## 3560
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface FastEthernet 0/48', ## 3560
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface FastEthernet 1/0/47',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface FastEthernet 1/0/48',
            'ip access-group 100 in',
            'ip access-group 100 out',
            'interface vlan 1',
            'ip access-group 100 in',
            'ip access-group 100 out',
            ]
        device = {
            "device_type": "cisco_ios",
            "host": str(self.switch_ipaddr),
            "username": str(switch_user),
            "password": str(switch_password),
            "session_log": logging_directory + str(self.switch_ipaddr) + "-" + str(get_time()) + ".txt",
            "timeout": 30,
        }
        with ConnectHandler(**device) as net_connect:
            self.output = net_connect.send_config_set(commands)
            self.output += net_connect.save_config()

    def get_version(self):
        return self.output[0]['version']