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
            if f'{request.lower()}' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request.lower()}')
        if type == 'Literature':
            if 'Books' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\Books')
            if 'MeSH' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\MeSH')
            if 'NLM Catalog' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\d'
                              f'ata_parser\\{request}\\{type}\\NLM Catalog')
            if 'PubMed' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\PubMed')
            if 'PubMed Central' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\PubMed Central')
        if type == 'Genes':
            if 'Gene' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\Gene')
            if 'GEO DataSets' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\GEO DataSets')
            if 'GEO Profiles' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\GEO Profiles')
            if 'Homologene' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\Homologene')
            if 'PopSet' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\') and request:
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{type}\\PopSet')

    @staticmethod
    def create_categoies_folders(request, categories):
        """ Create Categories Folders"""
        for elem in categories:
            if f'{elem}' not in os.listdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\'):
                os.mkdir(path=f'{THIS_FOLDER}\\..\\data_parser\\{request}\\{elem}')

    @staticmethod
    def get_driver():
        """ Get Path of WebDriver Chome 86"""
        return f'{THIS_FOLDER}\\..\\chromedriver.exe'

    @staticmethod
    def get_directory():
        return f'{THIS_FOLDER}\\..\\'

    @staticmethod
    def is_exist(elem, directory):
        return elem in os.listdir(path=directory)
