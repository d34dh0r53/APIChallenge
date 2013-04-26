#!/usr/bin/env python

"""challenge5.py: Response to Challenge 5 of Rackspace API Challenge"""
"""redirect stderr to eliminate status messages"""

__author__ = "david.wilde@rackspace.com"

import pyrax
import sys
import json
import argparse
import os

pyrax.set_credential_file("/home/cdw/.rackspace_cloud_credentials")
cdb = pyrax.cloud_databases
sys.stdout.flush()
sys.stderr.flush()

parser = argparse.ArgumentParser(description='Challenge 5: Create a new database')
args = parser.parse_args()

# create the instance
sys.stderr.write("Creating the new database instance...")
inst = cdb.create("ch5_instance", flavor="1GB Instance", volume=2)

# monitor the status of the new instance
while True:
    if cdb.get(inst.id).status == "ACTIVE":
        sys.stderr.write("done.\n")
        sys.stderr.flush()
        sys.stdout.write(json.dumps({"hostname": inst.hostname, "id": inst.id, "links": inst.links, "name": inst.name, "status": cdb.get(inst.id).status}, indent=4, separators=(',', ': ')))
        sys.stdout.write("\n")
        sys.stdout.flush()
        break
        
# create the database
sys.stderr.write("Create the new database...")
db = inst.create_database("ch5_db")
sys.stderr.write("done.\n")

# create the user
sys.stderr.write("Create the user...")
user = inst.create_user(name="ch5_user", password="password", database_names=[db])
sys.stderr.write("done.\n")