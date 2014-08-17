#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname
from os.path import realpath
from os.path import exists
from os import mkdir
import sys
import socket
import re

docker_image_name = 'isso:latest'
docker_image_port = '8080'
docker_name_prefix = 'rave_'
current_dir = dirname(realpath(__file__))
conf_default = current_dir + '/../conf/isso.conf'
conf_default_name = 'isso.conf'
conf_webserver = current_dir + '../conf/nginx.conf'
webserver_path = '/etc/nginx/rave'

def check_pseudo(name):
    """
    Check that pseudo is a string.
    Also check that pseudo is not a reserved pseudo.
    """
    if not isinstance(name, str):
        return False
    if name in ['proxy_add_x_forwarded_for', 'host', 'scheme']:
        print("Pseudo not allowed!")
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
    # Prepare user configuration file
    config = home + '/' + conf_default_name
    # Do some changes on it by writing new file
    destination = open(config, 'w')
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
    return home, config

def create_docker(port, volume_path, pseudo):
    """
    Create a docker container and mount volume_path as main path for Isso default directory
    """
    from subprocess import Popen, PIPE
    name = docker_name_prefix + pseudo
    ports = '%s:%s' % (port, docker_image_port)
    volumes = '%s:%s' % (volume_path, '/opt/isso')
    generation = Popen(['docker', 'run', '-d', '-p', ports, '--name', name, '-v', volumes, docker_image_name], stdout=PIPE, stderr=PIPE)
    # Launch clean up then generation
    stdout = ()
    try:
        stdout = generation.communicate()
    except Exception as e:
        return False, e
    if stdout and len(stdout) > 1 and stdout[1]:
        return False, stdout[1]
    return True, ''

def create_webserver_conf(pseudo, port):
    """
    Create a new Web Server configuration file for the new user.
    First read the default web server file.
    Then replace values.
    Finally 
    """
    res = False
    with open(conf_webserver, 'r') as conf:
        t = string.Template(conf.read())
        res = t.safe_substitute({
            'pseudo': pseudo,
            'port': port,
        })
    conf.close()
    if not res:
        raise Exception('Error during webserver file conversion')
        return False
    newfile_path = webserver_path + '/' + pseudo + '.conf'
    newfile = open(newfile_path, 'w')
    newfile.write(res)
    newfile.close()
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

    # Create the user home directory in which comments and configuration will be.
    home, config = create_home(pseudo, email, website)

    # Create the docker container with right parameters
    docker, msg = create_docker(port, home, pseudo)
    if not docker:
        raise Exception("Docker problem: %s" % msg)

    # Create the nginx configuration
    webserver_conf_creation = create_webserver_conf(pseudo, port)
    if not webserver_conf_creation:
        raise Exception('Web server configuration failed!')

    # TODO: Reload nginx
    # TODO: Check with wget or Mechanize that the result is OK

    # Display result
    print("INFO:%s;%s" % (pseudo, port))

    return 0

if __name__ == '__main__':
    sys.exit(main())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
