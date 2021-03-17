#!/usr/bin/python3

#IMPORTS
import sys
import grpc
import redis
import json
import logging
import ipaddress
from google.protobuf.any_pb2 import Any
from app_mongo import MongoFindPrefix
from app_telegram import NotificationAttackin,  NotificationAttackout
from app_ipam import GetData

import attribute_pb2
import capability_pb2
import gobgp_pb2
import gobgp_pb2_grpc
import attribute_pb2

import attribute_pb2_grpc
import capability_pb2_grpc
import gobgp_pb2_grpc
#END IMPORTS

# CONSTS
GET_DATA_MONGO = MongoFindPrefix()

GOBGP_HOST = '192.168.1.29'
GOBGP_PORT = 50051

REDIS_HOST = '192.168.1.29'
REDIS_PORT = 6379
REDIS_DB = 0

PREFIX_TO_BAN = 24
COMMUNITY_TO_BAN = 666
ORIGIN_TO_BAN = 2
LOCAL_PREF_TO_BAN = 1000

_get_ipam = GetData()
_send_telegram_in = NotificationAttackin()
_send_telegram_out = NotificationAttackout()


#NEXT_HOP_LIST_DIR = './next_hop_list.txt'
LOG_FILE_DIR = '/home/deivison/Dropbox/jobs/projeto_fnm/log/go.log'

ACTION_BAN = "ban"
ACTION_UNBAN = "unban"

LOG_LEVEL = logging.DEBUG
#END CONSTS

logging.basicConfig(level = LOG_LEVEL, filename = LOG_FILE_DIR, format='%(asctime)s:%(lineno)d - %(message)s')
channel = grpc.insecure_channel(GOBGP_HOST + ":" + str(GOBGP_PORT))
stub = gobgp_pb2_grpc.GobgpApiStub(channel)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf-8", decode_responses=True, db=REDIS_DB)

_TIMEOUT_SECONDS = 1000


def get_redis(net):
    ip_addr = str(f"ixdc_{net}_flow_dump")
    results = r.get(ip_addr)
    return results

def add_path(p):
    return stub.AddPath(gobgp_pb2.AddPathRequest(
        table_type=gobgp_pb2.GLOBAL,
        path=p
     ),
      _TIMEOUT_SECONDS,

     )

def del_path( p):
    return stub.DeletePath(gobgp_pb2.DeletePathRequest(table_type=gobgp_pb2.GLOBAL, path=p ),
     _TIMEOUT_SECONDS,)

def get_path(ip_addr, next_hop_addr, asn):
    nlri = Any()
    nlri.Pack(attribute_pb2.IPAddressPrefix(prefix=ip_addr, prefix_len=PREFIX_TO_BAN))

    next_hop = Any()
    next_hop.Pack(attribute_pb2.NextHopAttribute(next_hop=next_hop_addr))

    origin = Any()
    origin.Pack(attribute_pb2.OriginAttribute(origin=ORIGIN_TO_BAN))

    as_segment = attribute_pb2.AsSegment(
        # type=2,  # "type" causes syntax error
        numbers=[int(asn)]

        )

    as_segment.type = 2
    as_path = Any()
    as_path.Pack(attribute_pb2.AsPathAttribute(segments =[as_segment],))

    Path = gobgp_pb2.Path(
            nlri=nlri,
            pattrs=[origin, as_path, next_hop],
            family=gobgp_pb2.Family(afi=gobgp_pb2.Family.AFI_IP, safi=gobgp_pb2.Family.SAFI_UNICAST),
        )
    return Path

def get_data_mongo(ip_addr):
    v = ipaddress.ip_address(ip_addr).version
    if v == 4:
        x = ipaddress.IPv4Network(f'{ip_addr}/24',  strict=False)
        r2 = GET_DATA_MONGO(x)
        return r2
    if v == 6:
        y = ipaddress.IPv6Network(f'{ip_addr}/32',  strict=False)
        r4 = GET_DATA_MONGO(y)
        return r4

def family(net):
    v = ipaddress.ip_address(ip_addr).version
    list_mask = [24,25,26,27,28,29,30,32]
    if v == 4:
        x = ipaddress.IPv4Network(f'{ip_addr}/24',  strict=False)
        r2 = GET_DATA_MONGO(x)
        return r2
    if v == 6:
        y = ipaddress.IPv6Network(f'{ip_addr}/32',  strict=False)
        r4 = GET_DATA_MONGO(y)
        return r4
   

class AddMitigation:
    def __call__(self, ip_addr ):
        subnet = ipaddress.IPv4Network(f'{ip_addr}/24',  strict=False).network_address
        mitigating = r.get(str(subnet))
        on_redis = get_redis(ip_addr)
        on_ipam = _get_ipam(f'{subnet }/24')
        if mitigating == None:
            r1 = get_data_mongo(ip_addr)
            asn = r1['asn']
            hop = r1['hop']
            save_redis = r.set(str(subnet), 1 )
            add_path(get_path(str(subnet), hop, asn))
            _send_telegram_in(on_ipam[2], asn, ip_addr, on_redis, on_ipam[0], on_ipam[1])
            logging.debug(f"Not found this prefix on redis, lets add: {subnet}")
            raise SystemExit
        if int(mitigating) >= 1:
            valor = (int(mitigating) + 1)
            save_redis = r.set(str(subnet), valor)
            logging.debug(f'{subnet}: already on')
            raise SystemExit


class DeleteMitigation:
    def __call__(self, ip_addr):
        subnet = ipaddress.IPv4Network(f'{ip_addr}/24',  strict=False).network_address
        mitigating = r.get(str(subnet))
        on_ipam = _get_ipam(f'{subnet }/24')
        if int(mitigating) == 1:
            r1 = get_data_mongo(ip_addr)
            asn = r1['asn']
            hop = r1['hop']
            r.delete(str(subnet))
            del_path(get_path(str(subnet), hop, asn))
            _send_telegram_out(on_ipam[1])
            logging.debug(f"{subnet} Removed path from rib via path information.")
        if int(mitigating) >= 2:
            valor = (int(mitigating) - 1)
            save_redis = r.set(str(subnet), valor)
            logging.debug(f'{subnet}: already on and -1')
        else:
            raise SystemExit


