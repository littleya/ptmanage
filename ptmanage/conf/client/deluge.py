from oslo_config import cfg


deluge_group = cfg.OptGroup(
    'deluge',
    title='deluge RPC client',
    help='''
''')


deluge_opts = [
    cfg.StrOpt(
        'host',
        help='''
Deluge server's host, can be IP address or domain name or hostname
'''),
    cfg.IntOpt(
        'port',
        default=58846,
        help='''
Deluge server's rpc port
'''),
    cfg.StrOpt(
        'username',
        help='''
Deluge server's username to loggin.
'''),
    cfg.StrOpt(
        'password',
        help='''
Deluge server's password to loggin.
'''),
    cfg.StrOpt(
        'base_location',
        help='''
The path to store files.
''')
]


ALL_OPTS = deluge_opts


def register_opts(conf):
    conf.register_group(deluge_group)
    conf.register_opts(ALL_OPTS, group=deluge_group)


def list_opts():
    return {deluge_group: ALL_OPTS}
