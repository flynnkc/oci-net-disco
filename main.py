#!/bin/python3.9

import logging
import argparse
import json

from oci.config import from_file
from modules.utils import Utilities
from modules.search import Search

log = None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compartment', help='Compartment OCID to perform \
                        operations on')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--ip', action='store_true',
                        help='Use Instance Principal authnetication')
    parser.add_argument('--dt', action='store_true',
                        help='Use Delegation Token authnetication')
    parser.add_argument('-p', '--profile', help='Profile to use from config file \
                        -- Defaults to DEFAULT', default='DEFAULT')
    #parser.add_argument('--config', help='Config file location',
    #                    default='~/.oci/config')
    parser.add_argument('--subnet', help='OCID of Subnet to scan')
    args = parser.parse_args()

    # Configuration and other overhead
    _set_config(args)
    log.debug(f'Started script with args: {args}')
    config, signer = Utilities.create_signer(args.profile, args.ip, args.dt)

    # Search for objects
    search = Search(config, signer=signer)
    search.search_vnics(compartment=args.compartment, subnet=args.subnet)
    print(json.dumps(search.get_inventory(), indent=4))


# Set dependencies on modules
def _set_config(args: argparse.Namespace):
    # Init logging for utility functions
    Utilities()
    global log
    # Debug mode
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    # Default: Log if error, otherwise be silent
    else:
        logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger(__name__)


if __name__ == '__main__':
    main()