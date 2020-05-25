import os

import requests
from oslo_log import log as logging

from ptmanage.client import base
from ptmanage.conf import CONF


LOG = logging.getLogger(__name__)


class Client(base.BaseClient):

    def __init__(self, links):
        super(Client, self).__init__(links)
        self.url = f'http://{CONF.qbittorrent.host}:{CONF.qbittorrent.port}'

    def get_cookie(self):
        login_url = f'{self.url}/login'
        data = {
            'username': CONF.qbittorrent.username,
            'password': CONF.qbittorrent.password
        }
        result = requests.post(login_url, data=data)
        if result.status_code == 200 and result.text == 'Ok.':
            return result.headers.get('set-cookie')
        else:
            raise Exception('Failed to log in qbittorrent.')

    def upload(self):
        url = f'{self.url}/command/download'
        headers = {'Cookie': self.get_cookie(),
                   'Content-Type': 'application/x-www-form-urlencoded'}
        for tid, link in self.links.items():
            data = {
                'urls': link,
                'savepath': os.path.join(CONF.qbittorrent.base_location,
                                         str(tid)),
                'pause': False,
                'upLimit': CONF.qbittorrent.upload_limit
            }
            requests.post(url, headers=headers, data=data)
