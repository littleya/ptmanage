import os

from oslo_log import log as logging
import requests

from ptmanage.client import base
from ptmanage.conf import CONF

LOG = logging.getLogger(__name__)


class Client(base.BaseClient):
    def __init__(self, links):
        super(Client, self).__init__(links)

    def _get_torrent_file(self):
        self.torrent_contexts = {}
        for key in self.links.keys():
            self.torrent_contexts[key] = requests.get(self.links[key]).content

    def upload(self):
        self._get_torrent_file()
        for tid in self.torrent_contexts:
            local_path = os.path.join(CONF.local.path, str(tid)+'.torrent')
            with open(local_path, 'wb') as f:
                f.write(self.torrent_contexts[tid])
            LOG.info('add torrent: {}'.format(str(tid)))
