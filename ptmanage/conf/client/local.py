from oslo_config import cfg

local_group = cfg.OptGroup(
    'local',
    title='local client',
    help='''
''')

local_opts = [
    cfg.StrOpt(
        'path',
        help='''
''')
]

ALL_OPTS = local_opts


def register_opts(conf):
    conf.register_group(local_group)
    conf.register_opts(ALL_OPTS, group=local_group)


def list_opts():
    return {local_group: ALL_OPTS}
