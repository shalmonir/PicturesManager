from src.Context.ContextMgr import Context
from src.Report.LocalReporter import LocalReporter
from src.Uploaders.LocalUploader import LocalUploader
from src.DB.DBUtil import DBUtil


class LocalContextMgr(Context):
    def __init__(self):
        self.uploader = LocalUploader()
        self.db_utility = DBUtil()
        self.reporter = LocalReporter()
