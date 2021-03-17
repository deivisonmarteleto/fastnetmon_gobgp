#!/usr/bin/python3

import requests
import json
import telegram





#VARIABLE

BOT_TOKEN = '1443770125:AAFVl1XxjCfMv-vHWsfgcq65BLELGsuWmwM'
URL = 'https://api.telegram.org/bot'



class NotificationAttackin:

    def __call__(self, name, asn, ipaddr, redislog, tittle, chatID):
        bot_chatID = chatID
        msg = f""" 
Saudações,  {name}!


Comunicamos que um novo ataque DDoS teve início!

❌ ASN: {asn} CUSTOMER: ({tittle}) - IP: {ipaddr} 

Fique tranquilo, seu tráfego está protegido. Nosso sistema de mitigação automática já está em ação.

----------------

{redislog}
"""

        send_text = URL + BOT_TOKEN + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + msg
        response = requests.get(send_text)
        return response.json()


class NotificationAttackout:

    def __call__(self, chatID):
        bot_chatID = chatID
        msg = f""" 
 
✅ Fim do  Ataque!

----

Evite interrupções de conexão, operações indisponíveis por períodos longos e prejuízos financeiros causados por ataques DDoS.

Mitigação automatizada: ação próxima da origem e com tráfego nacional. 

        
        """

        send_text = URL + BOT_TOKEN + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + msg
        response = requests.get(send_text)
        return response.json()
