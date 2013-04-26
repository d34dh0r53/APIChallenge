#!/usr/bin/env python

"""challenge2.py: Response to Challenge 2 of Rackspace API Challenge"""
"""redirect stderr to eliminate status messages"""

__author__ = "david.wilde@rackspace.com"

import pyrax
import sys
import json

pyrax.set_credential_file("/home/cdw/.rackspace_cloud_credentials")
cs = pyrax.cloudservers
sys.stderr.flush()
sys.stdout.flush()

# get the ID of our first server to clone
servers = cs.servers.list()
server_id = servers[0].id

# create the image to clone from
image_name = "dolly"
server = cs.servers.get(server_id)
server.create_image(image_name)

# get the image id for our new image
for image in cs.images.list():
    if image.name == image_name:
        clone_id = image.id
        
# monitor the status of the image build
sys.stderr.write("Cloning image...")
while True:
    if cs.images.get(clone_id).status == "ACTIVE":
        sys.stderr.write("done.\n")
        sys.stderr.flush()
        break

# get/set the flavor
flavors = cs.flavors.list()
flavor_512 = [flavor for flavor in flavors if flavor.ram == 512][0]

# create a new server from the image
new_server = cs.servers.create("web4", clone_id, flavor_512)

# monitor the status of the new clone
sys.stderr.write("Creating server from image...")
while True:
    if cs.servers.get(new_server.id).status == "ACTIVE":
        sys.stderr.write("done.\n")
        sys.stderr.flush()
        sys.stdout.write(json.dumps({"serverName": new_server.name, "adminPassword": new_server.adminPass, "serverNetworks": cs.servers.get(new_server.id).networks}, indent=4, separators=(',', ': ')))
        sys.stdout.write("\n")
        sys.stdout.flush()
        break