import io
import random

from src.Configuration.Configuration import AWS_REPORT
from src.Report.ReporterInterface import ReporterInterface
from src.Uploaders.AWSUploader import AWSUploader


class AWSReporter(ReporterInterface):
    def __init__(self):
        self.uploader = AWSUploader()
        self.index = random.randint(10000, 100000)

    def report(self, content: str):
        self.uploader.store_single_using_client(io.BytesIO(content.encode("utf-8")),
                                                store_path=f"{AWS_REPORT}/{self.index}")
        self.index += 1
