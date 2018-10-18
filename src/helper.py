import argparse
import subprocess
import sys
import logging

logger = logging.getLogger("helper")

def azcli(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = process.communicate()
    logger.debug(str(out,"utf-8"))
    exit_code = process.returncode
    if exit_code and exit_code != 0:
        logger.error("{}".format(str(err,"utf-8")))
        sys.exit(exit_code)
    else:
        return out