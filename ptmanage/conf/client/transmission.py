from oslo_config import cfg


transmission_group = cfg.OptGroup(
    'transmission',
    title='transmission RPC client',
    help='''
''')


transmission_opts = [
    cfg.StrOpt(
        'host',
        help='''
Transmission server's host, can be IP address or domain name or hostname
'''),
    cfg.IntOpt(
        'port',
        default=9091,
        help='''
Transmission server's rpc port
'''),
    cfg.StrOpt(
        'username',
        default='',
        help='''
Transmission server's username to loggin.
'''),
    cfg.StrOpt(
        'password',
        default='',
        help='''
Transmission server's password to loggin.
'''),
    cfg.StrOpt(
        'base_location',
        help='''
The path to store files.
''')
]


ALL_OPTS = transmission_opts


def register_opts(conf):
    conf.register_group(transmission_group)
    conf.register_opts(ALL_OPTS, group=transmission_group)


def list_opts():
    return {transmission_group: ALL_OPTS}
