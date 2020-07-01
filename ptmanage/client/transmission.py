import os

from oslo_log import log as logging
from transmission_rpc import Client as tr_client

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

    def _init_client(self):
        self.client = tr_client(
            host=CONF.transmission.host,
            port=CONF.transmission.port,
            username=CONF.transmission.username,
            password=CONF.transmission.password)
        global client
        client = self.client

    def upload(self):
        for tid, link in self.links.items():
            self.client.add_torrent(
                link, paused=False, download_dir=os.path.join(
                    CONF.transmission.base_location, str(tid)))
            LOG.info('add torrent: {}'.format(str(tid)))
