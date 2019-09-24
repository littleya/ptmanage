import os

from oslo_log import log as logging
import paramiko
import requests

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
        elif client.sock.closed:
            self._init_client()
        else:
            self.client = client

    def _init_client(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(CONF.remote.host,
                    port=CONF.remote.port,
                    username=CONF.remote.username,
                    password=CONF.remote.password)
        self.client = paramiko.SFTPClient.from_transport(ssh.get_transport())
        global client
        client = self.client

    def _get_torrent_file(self):
        self.torrent_contexts = {}
        for key in self.links.keys():
            self.torrent_contexts[key] = requests.get(self.links[key]).content

    def upload(self):
        self._get_torrent_file()
        for tid in self.torrent_contexts:
            local_path = os.path.join('/tmp', str(tid))
            with open(local_path, 'wb') as f:
                f.write(self.torrent_contexts[tid])
            remtoe_path = os.path.join(CONF.remote.path, str(tid)+'.torrent')
            self.client.put(local_path, remtoe_path)
            os.remove(local_path)
            LOG.info('add torrent: {}'.format(str(tid)))
