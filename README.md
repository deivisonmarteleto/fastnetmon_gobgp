Olá!

This script integrates Fastnetmon to Gobgp with notice to Telegram, consulting the client's Chat_ID in PHP Ipam.

* In order to work correctly, it is necessary to make some customizations in PHPIpam:

- go to the "Custom fields" option, in the "Custom Customers fields" part, and create a field with the name "Chat_ID" option "varchar".

- Have the project already applied:
- modulo_mysql.py configure with PHP IP IPAM (get the Chat_ID)

1) Install "requirements.txt":
      pip3 install requirements.txt

2) perform the Gobgp configuration and start.

3) Customize the "/etc/fastnetmon.conf" file
- change the field to (notify_script_path = /.../main_app.py)
- enable redis
- enable the mongo
- Do not enable Gobgp on the file.
- perform the rest of the settings according to your network.

4) Install Redis and Mongo

5) Customize your telegram message to customers (app_telegram.py)

This script is suitable for IPS, Telecom Operators or Datacenters that have ASN.

In each attack the Script is triggered by Fastnetmon, queries MongoDB looking for the correct ASN, NEXTHOP of the Subnet that is under attack and performs the announcement for the Edge Router.


On the edge router it has a route-map that adds a larger prefix and adds a mitigation communites.

The script performs ads "/ 24"

# Enjoy! 
