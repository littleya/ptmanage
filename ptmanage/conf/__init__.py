import sys

from oslo_config import cfg
from oslo_log import log as logging

from ptmanage import __version__
from ptmanage.conf import default
from ptmanage.conf.client import deluge
from ptmanage.conf.client import local
from ptmanage.conf.client import qbittorrent
from ptmanage.conf.client import remote
from ptmanage.conf.client import transmission
from ptmanage.conf.notification import telegram
from ptmanage.conf.site import opencd
from ptmanage.conf.site import u2

CONF = cfg.CONF
DOMAIN = 'ptmanage'

default.register_opts(CONF)

deluge.register_opts(CONF)
local.register_opts(CONF)
qbittorrent.register_opts(CONF)
remote.register_opts(CONF)
transmission.register_opts(CONF)

telegram.register_opts(CONF)

opencd.register_opts(CONF)
u2.register_opts(CONF)

logging.register_options(CONF)

CONF(sys.argv[1:],
     project='ptmanage',
     version=__version__)

logging.setup(CONF, DOMAIN)
