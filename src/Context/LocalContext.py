from src.Context.Context import Context
from src.Report.LocalReporter import LocalReporter
from src.Uploaders.LocalCommunicator import LocalCommunicator
from src.DB.DBUtil import DBUtil


class LocalContext(Context):
    def __init__(self):
        self.uploader = LocalCommunicator()
        self.db_utility = DBUtil()
        self.reporter = LocalReporter()
