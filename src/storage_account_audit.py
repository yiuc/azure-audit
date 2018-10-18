import subprocess
import json
import csv
import logging

from helper import azcli

# Logging assumed to have been initialised outside of this module.
logger = logging.getLogger("ddos_audit")

def auditreport():
    # list out the keyvault

    out = azcli(['az','storage','account', 'list'])
    sa_list = json.loads(out)

    with open('../report/storage_account_audit.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["name",
                            "defaultAction",
                            "IP allow",
                            "IP deny",
                            "virtualNetworkRules allow",
                            "virtualNetworkRules deny"])
        # list out each config by name
        for sa in sa_list:
            logger.debug(sa)
            sa_netrule = sa["networkRuleSet"]
            # create the ip list
            iplist_allow = "\n".join(ip["ipAddressOrRange"] for ip in sa_netrule["ipRules"] if ip["action"] == "Allow")
            iplist_deny = "\n".join(ip["ipAddressOrRange"] for ip in sa_netrule["ipRules"] if ip["action"] == "Deny")
            # get the vitual network rule
            virtualNetworkrule_allow = "\n".join(rule["virtualNetworkResourceId"].split("/")[-1] for rule in sa_netrule["virtualNetworkRules"] if rule["action"] == "Allow")
            virtualNetworkrule_deny = "\n".join(rule["virtualNetworkResourceId"].split("/")[-1] for rule in sa_netrule["virtualNetworkRules"] if rule["action"] == "Deny")
            # write to CSV
            csv_writer.writerow([sa['name'],
                        sa_netrule['defaultAction'],
                        iplist_allow,
                        iplist_deny,
                        virtualNetworkrule_allow,
                        virtualNetworkrule_deny])