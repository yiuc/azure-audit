import subprocess
import json
import csv
import logging

from helper import azcli

# Logging assumed to have been initialised outside of this module.
logger = logging.getLogger("ddos_audit")

def auditreport():
    
    out = azcli(['az','network', 'ddos-protection', 'list'])
    ddosList = json.loads(out)

    with open('../../report/ddos_audit.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["name","type"])
        for ddos in ddosList:
            logger.debug(ddos)
            csv_writer.writerow([ddos['name'],ddos['type']])
