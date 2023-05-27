import io
import random

from src.Configuration.Configuration import AWS_REPORT
from src.Report.ReporterInterface import ReporterInterface
from src.Uploaders.AWSCommunicator import AWSCommunicator


class AWSReporter(ReporterInterface):
    def __init__(self):
        self.uploader = AWSCommunicator()
        self.index = random.randint(10000, 100000)

    def report(self, content: str):
        self.uploader.store(io.BytesIO(content.encode("utf-8")),
                            store_path=f"{AWS_REPORT}/{self.index}")
        self.index = self.index + 1
