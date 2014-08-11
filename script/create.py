#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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

def search_port():
    """
    Give a free port on the system.
    TIP: Ask system to use the port 0 give a free random port.
    """
    res = False
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    res = s.getsockname()[1]
#    s.close() # Close socket to prevent problem linked to its use
    return res

def main():
    args = sys.argv
    if len(args) != 2:
        raise Exception("Need only 1 argument: pseudo")
        return 1
    pseudo = args[1]
    if not check_pseudo(pseudo):
        raise Exception("Pseudo not valid")
        return 1
    port = search_port()
    if not port:
        raise Exception("No port found")
        return 1
    if not check_port(port):
        raise Exception("Port not valid")
        return 1
    port = int(port)
    
    print("###########################")
    print("Port: %s" % port)
    print("###########################")

    return 0

if __name__ == '__main__':
    sys.exit(main())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
