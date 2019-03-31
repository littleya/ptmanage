from oslo_log import log as logging
from oslo_service import service
from oslo_service import threadgroup

from ptmanage.common import utils
from ptmanage.conf import CONF


LOG = logging.getLogger(__name__)


class PeriodicService(service.ServiceBase):
    def __init__(self):
        super(PeriodicService, self).__init__()
        self.tgs = []

    def setup(self, pt_class, name, conf):
        pt = pt_class(conf, name)
        pool_size = 1
        tg = threadgroup.ThreadGroup(pool_size)
        tg.add_dynamic_timer(
            pt.run_periodic_tasks,
            periodic_interval_max=1,
            context=None)
        return tg

    def start(self):
        LOG.info('launching periodic task service')
        sites = utils.get_enabled_sites()
        self.tgs = [self.setup(sites.get(site), site, CONF) for site in sites]

    def wait(self):
        pass

    def stop(self):
        LOG.info('stopping periodic task service')
        for tg in self.tgs:
            tg.stop()

    def reset(self):
        self.stop()
        self.start()
