class DBConnectionMgr(object):
    def __new__(cls):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnectionMgr, cls).__new__(cls)
        return cls.instance

    def set_connection(self, connection):
        self.connection = connection

    def get_connection(self):
        return self.connection

    def set_session(self, session):
        self.session = session

    def get_session(self):
        return self.session
