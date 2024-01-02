#!/bin/python3.9

import logging

from oci import resource_search
from oci import pagination
from oci.util import to_dict
from modules.utils import Utilities


class Search:
    def __init__(self, config, signer=None):
        self.client = resource_search.ResourceSearchClient(config, signer=signer)
        # Holds search results; Is either type list[dict] or None
        self.inventory = None
        self.log = logging.getLogger(f'{__name__}.Search')
        self.log.debug(f'Initialized Search object: {self}')

    def get_inventory(self) -> list[dict]:
        self.log.info('Returning search results')
        return self.inventory

    def search_vnics(self, **kwargs):
        self.log.info('Searching for VNICs')
        search = resource_search.models.StructuredSearchDetails(
            type = 'Structured',
            query = 'query vnic resources'
        )
        if 'compartment' in kwargs:
            search.query += f' in compartment {kwargs.get("compartment")}'
        self.log.debug(f'Search Details: {search}')

        # Return additional fields required for script
        search.query += f' return allAdditionalFields'

        response = pagination.list_call_get_all_results(
            self.client.search_resources,
            search_details=search
            )
        self.log.debug(Utilities.print_response_metadata(response))
        self.inventory = to_dict(response.data)
    
    # Convenience method for when only OCIDs are required
    def search_vnics_ids(self, **kwargs):
        self.log.info('Getting VNIC OCIDs')
        ocids = []
        self.search_vnics(kwargs)
        for item in self.inventory:
            ocids.append(item['identifier'])

        self.inventory = ocids
    
    def filter_search_results(self, **kwargs):
        self.log.info('Filtering results')
        self.log.debug(f'Filtering parameters: {kwargs}')
        new_inventory = []

        # Main loop going over items in inventory
        for item in self.inventory:
            include = False

            # Field subnetId nested in additional_details field - Doing this manually
            if 'subnetId' in kwargs:
                pass

            for key, value in kwargs.items():
                if key in item and item[key] == value:
                    new_inventory.append(item)

        self.inventory = new_inventory
