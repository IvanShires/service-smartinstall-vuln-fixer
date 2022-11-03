from netmiko import ConnectHandler
import os

## Switch Credentials
switch_user = os.environ['network_switch_usr']
switch_password = os.environ['network_switch_pwd']

class switch_connect:
    def __init__(self,switch_ipaddr):
        self.switch_ipaddr = switch_ipaddr
        self.info = self.get_information()

    def get_information(self):
        command = "show version"
        device = {
            "device_type": "cisco_ios_telnet",
            "host": str(self.switch_ipaddr),
            "username": str(switch_user),
            "password": str(switch_password),
            "timeout": 30,
        }
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(command,use_textfsm=True)