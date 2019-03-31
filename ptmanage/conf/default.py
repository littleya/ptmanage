from oslo_config import cfg

default_options = [
    cfg.ListOpt(
        'enabled_sites',
        default=[],
        help='''
'''),
    cfg.ListOpt(
        'enabled_clients',
        default=[],
        help='''
'''),
    cfg.IntOpt(
        'periodic_task_interval',
        default=60,
        help='''
''')
]


def register_opts(conf):
    conf.register_opts(default_options)


def list_opts():
    return {'DEFAULT': default_options}
