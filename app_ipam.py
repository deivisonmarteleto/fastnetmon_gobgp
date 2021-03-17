#!/usr/bin/python3

from phpipam_client import PhpIpamClient, GET, PATCH
from datetime import datetime
import logging
from modulo_mysql import UseDatabase
import ipaddress 

#DB Configuração
dbconfig = {'user' : 'root',
            'password' : 'temp@2010',
            'host' : '127.0.0.1',
            'database' : 'phpipam'}

#Conexao IPAM API
ipam = PhpIpamClient(
                    url='http://127.0.0.1:8080',
                    app_id='app',
                    token='SiabDO7F4sJwcQn6p_Iu-dHWh5E5in6l',
                    username='api_user',
                    password='temp2010',
                    encryption=False,
                    )



class GetIpamQuery:
    def __call__(self, query):
        with UseDatabase(dbconfig) as cursor:
            _SQL = query
            cursor.execute(_SQL)
            data = cursor.fetchall()
            return data
            

class GetCustomer(GetIpamQuery):
    def __call__(self, _id):
        cx = GetIpamQuery()
        return cx(f"SELECT title, custom_Chat_ID, contact_person, contact_mail from customers WHERE id like '%{_id}%'")[0]

   

class GetData(GetCustomer):
    def __call__(self, net):
        subnet = net
        x = GetCustomer()
        r1 = ipam.get(f'/subnets/cidr/{subnet}')[0]
        r2 = x(r1['customer_id'])
        return r2





