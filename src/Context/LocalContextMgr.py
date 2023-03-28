from src.Context.ContextMgr import Context
from src.DB.LocalFileDB import LocalFileDB
from src.Report.LocalReporter import LocalReporter
from src.Uploaders.LocalUploader import LocalUploader


class LocalContextMgr(Context):
    def __init__(self):
        self.uploader = LocalUploader()
        self.db_utility = LocalFileDB()
        self.reporter = LocalReporter()
