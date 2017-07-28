import os
from openstack import connection
from openstack import profile

## AUTH PARAMETERS
# There are several ways to set these variables in Python.  In this example, we
# assume you sourced the Openstack RC script and get the correct values from the
# environement. You could also read them into the script from a config file.
auth_url = os.environ.get('OS_AUTH_URL')
project_name = os.environ.get('OS_PROJECT_NAME')
username = os.environ.get('OS_USERNAME')
password = os.environ.get('OS_PASSWORD')
region = os.environ.get('OS_REGION_NAME')


## INSTANCE PARAMETERS
# Make sure these values are appropriate for your OpenStack cluster and desired
# instance configuration. You can specify images and flavors by name or ID.  To
# see what's available, you can generally run the command:
#    $ `openstack <resource> list
# replacing <resource> with what you want a list of, such as `image`, `flavor', 
# `network`, `keypair`, or something else.

INSTANCE_NAME='Python Test Image'
IMAGE='CentOS 7 cloud'
#IMAGE='613a9ff5-c7de-4b34-86b6-a554998787b3'
FLAVOR='m1.small'
#FLAVOR=2
NETWORK_NAME='NETWORK NAME HERE'
KEYPAIR='KEYPAIR NAME HERE'



def create_connection(auth_url,region,project_name,username,password):
    """ Connect and authenticate to OpenStack
 
    This function came straight from the Openstack docs:
    http://developer.openstack.org/sdks/python/openstacksdk/users/guides/connect.html
    """
    prof = profile.Profile()
    prof.set_region(profile.Profile.ALL, region) 
    return connection.Connection(
        profile=prof,
        user_agent='examples',
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password) 

def simple_connect(auth_url, project_name, username, password):
    auth_args = {
        'auth_url': auth_url,
        'project_name': project_name,
        'username': username,
        'password': password,
    }  
    return connection.Connection(**auth_args)

# connect & authenticate
conn = create_connection(auth_url,region,project_name,username,password)

# Get resources
img = conn.compute.find_image(IMAGE)
flavor = conn.compute.find_flavor(FLAVOR)
network = conn.network.find_network(NETWORK_NAME)
keypair = conn.compute.find_keypair(KEYPAIR)

# create an instance
test_instance = conn.compute.create_server(
    name='testPython2', 
    image_id=img.id, 
    flavor_id=flavor.id, 
    networks=[{"uuid": network.id}], 
    key_name=keypair.name)

print(test_instance)

