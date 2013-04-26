#!/usr/bin/env python

"""challenge3.py: Response to Challenge 3 of Rackspace API Challenge"""
"""redirect stderr to eliminate status messages"""

__author__ = "david.wilde@rackspace.com"

import pyrax
import sys
import json
import argparse
import os

pyrax.set_credential_file("/home/cdw/.rackspace_cloud_credentials")
cf = pyrax.cloudfiles
sys.stdout.flush()
sys.stderr.flush()

parser = argparse.ArgumentParser(description='Challenge 3: Upload a directory to a container')
parser.add_argument('directory', help='the directory to upload')
parser.add_argument('container', help='the container to upload the directory to (it will be created if it does not exist)')
args = parser.parse_args()

# lets see if the directory exists on the local system
try:
    if not os.path.exists(args.directory):
        raise IOError
except IOError:
    sys.stderr.write("IOError: Directory %s does not exist\n" %args.directory)

# get the container specified (create_container will create if it doesn't exist and return if it does)
cont = cf.create_container(args.container)

# upload the files to the container
for (path,dirs,files) in os.walk(args.directory):
    for file in files:
        pth = path + file
        chksum = pyrax.utils.get_checksum(pth)
        sys.stderr.write("Uploading %s..." %pth)
        obj = cf.upload_file(cont, pth, etag=chksum)
        sys.stderr.write("done\n")
        sys.stderr.flush()
        sys.stdout.write("Checksum: %s etag: %s\n" %(chksum, obj.etag))
        sys.stdout.flush()