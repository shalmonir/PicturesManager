from abc import ABC, abstractmethod


class DBInterface(ABC):
    @abstractmethod
    def store(self, entity):
        pass

    @abstractmethod
    def get_user_albums(self, user_id: int):
        pass

    @abstractmethod
    def search_user_albums(self, user_id: int, keyword: str):
        pass

    @abstractmethod
    def get_album(self, user_id: int):
        pass

    @abstractmethod
    def get_album_pictures(self, album_id: int):
        pass

    @abstractmethod
    def get_user_by_name(self, username: str):
        pass

    @abstractmethod
    def fetch_album(self, album_name: str, user_id: int):
        pass
