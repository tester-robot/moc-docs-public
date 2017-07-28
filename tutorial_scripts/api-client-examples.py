import os

from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
from cinderclient.v2 import client as cinderclient

#glance stuff
from keystoneauth1 import loading
from keystoneauth1 import session
from glanceclient import Client as glanceclient

#Swift options
from swiftclient import Connection
from swiftclient.service import SwiftService


# There are several ways to set these variables in Python.  In this example, we
# assume you sourced the Openstack RC script and get the correct values from the
# environement. You could also read them into the script from a config file.
auth_url = os.environ.get('OS_AUTH_URL')
project_name = os.environ.get('OS_PROJECT_NAME')
project_id = os.environ.get('OS_PROJECT_ID')
username = os.environ.get('OS_USERNAME')
password = os.environ.get('OS_PASSWORD')
region = os.environ.get('OS_REGION_NAME')


## Nova
nova_version = 2
nova = novaclient.Client(nova_version,
                         username,
                         password,
                         project_name,
                         auth_url)

instances = nova.servers.list()
print instances

for svr in instances:
    print svr.id
    print svr.name
    print svr.status


## Neutron
neutron = neutronclient.Client(username=username,
                               password=password,
                               tenant_name=project_name,
                               auth_url=auth_url,
                               region_name=region)

nets = neutron.list_networks()
print nets


## Cinder
cinder = cinderclient.Client(username,
                             password,
                             project_name,
                             auth_url)

vols = cinder.volumes.list()
print vols

## Glance
GLANCE_ENDPOINT='https://glance.kaizen.massopencloud.org:9292'
loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(
    auth_url=auth_url,
    username=username,
    password=password,
    project_id=project_id)
session = session.Session(auth=auth)

glance = glanceclient('2', endpoint=GLANCE_ENDPOINT , session=session)

for img in glance.images.list():
    print img


## Swift
## Swiftclient offers both a higher level API called SwiftService, and a lower level API called SwiftClient

## SwiftService interface

# SwiftService API will actually use your environment auth variables if they are not specified in the script,
# but here is how to specify them explicitly:

options = {
    "auth_version": '2.0',
    "os_username": username,
    "os_password": password,
    "os_tenant_name": project_name,
    "os_auth_url": auth_url,
}

swift_service = SwiftService(options=options);
result = swift_service.list()
for item in result:
    for container in item['listing']:
        print container

## Connection interface
swift_conn = Connection(authurl=auth_url,
                              user=username,
                              key=password,
                              tenant_name=project_name,
                              auth_version=2)

headers, containers = swift_conn.get_account()

for con in containers:
    print con
    
