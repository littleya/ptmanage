import itertools

from oslo_config import cfg

opencd_group = cfg.OptGroup(
    'opencd',
    title='opencd options',
    help='''
''')

opencd_general_opts = [
    cfg.IntOpt(
        'uid',
        help='''
The user's id in opencd.
'''),
    cfg.StrOpt(
        'passkey',
        default='',
        help='''
Passkey to download torrent files.
'''),
    cfg.StrOpt(
        'cookie',
        default='',
        help='''
Cookie to login to fetch torrent status.
'''),
    cfg.IntOpt(
        'timeout',
        default=15,
        help='''
Timeout for fetch torrent status.
'''),
    cfg.BoolOpt(
        'enable_auto_add',
        default=True,
        help='''
Enable auto add, if enabled, will use configured client to upload torrent
files.

If enabled, it required all filter conditions can be passed:

* promote
* leecher
* seeder
* leecher_seeder_ratio
* name
* types
* size
* uploaded_time
''')
]

opencd_filter_opts = [
    cfg.IntOpt(
        'promote',
        default=0,
        help='''
Download promote, 0 means 100% off, 100 means no promote.
The fetched torrent can be passed if the torrent's download promote is
less than/equal to the configuration.

This is a policy for auto add torrent.
'''),
    cfg.IntOpt(
        'leecher',
        default=0,
        help='''
The downloader count of fetched torrent.
The fetched torrent can be passed if the torrent's downloader count is
large that the configuration.
This condition can be ignored if the value is 0.

This is a policy for auto add torrent.
'''),
    cfg.IntOpt(
        'seeder',
        default=1,
        help='''
The uploader count of fetched torrent.
The fetched torrent can be passed if the torrent's uploader count is
less than the configuration.
This condition can be ignored if the value is 0.

This is a policy for auto add torrent.
'''),
    cfg.IntOpt(
        'leecher_seeder_ratio',
        default=0,
        help='''
The leecher/seeder ratio of fetched torrent.
The fetched torrent can be passed if the torrent's leecher/seeder ratio is
large than the configuration.
This condition can be ignored if the value is 0.

This is a policy for auto add torrent.
'''),
    cfg.ListOpt(
        'name',
        default=[],
        help='''
A list of excluded name.
The torrent which name fit the configration will be ignored.
Not support regular expression.

This is a policy for auto add torrent.
'''),
    cfg.ListOpt(
        'types',
        default=[],
        help='''
A list of excluded types.
The torrent which type fit the configration will be ignored.
Not support regular expression.

This is a policy for auto add torrent.
'''),
    cfg.IntOpt(
        'size',
        default=0,
        help='''
Size limit. The torrent which size larger than the configration will be
ignored.
This option can be ignored if the value is 0.

This is a policy for auto add torrent.
'''),
    cfg.IntOpt(
        'uploaded_time',
        default=0,
        help='''
Time during which the torrent was uploaded (in seconds). The torrent which
upload time larger than the configration will be ignored.
This option can be ignored if the value is 0.

This is a policy for auto add torrent.
''')
]


ALL_OPTS = list(itertools.chain(
    opencd_general_opts,
    opencd_filter_opts,
))


def register_opts(conf):
    conf.register_group(opencd_group),
    conf.register_opts(ALL_OPTS, group=opencd_group)


def list_opts():
    return {opencd_group: ALL_OPTS}
