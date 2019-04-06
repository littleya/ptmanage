from oslo_service import periodic_task


class BaseSite(object):
    def __init__(self):
        pass

    def get_torrent_links(self):
        return {}


class BaseFilter(object):
    def __init__(self):
        pass

    def filter(self):
        pass


class BasePromote(object):
    def __init__(self):
        pass

    def promote(self):
        pass


class BasePeriodicTask(periodic_task.PeriodicTasks):
    def __init__(self, conf, name):
        super(BasePeriodicTask, self).__init__(conf)
        self.name = name
