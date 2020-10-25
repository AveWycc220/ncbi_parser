""" Module for working with Windows File System """
import os

""" CONSTS """
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class FileSystem:
    """ Class for working with Windows File System """
    @staticmethod
    def create_parser_folder():
        """ If parser folder doesnt exist create new """
        if 'data_parser' not in os.listdir(path=f'{THIS_FOLDER}\\..\\'):
            os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser')

    @staticmethod
    def create_folder(type: str, request=None):
        """ Create folders depending on types """
        if type == 'request':
            if f'{request}' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}')

    @staticmethod
    def create_categoies_folders(request, categories):
        """ Create Categories Folders"""
        for elem in categories:
            os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{elem}')
