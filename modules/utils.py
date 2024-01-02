#!/bin/python3.9

import logging

from os import getenv
from oci import Signer

from oci.auth import signers
from oci.config import from_file, get_config_value_or_default, DEFAULT_LOCATION, DEFAULT_PROFILE
from oci.response import Response

log = None

"""Utilities contains static methods that can be leveraged by other classes
    for the purposes of code comprehension elsewhere
"""
class Utilities:
    def __init__(self):
        global log
        log = logging.getLogger(__name__)
        log.debug(f'Initialized Utilities object: {self}')

    @staticmethod
    def print_response_metadata(response: Response) -> str:
        return (f'Response metadata:\n'
                f'\thas_next_page: {response.has_next_page}\n'
                f'\theaders: {response.headers}\n'
                f'\tnext_page: {response.next_page}\n'
                f'\trequest id: {response.request_id}\n'
                f'\trequest: \n\t\t{response.status} {response.request.method} {response.request.url}\n'
                f'\t\tHeader {response.request.header_params}\n'
                f'\t\tParameters {response.request.query_params}\n'
                f'\t\tType {response.request.response_type}\n'
                f'\t\tEnforce Content Headers {response.request.enforce_content_headers}\n'
                f'\t\tBody {response.request.body}')

    # Will need to decide to either pass the client from main or pass the signer and
    # let class handle it's own client
    @staticmethod
    def make_client(client_type: object, config: dict, signer=None, **kwargs) -> object:
        log.debug(f'Making client with parameters:\n\tclient_type: {client_type}'
                  f'\n\tConfig: {config}\n\tSigner: {signer}')
        client = None
        if signer is None:
            client = client_type(config, **kwargs)
        else:
            client = client_type({}, signer=signer, **kwargs)

        return client
    
    
    @staticmethod
    def create_signer(profile: str, instance_principal: bool, delegation_token: bool):
        # TODO Validation here
        log.info('Creating Signer')
        log.debug(f'Creating signer with args \nProfile: {profile} \n'
                  'Instance Principal: {instance_principal} \n'
                  'Delegation Token: {delegation_token}')
        if instance_principal:
            try:
                signer = signers.InstancePrincipalsSecurityTokenSigner()
                cfg = {'region': signer.region, 'tenancy': signer.tenancy_id}
                log.debug(f'Instance Principal signer created: {signer}\nConfig: {cfg}')
                return cfg, signer
            
            except Exception as e:
                log.error(f'Instance Principal signer failed due to exception {e}')
                raise SystemExit
            
        elif delegation_token:
            try:
                # Environment variables present in OCI Cloud Shell
                env_config_file = getenv('OCI_CONFIG_FILE')
                env_config_section = getenv('OCI_CONFIG_PROFILE')

                if not env_config_file or not env_config_section:
                    log.error('Missing delegation token configuration')
                    raise SystemExit

                config = from_file(env_config_file, env_config_section)
                delegation_token_location = config["delegation_token_file"]

                with open(delegation_token_location, 'r') as delegation_token_file:
                    delegation_token = delegation_token_file.read().strip()
                    signer = signers.InstancePrincipalsDelegationTokenSigner(delegation_token=delegation_token)

                    return config, signer
            except KeyError as e:
                log.error(f'Key Error exception during Delegation Token retrieval {e}')
                raise SystemExit
            except Exception as e:
                log.error(f'Exception during Delegation Token retrieval {e}')
                raise

        else:
            config = from_file(
                DEFAULT_LOCATION,
                (profile if profile else DEFAULT_PROFILE)
            )
            signer = Signer(
                tenancy=config["tenancy"],
                user=config["user"],
                fingerprint=config["fingerprint"],
                private_key_file_location=config.get("key_file"),
                pass_phrase=get_config_value_or_default(config, "pass_phrase"),
                private_key_content=config.get("key_content")
            )
            return config, signer
