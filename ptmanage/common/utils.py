import importlib

from ptmanage.conf import CONF


CLIENT_MAPPING = {
    'local': 'ptmanage.client.local',
    'remote': 'ptmanage.client.remote'
}

SITE_MAPPING = {
    'u2': 'ptmanage.site.u2'
}


def get_enabled_clients():
    for client in CONF.enabled_clients:
        if CLIENT_MAPPING.get(client, None):
            yield(getattr(importlib.import_module(CLIENT_MAPPING.get(client)),
                          'Client'))


def get_enabled_sites():
    enabled_sites = {}
    for site in CONF.enabled_sites:
        if SITE_MAPPING.get(site, None):
            enabled_sites[site] = getattr(importlib.import_module(
                SITE_MAPPING.get(site)), 'PeriodicTask')
    return enabled_sites
