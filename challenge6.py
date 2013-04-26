#!/usr/bin/env python

"""challenge6.py: Response to Challenge 6 of Rackspace API Challenge"""
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

parser = argparse.ArgumentParser(description='Challenge 6: Create a CDN enabled container')
args = parser.parse_args()

# create the container
sys.stderr.write('Creating container...')
cont = cf.create_container('ch6_container')
sys.stderr.write('done.\n')

# publish it to the CDN
sys.stderr.write('Publishing container...')
cont.make_public(ttl=1200)
sys.stderr.write('done.\n')

sys.stdout.write(json.dumps({"cdn_enabled": cont.cdn_enabled, "cdn_ttl": cont.cdn_ttl, 
    "cdn_log_retention": cont.cdn_log_retention, "cdn_uri": cont.cdn_uri, 
    "cdn_ssl_uri": cont.cdn_ssl_uri, "cdn_streaming_uri": cont.cdn_streaming_uri, 
    "cdn_ios_uri": cont.cdn_ios_uri}, indent=4, separators=(',', ': ')))
sys.stdout.write("\n")