from oslo_config import cfg

default_options = [
    cfg.ListOpt(
        'enabled_sites',
        default=[],
        help='''
Enabled sites, site will be check torrents periodic and add torrent by using
clients.
'''),
    cfg.ListOpt(
        'enabled_clients',
        default=[],
        help='''
Enabled clients, the clients used to upload torrent files.
'''),
    cfg.ListOpt(
        'enabled_notify_clients',
        default=[],
        help='''
Enabled notify clients, the notify client used to notify add/promote torrents.
'''),
    cfg.IntOpt(
        'periodic_task_interval',
        default=60,
        help='''
Time to periodic run site's check task. (In seconds)
'''),
    cfg.IntOpt(
        'periodic_online_notify_interval',
        default=3600,
        help='''
Time to periodic notify ptmanage is online. (In seconds)
'''),
    cfg.StrOpt(
        'online_notify_msg',
        default='Pt Manage is online :)',
        help='''
Online notify msg.
''')
]


def register_opts(conf):
    conf.register_opts(default_options)


def list_opts():
    return {'DEFAULT': default_options}
