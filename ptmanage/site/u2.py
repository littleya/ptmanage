import re
import time

from lxml import etree
from oslo_log import log as logging
from oslo_service import periodic_task
import requests

from ptmanage.common import utils
from ptmanage.conf import CONF
from ptmanage.objects import torrent
from ptmanage.site import base


LOG = logging.getLogger(__name__)

HEADERS = {
    'dnt': '1',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,image/apng,*/*;q=0.8',
    'cache-control': 'max-age=0',
    'authority': 'u2.dmhy.org',
    'cookie': CONF.u2.cookie
}
DOWNLOADING_LINK = 'https://u2.dmhy.org/getusertorrentlistajax.php?' + \
                   'userid={}&type=seeding'.format(str(CONF.u2.uid))
SEEDING_LINK = 'https://u2.dmhy.org/getusertorrentlistajax.php?' + \
               'userid={}&type=leeching'.format(str(CONF.u2.uid))
TORRENT_LINK = 'https://u2.dmhy.org/torrents.php'

RG_TORRENT_ID = re.compile('.*?(\\d+)', re.IGNORECASE | re.DOTALL)

PROMOTE_MAPPING = {
    'pro_30pctdown': 30,
    'pro_50pctdown': 50,
    'pro_free': 100,
    'pro_free2up': 100,
    'pro_custom': 100
}


class U2Site(base.BaseSite):
    def __init__(self):
        super(U2Site, self).__init__()

    def _get_torrent_page(self, link):
        page = requests.get(link, headers=HEADERS, timeout=CONF.u2.timeout)
        return page.text

    def _get_torrent_webpage(self):
        page = self._get_torrent_page(TORRENT_LINK)
        html = etree.HTML(page)
        tr = html.xpath('//table[contains(@class, \'torrents\')]/tr')[1:]
        info = []
        for i in tr:
            # check leeching or seeding
            if len(i.xpath('td[contains(@class, \'leechhlc_current\')]')):
                continue
            if len(i.xpath('td[contains(@class, \'seedhlc_current\')]')):
                continue
            # get id
            trid = i.xpath('td[position()=2]/table/tr/td[position()=2]'
                           '/a/@href')[0]
            trid = re.findall('\\d+', trid)[0]
            # get type
            trtype = str(i.xpath('td[position()=1]/a/text()')[0])
            # get name
            trname = str(i.xpath('td[position()=2]/table/tr[position()=1]'
                                 '/td/a/text()')[0])
            # get magic
            trmagic = i.xpath('td[position()=2]/table/tr[position()=2]'
                              '/td/img/@class')
            if trmagic:
                trmagic = str(trmagic[0])
            else:
                trmagic = ''
            # get magictime
            trmagictime = i.xpath('td[position()=2]/table/tr[position()=2]'
                                  '/td/b/time/@title')
            if trmagictime:
                trmagictime = trmagictime[0]
                trmagictime = time.mktime(time.strptime(trmagictime,
                                                        '%Y-%m-%d %H:%M:%S'))
            else:
                trmagictime = None
            # get uploadtime
            truploadtime = i.xpath('td[position()=4]/time/@title')[0]
            truploadtime = time.mktime(time.strptime(truploadtime,
                                                     '%Y-%m-%d %H:%M:%S'))
            # get size
            trsize = i.xpath('td[position()=5]/text()')
            if 'T' in trsize[1]:
                trsize = float(trsize[0]) * 1024
            elif 'G' in trsize[1]:
                trsize = float(trsize[0])
            elif 'M' in trsize[1]:
                trsize = float(trsize[0]) / 1024
            # get seeder
            trseeder = i.xpath('td[position()=6]/b/a/text()')
            if trseeder:
                trseeder = int(trseeder[0])
            elif i.xpath('td[position()=6]/b/a/font/text()'):
                trseeder = int(i.xpath('td[position()=6]/b/a/font/text()')[0])
            else:
                trseeder = 0
            # get leecher
            trleecher = i.xpath('td[position()=7]/b/a/text()')
            if trleecher:
                trleecher = int(trleecher[0])
            else:
                trleecher = 0
            kwargs = {
                'id': int(trid),
                'types': trtype,
                'name': trname,
                'promote': trmagic,
                'promotetime': trmagictime,
                'uploadtime': truploadtime,
                'size': trsize,
                'seeder': trseeder,
                'leecher': trleecher}
            info.append(torrent.Torrent(**kwargs))
            LOG.debug('Get torrent: ' + str(trid))
        return info

    # def _get_torrent_downloading(self):
    #     page = self._get_torrent_page(DOWNLOADING_LINK)
    #     return self._resolv_torrent_from_user_details(page)

    # def _get_torrent_seeding(self):
    #     page = self._get_torrent_page(SEEDING_LINK)
    #     return self._resolv_torrent_from_user_details(page)

    # def _resolv_torrent_from_user_details(self, page):
    #     html = etree.HTML(page)
    #     hrefs = html.xpath('//table[contains(@class, 'torrentname')]'
    #                        '/tr/td/a/@href')
    #     torrent_list = []
    #     for href in hrefs:
    #         res = RG_TORRENT_ID.search(href)
    #         if res:
    #             torrent_list.append(int(res.group(1)))
    #     return torrent_list

    def get_torrent_links(self):
        selected_torrents = U2Filter(self._get_torrent_webpage()).filter()
        passkey = CONF.u2.passkey
        torrent_links = {}
        for tid in selected_torrents:
            torrent_links[tid] = 'https://u2.dmhy.org/download.php?id=' + \
                                 str(tid) + '&passkey=' + passkey + '&http=1'
            LOG.debug('Add torrents: {}'.format(str(tid)))
        return torrent_links


class U2Filter(base.BaseFilter):

    def __init__(self, unusing_torrents):
        super(U2Filter, self).__init__()
        self.unusing_torrents = unusing_torrents

    def _filter_promote(self, t):
        torrent_promtoe = PROMOTE_MAPPING.get(t.promote, 0)
        if torrent_promtoe < CONF.u2.promote:
            LOG.debug('filter promtoe unpass: ' + str(t.id))
            return False
        return True

    def _filter_peer(self, t):
        if CONF.u2.seeder != 0:
            if t.seeder >= CONF.u2.seeder:
                LOG.debug('filter seeder unpass: ' + str(t.id))
                return False
        if CONF.u2.leecher != 0:
            if t.leecher <= CONF.u2.leecher:
                LOG.debug('filter leecher unpass: ' + str(t.id))
                return False
        if CONF.u2.leecher_seeder_ratio != 0:
            if t.seeder != 0 and \
                    t.leecher/t.seeder <= CONF.u2.leecher_seeder_ratio:
                LOG.debug('filter dl/seed ratio unpass: ' + str(t.id))
                return False
        return True

    def _filter_size(self, t):
        if CONF.u2.size != 0:
            if t.size >= CONF.u2.size:
                LOG.debug('filter size unpass: ' + str(t.id))
                return False
        return True

    def _filter_name(self, t):
        for name in CONF.u2.name:
            if name in t.name:
                LOG.debug('filter name unpass: ' + str(t.id))
                return False
        return True

    def _filter_type(self, t):
        for typ in CONF.u2.types:
            if typ in t.types:
                LOG.debug('filter type unpass: ' + str(t.id))
                return False
        return True

    def _filter_time(self, t):
        if CONF.u2.uploaded_time != 0:
            delta = time.time() - t.uploadtime
            if delta > CONF.u2.uploaded_time * 60:
                LOG.debug('filter time unpass: ' + str(t.id))
                return False
        return True

    def filter(self):
        torrents = []
        for t in self.unusing_torrents:
            if self._filter_promote(t) and \
               self._filter_peer(t) and \
               self._filter_size(t) and \
               self._filter_name(t) and \
               self._filter_type(t) and \
               self._filter_time(t):
                torrents.append(t.id)
        return torrents


class PeriodicTask(base.BasePeriodicTask):

    @periodic_task.periodic_task(spacing=CONF.periodic_task_interval)
    def upload(self, ctx):
        clients = utils.get_enabled_clients()
        for client in clients:
            client(U2Site().get_torrent_links()).upload()
