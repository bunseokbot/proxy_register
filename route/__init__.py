class Route(object):
    def __init__(self, ip, domain):
        self.ip = ip
        self.domain = domain

    def __str__(self):
        return self.domain

    def query(self):
        """ search domain routing info """
        pass

    def register(self):
        """ register domain nginx reverse proxy """
        pass

    def __del__(self):
        del self
