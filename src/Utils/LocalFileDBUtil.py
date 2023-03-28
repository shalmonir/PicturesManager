import os


class LocalFileDBUtil:
    @staticmethod
    def get_local_reporter_index(database_file):
        if os.path.isfile(database_file):
            with open(database_file, "rb") as report:
                try:
                    report.seek(-2, os.SEEK_END)
                    while report.read(1) != b'\n':
                        report.seek(-2, os.SEEK_CUR)
                except OSError:
                    report.seek(0)
                last_line = report.readline().decode()
                return int(last_line.split(" ")[0])
        return 0
