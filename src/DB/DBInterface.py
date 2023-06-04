from abc import ABC, abstractmethod


class DBInterface(ABC):
    @abstractmethod
    def store(self, entity):
        pass

    @abstractmethod
    def get_albums_by_user(self, user_id: int):
        pass

    @abstractmethod
    def search_user_albums(self, user_id: int, keyword: str):
        pass

    @abstractmethod
    def get_album_by_user(self, user_id: int):
        pass

    @abstractmethod
    def get_pictures_by_album(self, album_id: int):
        pass

    @abstractmethod
    def get_user_by_name(self, username: str):
        pass

    @abstractmethod
    def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    def obtain_album(self, album_name: str, user_id: int):
        pass
