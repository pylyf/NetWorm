import socket
from urllib.request import urlopen
import urllib

def get_private_ip():
    """
    Gets private IP address of this machine.
    This will be used for scanning other computers on LAN.

    Returns:
        private IP address
    """
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def get_public_ip():
    """
    Gets public IP address of this network.
    You can access the router with this ip too.

    Returns:
        public IP address
    """
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)