from abc import ABC, abstractmethod


class APIExport:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_values(self, response_json):
        pass

    @abstractmethod
    def log_status_code(self, status_code):
        pass