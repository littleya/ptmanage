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
    'cookie': CONF.opencd.cookie
}
TORRENT_LINK = 'https://open.cd/torrents.php'

RG_TORRENT_ID = re.compile('.*?(\\d+)', re.IGNORECASE | re.DOTALL)

PROMOTE_DOWNLOAD_MAPPING = {
    'pro_30pctdown': 30,
    'pro_50pctdown': 50,
    'pro_free': 0,
    'pro_free2up': 0,
    'pro_custom': 0,
    'pro_2up': 100,
    'pro_50pctdown2up': 50
}

PROMOTE_UPLOAD_MAPPING = {
    'pro_30pctdown': 100,
    'pro_50pctdown': 100,
    'pro_free': 100,
    'pro_free2up': 200,
    'pro_custom': 233,
    'pro_2up': 200,
    'pro_50pctdown2up': 200
}


NOTIFY_TORRENT_KEY = ['id', 'name', 'size', 'promote', 'promotetime', 'seeder',
                      'leecher', 'uploadtime']


class OpenCDSite(base.BaseSite):
    def __init__(self):
        super(OpenCDSite, self).__init__()

    def _get_torrent_page(self, link):
        page = requests.get(link, headers=HEADERS, timeout=CONF.opencd.timeout)
        return page.text

    def _get_torrent_webpage(self):
        page = self._get_torrent_page(TORRENT_LINK)
        html = etree.HTML(page)
        tr = html.xpath('//table[contains(@class, \'torrents\')]/tr')[1:]
        info = []
        for i in tr:
            # check the torrent is leeching or seeding
            if len(i.xpath('td[position()=3]//td//div'
                           '[contains(@class, \'progressarea\')]')):
                continue
            # get id
            trid = i.xpath('td[position()=3]/table/tr/td[position()=4]'
                           '/a/@href')[0]
            trid = re.findall('\\d+', trid)[0]
            # get type
            trtype = str(i.xpath('td[position()=1]/@title')[0])
            # get name
            trname = str(i.xpath('td[position()=3]/table/tr[position()=1]'
                                 '/td/a/@title')[0])
            # get magic
            trmagic = i.xpath('td[position()=3]/table/tr/td[position()=2]'
                              '/div/img/@class')
            if trmagic:
                trmagic = str(trmagic[0])
            else:
                trmagic = ''
            # get magictime
            trmagictime = i.xpath('td[position()=3]/table/tr/td[position()=2]'
                                  '/span/@title')
            if trmagictime:
                trmagictime = trmagictime[0]
                trmagictime = time.mktime(time.strptime(trmagictime,
                                                        '%Y-%m-%d %H:%M:%S'))
            else:
                trmagictime = None
            # get uploadtime
            truploadtime = i.xpath('td[position()=6]/span/@title')[0]
            truploadtime = time.mktime(time.strptime(truploadtime,
                                                     '%Y-%m-%d %H:%M:%S'))
            # get size
            trsize = i.xpath('td[position()=7]/text()')[0].split('\xa0')
            if 'T' in trsize[1]:
                trsize = float(trsize[0]) * 1024
            elif 'G' in trsize[1]:
                trsize = float(trsize[0])
            elif 'M' in trsize[1]:
                trsize = float(trsize[0]) / 1024
            # get seeder
            trseeder = i.xpath('td[position()=8]//text()')
            if trseeder:
                trseeder = int(trseeder[0])
            elif i.xpath('td[position()=8]//font/text()'):
                trseeder = int(i.xpath('td[position()=6]/b/a/font/text()')[0])
            else:
                trseeder = 0
            # get leecher
            trleecher = i.xpath('td[position()=9]//text()')
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

    def get_torrent_links(self):
        selected_torrents = OpenCDFilter(self._get_torrent_webpage()).filter()
        passkey = CONF.opencd.passkey
        torrent_links = {}
        msg = ''
        for t in selected_torrents:
            torrent_links[t.id] = 'https://open.cd/download.php?id=' + \
                                 str(t.id) + '&passkey=' + passkey
            LOG.debug('Add torrents: {}'.format(str(t.id)))

            # Notification
            for key in NOTIFY_TORRENT_KEY:
                msg += '{}: {}\n'.format(key, getattr(t, key, None))
            msg += '\n\n'
        if msg:
            msg = 'Add torrent from site: opencd\n' + msg
            utils.notify(msg)
        return torrent_links


class OpenCDFilter(base.BaseFilter):

    def __init__(self, unusing_torrents):
        super(OpenCDFilter, self).__init__()
        self.unusing_torrents = unusing_torrents

    def _filter_promote(self, t):
        torrent_promote = PROMOTE_DOWNLOAD_MAPPING.get(t.promote, 100)
        if torrent_promote > CONF.opencd.promote:
            LOG.debug('filter promtoe unpass: ' + str(t.id))
            return False
        return True

    def _filter_peer(self, t):
        if CONF.opencd.seeder != 0:
            if t.seeder > CONF.opencd.seeder:
                LOG.debug('filter seeder unpass: ' + str(t.id))
                return False
        if CONF.opencd.leecher != 0:
            if t.leecher < CONF.opencd.leecher:
                LOG.debug('filter leecher unpass: ' + str(t.id))
                return False
        if CONF.opencd.leecher_seeder_ratio != 0:
            if t.seeder != 0 and \
                    t.leecher/t.seeder < CONF.opencd.leecher_seeder_ratio:
                LOG.debug('filter dl/seed ratio unpass: ' + str(t.id))
                return False
        return True

    def _filter_size(self, t):
        if CONF.opencd.size != 0:
            if t.size > CONF.opencd.size:
                LOG.debug('filter size unpass: ' + str(t.id))
                return False
        return True

    def _filter_name(self, t):
        for name in CONF.opencd.name:
            if name in t.name:
                LOG.debug('filter name unpass: ' + str(t.id))
                return False
        return True

    def _filter_type(self, t):
        for typ in CONF.opencd.types:
            if typ in t.types:
                LOG.debug('filter type unpass: ' + str(t.id))
                return False
        return True

    def _filter_time(self, t):
        if CONF.opencd.uploaded_time != 0:
            delta = time.time() - t.uploadtime
            if delta > CONF.opencd.uploaded_time:
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
                torrents.append(t)
        return torrents


class PeriodicTask(base.BasePeriodicTask):

    @periodic_task.periodic_task(
        spacing=CONF.periodic_task_interval, run_immediately=True)
    def upload(self, ctx):
        if CONF.opencd.enable_auto_add:
            clients = utils.get_enabled_clients()
            for client in clients:
                client(OpenCDSite().get_torrent_links()).upload()
        else:
            LOG.info('opencd: Auto add disabled, skip it')
