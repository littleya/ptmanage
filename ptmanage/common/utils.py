import importlib

from oslo_log import log as logging

from ptmanage.conf import CONF


LOG = logging.getLogger(__name__)

CLIENT_MAPPING = {
    'local': 'ptmanage.client.local',
    'remote': 'ptmanage.client.remote',
    'deluge': 'ptmanage.client.deluge',
    'qbittorrent': 'ptmanage.client.qbittorrent',
    'transmission': 'ptmanage.client.transmission'
}

SITE_MAPPING = {
    'u2': 'ptmanage.site.u2',
    'opencd': 'ptmanage.site.opencd',
}

NOTIFY_MAPPING = {
    'telegram': 'ptmanage.notification.telegram'
}

NOTIFY_CLIENT = None


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


def get_enabled_notify_clients():
    enabled_notify_clients = []
    for client in CONF.enabled_notify_clients:
        if NOTIFY_MAPPING.get(client, None):
            enabled_notify_clients.append(
                getattr(importlib.import_module(NOTIFY_MAPPING.get(client)),
                        'NotifyClient'))
    return enabled_notify_clients


def notify(msg):
    global NOTIFY_CLIENT
    if not NOTIFY_CLIENT:
        NOTIFY_CLIENT = get_enabled_notify_clients()
    for client in NOTIFY_CLIENT:
        LOG.info('notify online')
        client().notify(msg)
