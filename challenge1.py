#!/usr/bin/env python

import pyrax
import sys
import json
import os
import sys
import argparse
from math import floor
from time import sleep

class RaxServer(object):
    
    def __init__(self, cs, server_name, image, flavor):
        self.cs = cs
        self.server_name = server_name
        self.image = image
        self.flavor = flavor
        
        self.instance = self.cs.servers.create(
                            self.server_name, 
                            self.image.id, 
                            self.flavor.id)
        self.server_id = self.instance.id
        self.adminPass = self.instance.adminPass
    
    def status(self):
        return self.cs.servers.get(self.server_id).status
        
    def progress(self):
        return self.cs.servers.get(self.server_id).progress
        
    def networks(self):
        return self.cs.servers.get(self.server_id).networks
        
def auth():
    sys.stderr.write("Authenticating....")
    pyrax.set_credential_file(
                os.path.expanduser("~/.rackspace_cloud_credentials"))
    cs = pyrax.cloudservers
    sys.stderr.write("success!\n")
    sys.stderr.flush()
    return cs
    
def getFlavor(cs):
    sys.stderr.write("Enumerating flavors...")
    # load the images and flavors
    images = cs.images.list()
    flavors = cs.flavors.list()
    
    # we're building 512MiB Ubuntu 12.10 instances by default
    image = [image for image in images if "Ubuntu 12.10" in image.name][0]
    flavor = [flavor for flavor in flavors if flavor.ram == 512][0]
    sys.stderr.write("success!\n")
    sys.stderr.flush()
    return image,flavor
        
def ProgressBar(servers, bar_length=50):
    total_counter = (len(servers)*100)
    progress_counter = 0
    status_string = ""
    for server in servers:
        progress_counter += server.progress()
        status_string += "%s: %s (%d%%) " %(
                server.server_name, 
                server.status(), 
                server.progress())
    bar_pct = float(progress_counter) / total_counter
    chunks = int(floor(bar_length * bar_pct))
    return "\r[{0}>{1}] {2:.2}% {3}".format(
            "="*chunks, 
            " " * (bar_length - chunks), 
            bar_pct * 100, 
            status_string)
    
def BuildComplete(servers):
    flags = 0
    for server in servers:
        if server.status() == 'ACTIVE':
            flags += 1
    if flags == len(servers):
        return True
    else:
        return False

def main():
    ooServers = []
    serverNames = ['oo-web1', 'oo-web2', 'oo-web3']
    
    cs = auth()
    flavor, image = getFlavor(cs)
    
    # create the servers
    sys.stderr.write("Creating instances\n")
    sys.stderr.flush()
    for ooName in serverNames:
        s = RaxServer(cs, ooName, flavor, image)
        ooServers.append(s)
                
    while True:
        if BuildComplete(ooServers):
            for ooServer in ooServers:
                sys.stderr.write("\n")
                sys.stdout.write(json.dumps({
                    'serverName': ooServer.server_name,
                    'adminPass': ooServer.adminPass,
                    'networks': ooServer.networks()
                }, indent=4, separators=(',', ': ')))
                sys.stdout.write("\n")
                sys.stdout.flush()
            break
        else:
            sys.stderr.write(ProgressBar(ooServers))
            sys.stderr.flush()
            sleep(5)
    
if __name__ == '__main__':
    main()