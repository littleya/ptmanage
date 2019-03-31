from oslo_config import cfg

remote_group = cfg.OptGroup(
    'remote',
    title='remote ssh client',
    help='''
''')

remote_opts = [
    cfg.StrOpt(
        'host',
        help='''
'''),
    cfg.IntOpt(
        'port',
        default=22,
        help='''
'''),
    cfg.StrOpt(
        'username',
        help='''
'''),
    cfg.StrOpt(
        'password',
        help='''

'''),
    cfg.StrOpt(
        'path',
        help='''
''')
]

ALL_OPTS = remote_opts


def register_opts(conf):
    conf.register_group(remote_group)
    conf.register_opts(ALL_OPTS, group=remote_group)


def list_opts():
    return {remote_group: ALL_OPTS}
