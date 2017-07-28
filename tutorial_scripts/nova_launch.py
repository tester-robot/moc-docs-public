import os
import json
import pprint

from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient



# There are several ways to set these variables in Python.  In this example, we
# assume you sourced the Openstack RC script and get the correct values from the
# environement. You could also read them into the script from a config file.
auth_url = os.environ.get('OS_AUTH_URL')
project_name = os.environ.get('OS_PROJECT_NAME')
project_id = os.environ.get('OS_PROJECT_ID')
username = os.environ.get('OS_USERNAME')
password = os.environ.get('OS_PASSWORD')
region = os.environ.get('OS_REGION_NAME')

##Authenticate to Keystone
#keystone = keystoneclient.Client(username=username,
#                                 password=password,
#                                 tenant_name=project_name,
#                                 auth_url=auth_url)

## Neutron
#neutron = neutronclient.Client(username=username,
#                               password=password,
#                               tenant_name=project_name,
#                               auth_url=auth_url,
#                               region_name=region)

#nets = neutron.list_networks()

#print nets

INSTANCE_NAME='Test NovaClient'
IMAGE_NAME='Centos 7'
FLAVOR_NAME='m1.small'
KEYPAIR='kamfonik-thinkpad'

nova_version = 2

nova = novaclient.Client(nova_version,
                         username,
                         password,
                         project_name,
                         auth_url)

image = nova.images.find(name=IMAGE_NAME)
flavor = nova.flavors.find(name=FLAVOR_NAME)
network = nova.networks.find(label='test_network')
keypair = nova.keypairs.find(name=KEYPAIR)



server = nova.servers.create(INSTANCE_NAME, image, flavor, nics=[{'net-id': network.id}], key_name=keypair.name)

print server

#create(name, image, flavor, meta=None, files=None, reservation_id=None, min_count=None, max_count=None, security_groups=None, userdata=None, key_name=None, availability_zone=None, block_device_mapping=None, block_device_mapping_v2=None, nics=None, scheduler_hints=None, config_drive=None, disk_config=None, admin_pass=None, access_ip_v4=None, access_ip_v6=None, **kwargs)
