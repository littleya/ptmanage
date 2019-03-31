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
'''),
    cfg.StrOpt(
        'passkey',
        default='',
        help='''
'''),
    cfg.StrOpt(
        'cookie',
        default='',
        help='''
'''),
    cfg.IntOpt(
        'timeout',
        default=15,
        help='''
''')
]

u2_filter_opts = [
    cfg.IntOpt(
        'promote',
        default=30,
        help='''
'''),
    cfg.IntOpt(
        'leecher',
        default=5,
        help='''
'''),
    cfg.IntOpt(
        'seeder',
        default=3,
        help='''
'''),
    cfg.IntOpt(
        'leecher_seeder_ratio',
        default=1,
        help='''
'''),
    cfg.ListOpt(
        'name',
        default=[],
        help='''
'''),
    cfg.ListOpt(
        'types',
        default=[],
        help='''
'''),
    cfg.IntOpt(
        'size',
        default=0,
        help='''
'''),
    cfg.IntOpt(
        'uploaded_time',
        default=0,
        help='''
''')
]

ALL_OPTS = list(itertools.chain(
    u2_general_opts,
    u2_filter_opts
))


def register_opts(conf):
    conf.register_group(u2_group),
    conf.register_opts(ALL_OPTS, group=u2_group)


def list_opts():
    return {u2_group: ALL_OPTS}
