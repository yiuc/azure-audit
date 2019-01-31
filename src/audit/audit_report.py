from ddos_audit import auditreport as ddos_audit
from keyvault_audit import auditreport as kv_audit
from nsg_audit import auditreport as nsg_audit
from storage_account_audit import auditreport as sa_audit

import logging
import glob, os
import pandas as pd
import argparse
import subprocess
import sys

from pandas import DataFrame, ExcelWriter
from helper import azcli

if '__DEPLOY_DEBUG' in os.environ.keys():
    HTTP_CONNECTION_DEBUGLEVEL = 1
    LOG_LEVEL = logging.DEBUG
else:
    HTTP_CONNECTION_DEBUGLEVEL = 0
    LOG_LEVEL = logging.INFO

logging.basicConfig()
logging.getLogger().setLevel(LOG_LEVEL)  # Set this to DEBUG for deploy-api debug message output.
logger = logging.getLogger("audit_report")

def combineCSV():
    writer = ExcelWriter("../../auditreport.xlsx")
    for filename in glob.glob("../../report/*.csv"):
        logger.debug("Proceed CSV {}".format(filename))
        df_csv = pd.read_csv(filename)
        logger.debug(df_csv)
        (_, f_name) = os.path.split(filename)
        logger.debug("_ = {} and f_name = {}".format(_,f_name))
        (short_name, _) = os.path.splitext(f_name)
        df_csv.to_excel(writer, short_name, index=False)
    writer.save()

def setupSubscription(subscription_id):
    function=['az','account', 'set','-s', subscription_id]
    azcli(function)

parser = argparse.ArgumentParser(description='Pass the value')
parser.add_argument('--subscription-id', dest='subscription_id', required=True, help='Azure subscription_id')

args = parser.parse_args()
logger.debug(args)

setupSubscription(args.subscription_id)

logger.info("DDOS audit")
ddos_audit()
logger.info("Key vault audit")
kv_audit()
logger.info("NSG audit")
nsg_audit()
logger.info("Storage Account audit")
sa_audit()
logger.info("Create Excel")
combineCSV()