import itertools

from oslo_config import cfg

u2_group = cfg.OptGroup(
    'u2',
    title='U2 options',
    help='''
''')

u2_general_opts = [
    cfg.IntOpt(
        'uid',
        help='''
The user's id in U2.
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
'''),
    cfg.BoolOpt(
        'enable_auto_promote',
        default=True,
        help='''
Enable auto promote, if enabled, will auto set torrent's promote which
not fit user's promote policy.

If enabled, it required all filter conditions can be passed:

* upload_trigger
* download_trigger
''')
]

u2_filter_opts = [
    cfg.IntOpt(
        'promote',
        default=0,
        help='''
Download promote, 0 means no promote, 100 means 100% off.
The fetched torrent can be passed if the torrent's download promote is
large that the configuration.

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
Time during which the torrent was uploaded (in hours). The torrent which
upload time larger than the configration will be ignored.
This option can be ignored if the value is 0.

This is a policy for auto add torrent.
''')
]

u2_promote_opts = [
    cfg.IntOpt(
        'upload_ratio',
        default=233,
        help='''
Upload ratio to apply promote, minimum is 0, maximum is 233.
'''),
    cfg.IntOpt(
        'download_ratio',
        default=0,
        help='''
Download ratio ratio to apply promote, minimum is 0, maximum is 100.
'''),
    cfg.IntOpt(
        'upload_trigger',
        default=100,
        help='''
The trigger to apply promote, minimum is 0, maximum is 233. Need torrent's
current upload ratio is less than the configration.
'''),
    cfg.IntOpt(
        'download_trigger',
        default=30,
        help='''
The trigger to apply promote, minimum is 0, maximum is 100. Need torrent's
current download ratio is larger than the configration.
'''),
    cfg.IntOpt(
        'promote_time',
        default=24,
        help='''
The promote effect time in hours, minimum is 24.
''')
]

ALL_OPTS = list(itertools.chain(
    u2_general_opts,
    u2_filter_opts,
    u2_promote_opts
))


def register_opts(conf):
    conf.register_group(u2_group),
    conf.register_opts(ALL_OPTS, group=u2_group)


def list_opts():
    return {u2_group: ALL_OPTS}
