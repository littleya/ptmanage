import sys

from oslo_log import log as logging
from oslo_service import service

from ptmanage import __authors__
from ptmanage import __version__
from ptmanage.conf import CONF
from ptmanage.manage import PeriodicService

LOG = logging.getLogger(__name__)

THREAD_LAUNCHER = None

info = r'''
       _
 _ __ | |_ _ __ ___   __ _ _ __   __ _  __ _  ___
| '_ \| __| '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \
| |_) | |_| | | | | | (_| | | | | (_| | (_| |  __/
| .__/ \__|_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|
|_|                                    |___/

                                       version: {}
                                       authors: {}
'''.format(__version__, __authors__)


def print_server_info():
    print(info)


def thread_launch(server):
    try:
        global THREAD_LAUNCHER

        if THREAD_LAUNCHER is None:
            THREAD_LAUNCHER = service.ServiceLauncher(CONF)

        THREAD_LAUNCHER.launch_service(server)
    except Exception as exc:
        LOG.error(exc)
        sys.exit(1)


def launch_all():
    global THREAD_LAUNCHER
    thread_launch(PeriodicService())
    THREAD_LAUNCHER.wait()


def main():
    print_server_info()
    launch_all()


if __name__ == '__main__':
    sys.exit(main())
