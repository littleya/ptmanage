from oslo_log import log as logging
from telegram.ext import Updater

from ptmanage.conf import CONF
from ptmanage.notification import base


TELEGRAM_CLIENT = None
LOG = logging.getLogger(__name__)


class NotifyClient(base.BaseNotifyClient):

    def notify(self, msg):
        global TELEGRAM_CLIENT
        if not TELEGRAM_CLIENT:
            TELEGRAM_CLIENT = Updater(
                token=CONF.telegram.token,
                use_context=True)
        TELEGRAM_CLIENT.bot.send_message(CONF.telegram.chat_id, msg)
