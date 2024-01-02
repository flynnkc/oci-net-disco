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
        self.log.info(f'Returning search results -- Found {len(self.inventory)} items')
        return self.inventory

    def search_vnics(self, compartment=None, subnet=None, **kwargs):
        self.log.info('Searching for VNICs')
        search = resource_search.models.StructuredSearchDetails(
            type = 'Structured',
            # Return allAdditionalFields required for extracting subnet
            query = 'query vnic resources return allAdditionalFields'
        )
        if compartment:
            search.query += f" where compartmentId = '{compartment}'"
        self.log.debug(f'Search Details: {search}')

        response = pagination.list_call_get_all_results(
            self.client.search_resources,
            search_details=search
            )
        self.log.debug(Utilities.print_response_metadata(response))
        self.inventory = to_dict(response.data)

        # If subnet is provided we will need to filter results because
        # search will not include additionalDetails fields as valid targets
        # of the 'where' clause
        if subnet:
            self.filter_search_results(subnetId=subnet)
    
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
        
        # Nested fields -- Unable to loop easily
        subnetId = kwargs.pop('subnetId', None)

        # Main loop going over items in inventory
        for item in self.inventory:
            # Start out False and flip to True if any match
            # i.e. functions like an OR statement
            include = False

            if subnetId:
                if item['additional_details']['subnetId'] == subnetId:
                    include = True


            for key, value in kwargs.items():
                if key in item and item[key] == value:
                    include = True

            if include: new_inventory.append(item)

        self.inventory = new_inventory
