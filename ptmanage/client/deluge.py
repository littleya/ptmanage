import os

import deluge_client
from oslo_log import log as logging

from ptmanage.client import base
from ptmanage.conf import CONF


client = None
LOG = logging.getLogger(__name__)


class Client(base.BaseClient):

    def __init__(self, links):
        super(Client, self).__init__(links)
        global client
        if client is None:
            self._init_client()
        else:
            self.client = client

        if not self.client.connected:
            self.client.connect()

    def _init_client(self):
        self.client = deluge_client.DelugeRPCClient(
            CONF.deluge.host, CONF.deluge.port,
            CONF.deluge.username, CONF.deluge.password)
        global client
        client = self.client

    def upload(self):
        for tid, link in self.links.items():
            self.client.call(
                'core.add_torrent_url', link,
                {'add_paused': False,
                 'download_location': os.path.join(
                     CONF.deluge.base_location, str(tid))
                 })
            LOG.info('add torrent: {}'.format(str(tid)))
