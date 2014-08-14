#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname
from os.path import realpath
from os.path import exists
from os import mkdir
import sys
import socket
import re

current_dir = dirname(realpath(__file__))
conf_default = current_dir + '/../conf/isso.conf'
conf_default_name = 'isso.conf'

def check_pseudo(name):
    """
    Check that pseudo is a string.
    """
    if not isinstance(name, str):
        return False
    return True

def check_port(name):
    """
    Check that port is an integer or can be converted into an integer.
    Check also port is superior to 1023 (well-known ports)
    """
    try:
        name = int(name)
    except ValueError as e:
        print(e)
        return False
    if name <= 1023:
        print("This port cannot be used: %s" % name)
        return False
    return True

def check_url(url):
    """
    Check that URL is well formed.
    Regex found in Django regex url validator.
    """
    # Check that URL is well formed
    regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not regex.match(url):
        print("URL malformed")
        return False
    return True

def search_port():
    """
    Give a free port on the system.
    TIP: Ask system to use the port 0 give a free random port.
    """
    res = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    res = s.getsockname()[1]
#    s.close() # Close socket to prevent problem linked to its use
    return res

def create_home(name, email, url):
    """
    Create the home directory with given name.
    Copy default configuration into by changing some elements.
    """
    home = current_dir + '/../users/' + name
    # Check that no other home directory have the same name
    if exists(home):
        raise Exception("Directory already exists: %s" % name)
        return 1
    # Create the directory
    mkdir(home)
    # Open the configuration file, read it and close it
    with open(conf_default, 'r') as f:
        origin = f.readlines()
        f.close()
    # Do some changes on it by writing new file
    destination = open(home + '/' + conf_default_name, 'w')
    host_found = 0
    for line in origin:
        if line.startswith('host ='):
            if not host_found or host_found < 1:
                line = 'host = ' + url + '\n'
                host_found += 1
            # TODO: Read a specific rave configuration file to find change to do into the isso cfg file
            elif host_found == 1:
                pass # Change host by those from the Rave server
        elif line.startswith('to ='):
            line = 'to = ' + email + '\n'
        destination.write(line)
    destination.close()
    return True

def main():
    """
    """
    # Check command line
    args = sys.argv
    if len(args) != 4:
        raise Exception("Need only 3 arguments: pseudo email website")
        return 1
    # Check pseudo
    pseudo = args[1]
    if not check_pseudo(pseudo):
        raise Exception("Pseudo not valid")
        return 1
    # Fetch remaining args
    email = args[2]
    website = args[3]
    # Check website URL
    if not check_url(website):
        raise Exception("Website URL not valid")
        return 1
    # Search an available port
    port = search_port()
    if not port:
        raise Exception("No port found")
        return 1
    if not check_port(port):
        raise Exception("Port not valid")
        return 1
    port = int(port)
    # TODO: Check WEBSITE URL
    print("###########################")
    print("Port: %s" % port)
    print("###########################")

    # Create the user home directory in which comments and configuration will be.
    create_home(pseudo, email, website)

    # TODO: Create the docker container with right parameters
    # TODO: Create the nginx configuration
    # TODO: Reload nginx
    # TODO: Check with wget or Mechanize that the result is OK

    return 0

if __name__ == '__main__':
    sys.exit(main())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
