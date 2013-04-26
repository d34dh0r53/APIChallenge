#!/usr/bin/env python

"""challenge4.py: Response to Challenge 4 of Rackspace API Challenge"""
"""redirect stderr to eliminate status messages"""

__author__ = "david.wilde@rackspace.com"

import pyrax
import sys
import json
import argparse
import os

pyrax.set_credential_file("/home/cdw/.rackspace_cloud_credentials")
dns = pyrax.cloud_dns
sys.stdout.flush()
sys.stderr.flush()

parser = argparse.ArgumentParser(description='Challenge 4: Create a DNS A record')
parser.add_argument('fqdn', help='Fully qualified domain name of A record to create')
parser.add_argument('ip', help='IP address to point the A record at')
args = parser.parse_args()

# we need to figure out where our fqdn goes
fqdn_list = args.fqdn.split('.')
fqdn_tld = []
domain_id = []

# we loop through the domains and split them into reverse order lists
# then we compare the current tld to the one specified in the arguments
# and determine the existing domain (if any) to add the fqdn to
for domain in dns.list():
    domain_name = domain.name.split('.')
    for i in range(len(fqdn_list) - 1):
        try:
            if domain_name[::-1][i] == fqdn_list[::-1][i]:
                if len(fqdn_tld) <= i:
                    fqdn_tld.append(domain_name[::-1][i])
                    domain_id = domain.id
        except IndexError:
            sys.stderr.write("Index out of range, you probably want to create a sub-domain first.\n")
            quit()

#print "TLD Length: %d FQDN Length: %d Diff: %d" %(len(fqdn_tld), len(fqdn_list), (len(fqdn_list) - len(fqdn_tld)))
if len(fqdn_tld) <= 1:
    try:
        raise IndexError
    except:
        sys.stderr.write("Index out of range, it doesn't look like you have registered that domain.\n")
        quit()

dom = dns.get(domain_id)
      
# build our A record
record = [{
    "type": "A",
    "name": args.fqdn,
    "data": args.ip,
    "ttl": 6000,
    "comment": "challenge-4"
    }]
    
new_rec = dom.add_records(record)

sys.stdout.write(json.dumps({new_rec}))
sys.stdout.flush()