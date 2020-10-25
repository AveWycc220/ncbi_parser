""" Module for working with Windows File System """
import os

""" CONSTS """
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class FileSystem:
    """ Class for working with Windows File System """
    @staticmethod
    def create_parser_folder():
        if 'data_parser' not in os.listdir(path=f'{THIS_FOLDER}\\..\\'):
            os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser')

    @staticmethod
    def create_folder(type: str, request=None):
        if type == 'request':
            if f'{request}' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}')
