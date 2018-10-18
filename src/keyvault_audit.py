import subprocess
import json
import csv
import logging

from helper import azcli

# Logging assumed to have been initialised outside of this module.
logger = logging.getLogger("keyvault_audit")

def auditreport():
    # list out the keyvault
    out = azcli(['az','keyvault', 'list'])
    kv_list = json.loads(out)

    with open('../report/keyvault_audit.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["name",
                            "defaultAction",
                            "IP allow",
                            "virtualNetworkRules allow"])
        # list out each config by name
        for kv in kv_list:
            logger.debug(kv)
            out = azcli(['az','keyvault', 'network-rule','list','--name',kv["name"]])
            kv_netrule = json.loads(out)
            # create the ip list
            iplist_allow = "\n".join(ip["value"] for ip in kv_netrule["ipRules"])
            # get the vitual network rule
            virtualNetworkrule_allow = "\n".join(rule["id"].split("/")[-1] for rule in kv_netrule["virtualNetworkRules"])
            # write to CSV
            csv_writer.writerow([kv['name'],
                                kv_netrule['defaultAction'],
                                iplist_allow,
                                virtualNetworkrule_allow])