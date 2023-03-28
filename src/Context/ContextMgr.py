from src.DB.DBInterface import DBInterface
from src.Report.ReporterInterface import ReporterInterface
from src.Uploaders.UploaderInterface import UploaderInterface


class Context:
    def __init__(self):
        self.uploader = None
        self.db_utility = None
        self.reporter = None

    def get_uploader(self) -> UploaderInterface:
        return self.uploader

    def get_db_utility(self) -> DBInterface:
        return self.db_utility

    def get_reporter(self) -> ReporterInterface:
        return self.reporter
