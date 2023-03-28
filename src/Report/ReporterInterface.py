from abc import ABC


class ReporterInterface(ABC):
    def report(self, content: str):
        pass
