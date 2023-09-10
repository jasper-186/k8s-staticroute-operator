import kopf
from pyroute2 import IPRoute
from pyroute2 import NDB
from pyroute2 import IPDB
from api.v1.types import StaticRoute
from constants import DEFAULT_DEPLOYMENT_LABEL
from constants import DEFAULT_GW_CIDR
from constants import NOT_USABLE_IP_ADDRESS
from constants import ROUTE_EVT_MSG
from constants import ROUTE_READY_MSG
from constants import ROUTE_NOT_READY_MSG
from utils import valid_ip_address
from kubernetes import client, config


config.load_incluster_config()
api=client.CoreV1Api()
pod_wireguard=api.list_pod_for_all_namespaces(label_selector=f"app==app-wireguard")        
gateway = pod_wireguard.items[0].status.pod_ip 
#with IPRoute() as ipr:
#  ipr.route('add', dst='192.68.21.0/24', gateway=gateway, )
  

with NDB() as ndb:
  ndb.routes.add({'dst': '192.68.21.0/24', 'multipath': [{'gateway': gateway, 'hops': 1}]})

#with IPDB() as ipdb:
#  ipdb.routes.add({'dst': '192.68.21.0/24', 'multipath': [{'gateway': gateway, 'hops': 1}]})