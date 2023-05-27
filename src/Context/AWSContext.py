from src.Context.Context import Context
from src.DB.DBUtil import DBUtil
from src.Report.AWSReporter import AWSReporter
from src.Uploaders.AWSCommunicator import AWSCommunicator


class AWSContext(Context):
    def __init__(self):
        self.uploader = AWSCommunicator()
        self.db_utility = DBUtil()
        self.reporter = AWSReporter()

