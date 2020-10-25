""" Module for parser """
from src.file_system import FileSystem


class Parser:
    """ Class for parser """
    request = None

    def __init__(self, request: str):
        self.request = request
        self.__create_request_folder()

    def __create_request_folder(self):
        FileSystem.create_folder('request', self.request)
