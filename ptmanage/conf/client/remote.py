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
Remote hostname, can be IP address or domain name or hostname.
'''),
    cfg.IntOpt(
        'port',
        default=22,
        help='''
Remote sshd port.
'''),
    cfg.StrOpt(
        'username',
        help='''
SSH username to loggin.
'''),
    cfg.StrOpt(
        'password',
        help='''
SSH password to loggin.
'''),
    cfg.StrOpt(
        'path',
        help='''
Remote path to store torrent files.
''')
]

ALL_OPTS = remote_opts


def register_opts(conf):
    conf.register_group(remote_group)
    conf.register_opts(ALL_OPTS, group=remote_group)


def list_opts():
    return {remote_group: ALL_OPTS}
