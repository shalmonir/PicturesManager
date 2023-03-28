import os
from datetime import datetime
from typing import List

from src.Configuration.Configuration import PATH_TO_LOCAL_REPORT
from src.Report.ReporterInterface import ReporterInterface


class LocalReporter(ReporterInterface):
    @staticmethod
    def get_local_reporter_index():
        if os.path.isfile(PATH_TO_LOCAL_REPORT):
            with open(PATH_TO_LOCAL_REPORT, "rb") as report:
                try:
                    report.seek(-2, os.SEEK_END)
                    while report.read(1) != b'\n':
                        report.seek(-2, os.SEEK_CUR)
                except OSError:
                    report.seek(0)
                last_line = report.readline().decode()
                return int(last_line.split(" ")[0])
        return 0

    def __init__(self):
        self.index = LocalReporter.get_local_reporter_index()

    def report(self, files_succeed: List[str], files_failed: List[str]):
        with open(PATH_TO_LOCAL_REPORT, "a+") as report:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.index = self.index + 1
            report.write(f"{self.index} {time} | upload report: success: {files_succeed}, failed: {files_failed}")
