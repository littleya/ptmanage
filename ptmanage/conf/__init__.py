import sys

from oslo_config import cfg
from oslo_log import log as logging

from ptmanage import __version__
from ptmanage.conf import default
from ptmanage.conf.client import local
from ptmanage.conf.client import remote
from ptmanage.conf.notification import telegram
from ptmanage.conf.site import u2

CONF = cfg.CONF
DOMAIN = 'ptmanage'

default.register_opts(CONF)

local.register_opts(CONF)
remote.register_opts(CONF)

telegram.register_opts(CONF)

u2.register_opts(CONF)

logging.register_options(CONF)

CONF(sys.argv[1:],
     project='ptmanage',
     version=__version__)

logging.setup(CONF, DOMAIN)
