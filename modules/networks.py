#!/bin/python3.9

import logging

from oci.core import VirtualNetworkClient, models
from modules.utils import Utilities

class Networks:
    def __init__(self, config, signer=None):
        self.client = VirtualNetworkClient(config, signer=signer)
        self.log = logging.getLogger(f'{__name__}.Networks')
        self.log.debug(f'Initlialized Networks object: {self}')

    def get_vnic(self, vnic: str) -> models.Vnic:
        response = self.client.get_vnic(vnic)
        self.log.debug(
            f'get_vnic Response: {Utilities.print_response_metadata(response)}'
            )
        return response.data