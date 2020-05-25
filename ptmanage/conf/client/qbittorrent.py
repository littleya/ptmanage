from oslo_config import cfg


qbittorrent_group = cfg.OptGroup(
    'qbittorrent',
    title='qBittorrent configuration',
    help='''
''')


qbittorrent_opts = [
    cfg.StrOpt(
        'host',
        help='''
qbittorrent webui host, can be IP address or domain name or hostname
'''),
    cfg.IntOpt(
        'port',
        default=8080,
        help='''
qbittorrent webui port
'''),
    cfg.StrOpt(
        'username',
        help='''
qbittorrent webui username to loggin.
'''),
    cfg.StrOpt(
        'password',
        help='''
qbittorrent webui password to loggin.
'''),
    cfg.StrOpt(
        'base_location',
        help='''
The path to store files.
'''),
    cfg.IntOpt(
        'upload_limit',
        default=50000000,
        help='''
The upload limit(in bytes/s)
'''
    )
]


ALL_OPTS = qbittorrent_opts


def register_opts(conf):
    conf.register_group(qbittorrent_group)
    conf.register_opts(ALL_OPTS, group=qbittorrent_group)


def list_opts():
    return {qbittorrent_group: ALL_OPTS}
