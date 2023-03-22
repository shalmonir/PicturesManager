from src.Context.ContextMgr import Context
from src.DB.LocalFileDBUtility import LocalFileDBUtility
from src.Report.LocalReporter import LocalReporter
from src.Uploaders.LocalUploader import LocalUploader


class LocalContextMgr(Context):
    def __init__(self):
        self.uploader = LocalUploader()
        self.db_utility = LocalFileDBUtility()
        self.reporter = LocalReporter()
