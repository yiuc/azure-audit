import subprocess
import json
import csv
import logging

from helper import azcli

# Logging assumed to have been initialised outside of this module.
logger = logging.getLogger("ddos_audit")

def auditreport():
    # list out the keyvault
    out = azcli(['az','network','nsg', 'list'])
    nsg_list = json.loads(out)

    with open('../../report/nsg_audit.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([
                            "rg-name",
                            "nsg-name",
                            "direction",
                            "priority",
                            "rule-name",
                            "port",
                            "protocol",
                            "source",
                            "destination",
                            "action",
                            "description"
                            ])
        # list out each config by name
        for nsg in nsg_list:
            logger.debug(nsg)
            out = azcli(['az','network','nsg','rule', 'list', '--nsg-name',nsg['name'],'-g',nsg['resourceGroup']])
            nsg_rule = json.loads(out)
            for defrule in nsg['defaultSecurityRules']:
                logger.debug("Range {} Ranges {}".format(defrule["destinationPortRange"],defrule["destinationPortRanges"]))
                port=defrule["destinationPortRange"] if defrule["destinationPortRange"] is not None else ""
                port+="\n".join(defrule["destinationPortRanges"]) if defrule["destinationPortRanges"] is not None else ""
                logger.debug("Source {} Ranges {}".format(defrule["sourceAddressPrefix"],defrule["sourceAddressPrefixes"]))
                sourceaddress=defrule["sourceAddressPrefix"] if defrule["sourceAddressPrefix"] is not None else ""
                sourceaddress=sourceaddress+"\n".join(defrule["sourceAddressPrefixes"]) if defrule["sourceAddressPrefixes"] is not None else ""
                logger.debug("Dest {} Ranges {}".format(defrule["destinationAddressPrefix"],defrule["destinationAddressPrefixes"]))
                destinationAddress=defrule["destinationAddressPrefix"] if defrule["destinationAddressPrefix"] is not None else ""
                destinationAddress=destinationAddress+"\n".join(defrule["destinationAddressPrefixes"]) if defrule["destinationAddressPrefixes"] is not None else ""
                # write to CSV
                csv_writer.writerow([
                            nsg['resourceGroup'],
                            nsg['name'],
                            defrule['direction'],
                            defrule['priority'],
                            defrule['name'],
                            port,
                            defrule['protocol'],
                            sourceaddress,
                            destinationAddress,
                            defrule['access'],
                            defrule['description']
                            ])
            for rule in nsg_rule:
                logger.debug("Range {} Ranges {}".format(rule["destinationPortRange"],rule["destinationPortRanges"]))
                port=rule["destinationPortRange"] if rule["destinationPortRange"] is not None else ""
                port+="\n".join(rule["destinationPortRanges"]) if rule["destinationPortRanges"] is not None else ""
                logger.debug("Source {} Ranges {}".format(rule["sourceAddressPrefix"],rule["sourceAddressPrefixes"]))
                sourceaddress=rule["sourceAddressPrefix"] if rule["sourceAddressPrefix"] is not None else ""
                sourceaddress=sourceaddress+"\n".join(rule["sourceAddressPrefixes"]) if rule["sourceAddressPrefixes"] is not None else ""
                logger.debug("Dest {} Ranges {}".format(rule["destinationAddressPrefix"],rule["destinationAddressPrefixes"]))
                destinationAddress=rule["destinationAddressPrefix"] if rule["destinationAddressPrefix"] is not None else ""
                destinationAddress=destinationAddress+"\n".join(rule["destinationAddressPrefixes"]) if rule["destinationAddressPrefixes"] is not None else ""
                # write to CSV
                csv_writer.writerow([
                            nsg['resourceGroup'],
                            nsg['name'],
                            rule['direction'],
                            rule['priority'],
                            rule['name'],
                            port,
                            rule['protocol'],
                            sourceaddress,
                            destinationAddress,
                            rule['access'],
                            rule['description']
                            ])