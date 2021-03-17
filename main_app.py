#!/usr/bin/python3
import sys
import optparse
import logging
from app_go import AddMitigation, DeleteMitigation

LOG_FILE = '/home/deivison/Dropbox/jobs/projeto_fnm/log/fastnetmon_app.log'

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(formatter)
logger.addHandler(handler)

_add_gobgp = AddMitigation()
_delete_gobgp = DeleteMitigation()

ip_addr = sys.argv[1]
data_direction = sys.argv[2]
pps_as_string = int(sys.argv[3])
action = sys.argv[4]

logger.info(" - " . join(sys.argv))



try:

    if action == "unban":
        _delete_gobgp(ip_addr)
        logger.info('Delete IP RIB GOBGP:' + ip_addr)
        sys.exit(0)
    elif action == "ban":
        body = "".join(sys.stdin.readlines())
        _add_gobgp(ip_addr)
        logger.info('ADD RIB GOBGP:' + ip_addr)
        sys.exit(0)

    else:
        sys.exit(0)

except Exception as e:
    logger.critical(str(e))
