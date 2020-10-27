""" Module for parser """
from src.file_system import FileSystem
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import pyautogui
import time

""" CONSTS """
DB_LIST = ['Bookshelf', 'MeSH', 'NLM Catalog', 'PubMed', 'PubMed Central', 'Gene', 'GEO DataSets',
           'GEO Profiles', 'HomoloGene', 'PopSet', 'Conserved Domains', 'Identical Protein Groups',
           'Protein', 'Protein Clusters', 'Sparcle', 'Structure', 'Assembly', 'BioCollections',
           'BioProject', 'BioSample', 'Genome', 'Nucleotide', 'SRA', 'Taxonomy', 'ClinicalTrials.gov',
           'ClinVar', 'dbGaP', 'dbSNP', 'dbVar', 'GTR', 'MedGen', 'OMIM', 'BioAssays',
           'Compounds', 'Pathways', 'Substances']
DB_NAME_LIST = ['books', 'mesh', 'nlmcatalog', 'pubmed', 'pmc', 'gene', 'gds', 'geoprofiles', 'homologene'
                'popset', 'cdd', 'ipg', 'protein', 'proteinclusters', 'sparcle', 'structure', 'assembly', 'biocollections',
                'bioproject', 'biosample', 'genome', 'nuccore', 'sra', 'taxonomy', 'clinicaltrials.gov', 'clinvar',
                'gap', 'snp', 'dbvar', 'gtr', 'medgen', 'omim', 'bioassay', 'compound', 'pathway', 'substance']
DB_CATEGORIES_LIST = ['Literature', 'Genes', 'Proteins', 'Genomes', 'Clinical', 'PubChem']


class Parser:
    """ Class for parser """

    @staticmethod
    def get_request(request: str):
        """ Get request and save documents """
        request = request.strip()
        FileSystem.create_parser_folder()
        FileSystem.create_folder('request', request)
        FileSystem.create_categoies_folders(request, DB_CATEGORIES_LIST)
        Parser.__get_files(request)

    @staticmethod
    def __get_files(request):
        Parser.__books(request)

    @staticmethod
    def __replace_elem_in_request(request):
        request = request.replace(' ', '%20')
        request = request.replace('[', '%5B')
        request = request.replace(']', '%5D')
        request = request.replace('(', '%28')
        request = request.replace(')', '%29')
        return request

    @staticmethod
    def __replace_elem_for_windows(string):
        string = string.replace(':', '')
        string = string.replace(';', '')
        string = string.replace(',', '')
        string = string.replace('.', '')
        string = string.replace('|', '')
        string = string.replace('/', '')
        return string

    @staticmethod
    def __books(request):
        FileSystem.create_folder('Literature', request)
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/books/?term={request}').content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        books_list = []
        if not soup.find(id="Details"):
            driver = webdriver.Chrome(executable_path=FileSystem.get_driver())
            driver.get(url=f'https://www.ncbi.nlm.nih.gov/books/?term={request}')
            content_list.append(driver.page_source)
            next = driver.find_element_by_class_name('next')
            while 'inactive' not in next.get_attribute('class'):
                next.click()
                content_list.append(driver.page_source)
                next = driver.find_element_by_class_name('next')
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    books_list.append(titles_list[j].a['href'])
            for i in range(0, len(books_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{books_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                titles = driver.find_elements_by_class_name('title')
                title_book = soup.findAll(True, {"class": "rsltcont"})[0].p.decode_contents()
                title_book = ''.join(title_book.split(' ')[0:4])
                title_book = Parser.__replace_elem_for_windows(title_book)
                if not FileSystem.is_exist(f'{title_book}', f'{FileSystem.get_directory()}data_parser\\'
                                                       f'{string_request}\\Literature\\Books\\'):
                    os.mkdir(f'{FileSystem.get_directory()}data_parser\\'
                             f'{string_request}\\Literature\\Books\\{title_book}')
                for j in range(1, len(titles)):
                    titles = driver.find_elements_by_class_name('title')
                    title_part = titles[j].text
                    title_part = ' '.join(title_part.split(' ')[0:5])
                    title_part = Parser.__replace_elem_for_windows(title_part)
                    titles[j].find_element_by_tag_name('a').click()
                    if not FileSystem.is_exist(f'{title_part}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\Books\\{title_book}\\'):
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(1)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Literature\\Books\\{title_book}\\{title_part}.html')
                        time.sleep(1)
                        pyautogui.hotkey('enter')
                        time.sleep(1)
                    driver.back()
                    time.sleep(1)