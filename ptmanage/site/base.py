from oslo_log import log as logging
from oslo_service import periodic_task

from ptmanage.common import utils
from ptmanage.conf import CONF


LOG = logging.getLogger(__name__)


class BaseSite(object):
    def __init__(self):
        pass

    def get_torrent_links(self):
        return {}


class BaseFilter(object):
    def __init__(self):
        pass

    def filter(self):
        pass


class BasePromote(object):
    def __init__(self):
        pass

    def promote(self):
        pass


class BasePeriodicTask(periodic_task.PeriodicTasks):
    def __init__(self, conf, name):
        super(BasePeriodicTask, self).__init__(conf)
        self.name = name

    @periodic_task.periodic_task(spacing=CONF.periodic_online_notify_interval)
    def notify_online(self, ctx):
        utils.notify(CONF.online_notify_msg)
