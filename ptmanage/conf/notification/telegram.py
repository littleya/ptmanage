from oslo_config import cfg


telegram_group = cfg.OptGroup(
    'telegram',
    title='telegram',
    help='''
''')

telegram_opts = [
    cfg.StrOpt(
        'token',
        help='''
Telegram bot token.
'''),
    cfg.StrOpt(
        'chat_id',
        help='''
Telegram chat id. Can be channel or user.
''')
]

ALL_OPTS = telegram_opts


def register_opts(conf):
    conf.register_group(telegram_group)
    conf.register_opts(ALL_OPTS, group=telegram_group)


def list_opts():
    return {telegram_group: ALL_OPTS}
