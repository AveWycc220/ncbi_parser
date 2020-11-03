""" Module for parser """
from src.file_system import FileSystem
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import pyautogui
import time
from selenium.common.exceptions import NoSuchElementException,  WebDriverException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
TIME_SLEEP = 1


class Parser:
    """ Class for parser """

    @staticmethod
    def get_request(request: str, catalog: str):
        """ Get request and save documents """
        request = request.strip()
        FileSystem.create_parser_folder()
        FileSystem.create_folder('request', request)
        FileSystem.create_categoies_folders(request, DB_CATEGORIES_LIST)
        Parser.__get_files(request, catalog)

    @staticmethod
    def __get_files(request, catalog):
        FileSystem.create_folder('Literature', request)
        FileSystem.create_folder('Genes', request)
        if catalog == '1':
            Parser.__books(request)
            Parser.__mesh(request)
            Parser.__nlmcatalog(request)
            Parser.__pubmed(request)
            Parser.__pmc(request)
        elif catalog == '1.1':
            Parser.__books(request)
        elif catalog == '1.2':
            Parser.__mesh(request)
        elif catalog == '1.3':
            Parser.__nlmcatalog(request)
        elif catalog == '1.4':
            Parser.__pubmed(request)
        elif catalog == '1.5':
            Parser.__pmc(request)
        elif catalog == '2':
            #Parser.__gene(request)
            #Parser.__gds(request)
            #Parser.__geo(request)
            #Parser.__homologene(request)
            Parser.__popset(request)

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
        string = string.replace('.', '')
        string = string.replace('|', '')
        string = string.replace('/', '')
        string = string.replace('--', '')
        string = string.replace('®', '')
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.strip()
        return string

    @staticmethod
    def __books(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/books/?term={request}').content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        literature_url_list = []
        if not soup.find(id="Details"):
            driver = webdriver.Chrome(executable_path=FileSystem.get_driver())
            driver.get(url=f'https://www.ncbi.nlm.nih.gov/books/?term={request}')
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    literature_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(literature_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{literature_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                titles = driver.find_elements_by_class_name('title')
                full_title = soup.findAll(True, {"class": "rsltcont"})[0].p.decode_contents()
                title_book = ''.join(full_title.split(' ')[0:4])
                title_book = Parser.__replace_elem_for_windows(title_book)
                full_title = Parser.__replace_elem_for_windows(full_title)
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
                    if j == 1:
                        pdf = driver.find_elements_by_xpath("//*[contains(text(), 'PDF version of this title')]")
                        if len(pdf) == 1 and not FileSystem.is_exist(f'{full_title}.pdf', f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\Books\\{title_book}\\'):
                            pdf[0].click()
                            pyautogui.hotkey('ctrl', 's')
                            time.sleep(TIME_SLEEP)
                            pyautogui.typewrite(
                                f'{FileSystem.get_directory()}data_parser\\'
                                f'{string_request}\\Literature\\Books\\{title_book}\\{full_title}.pdf')
                            time.sleep(TIME_SLEEP)
                            pyautogui.hotkey('enter')
                            time.sleep(TIME_SLEEP)
                            driver.back()
                            time.sleep(TIME_SLEEP)
                    if not FileSystem.is_exist(f'{title_part}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\Books\\{title_book}\\'):
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Literature\\Books\\{title_book}\\{title_part}.html')
                        time.sleep(TIME_SLEEP)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP)
                    driver.back()
                    time.sleep(TIME_SLEEP)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __mesh(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/mesh/?term={request}').content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        literature_url_list = []
        if not soup.find(id="Details"):
            driver = webdriver.Chrome(executable_path=FileSystem.get_driver())
            driver.get(url=f'https://www.ncbi.nlm.nih.gov/mesh/?term={request}')
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    literature_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(literature_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{literature_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "title"})[0].text
                full_title = Parser.__replace_elem_for_windows(full_title)
                if not FileSystem.is_exist(f'{full_title}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\MeSH\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP/2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Literature\\MeSH\\{full_title}.html')
                    time.sleep(TIME_SLEEP/2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP/2)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __nlmcatalog(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/nlmcatalog/?term={request}').content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        literature_url_list = []
        if not soup.find(id="Details"):
            driver = webdriver.Chrome(executable_path=FileSystem.get_driver())
            driver.get(url=f'https://www.ncbi.nlm.nih.gov/nlmcatalog/?term={request}')
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    literature_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(literature_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{literature_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "title"})[0].text[0:255]
                full_title = Parser.__replace_elem_for_windows(full_title)
                if not FileSystem.is_exist(f'{full_title}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\NLM Catalog\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP/2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Literature\\NLM Catalog\\{full_title}.html')
                    time.sleep(TIME_SLEEP/2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP/2)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __pubmed(request):
        string_request = request
        content_list = []
        literature_url_list = []
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/?term={request}').content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        if not soup.find(class_="altered-search-explanation"):
            driver = webdriver.Chrome(executable_path=FileSystem.get_driver())
            for i in range(0, 21):
                driver.get(url=f'https://pubmed.ncbi.nlm.nih.gov/?term={request}&page={i}')
                content_list.append(driver.page_source)
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "docsum-title"})
                for j in range(0, len(titles_list)):
                    literature_url_list.append(titles_list[j]['href'])
            for i in range(0, len(literature_url_list)):
                driver.get(url=f'https://pubmed.ncbi.nlm.nih.gov{literature_url_list[i]}')
                elem = None
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "heading-title"})[0].text.strip()
                full_title = Parser.__replace_elem_for_windows(full_title)
                try:
                    temp_elem = driver.find_element_by_class_name('linkout-category-links')
                    temp_elem = temp_elem.find_elements_by_tag_name('li')
                    for j in range(0, len(temp_elem)):
                        if temp_elem[j].text.strip() == 'MedGen':
                            elem = temp_elem[j]
                            break
                except NoSuchElementException:
                    pass
                try:
                    temp_elem = driver.find_element_by_class_name('linkout-category-links')
                    temp_elem = temp_elem.find_elements_by_tag_name('li')
                    for j in range(0, len(temp_elem)):
                        if temp_elem[j].text.strip() == 'PubMed Central':
                            elem = temp_elem[j]
                            break
                except NoSuchElementException:
                    pass
                if elem:
                    elem_name = elem.text
                    elem.find_element_by_tag_name('a').click()
                    time.sleep(TIME_SLEEP * 2)
                    driver.switch_to.window(driver.window_handles[1])
                    if not FileSystem.is_exist(f'{elem_name} {full_title}.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Literature\\PubMed\\'):
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP * 4)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Literature\\PubMed\\{elem_name}{full_title}.html')
                        time.sleep(TIME_SLEEP)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP)
                    driver.close()
                    time.sleep(TIME_SLEEP)
                    driver.switch_to.window(driver.window_handles[0])
                if not FileSystem.is_exist(f'{full_title}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\PubMed\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Literature\\PubMed\\{full_title}.html')
                    time.sleep(TIME_SLEEP)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __pmc(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/pmc/?term={request}').content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        literature_url_list = []
        count = 0
        if not soup.find(id="Details"):
            driver = webdriver.Chrome(executable_path=FileSystem.get_driver())
            driver.get(url=f'https://www.ncbi.nlm.nih.gov/pmc/?term={request}')
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class') and count != 0:
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
                    count += 1
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    literature_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(literature_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{literature_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "content-title"})[0].text[0:255]
                full_title = Parser.__replace_elem_for_windows(full_title)
                if not FileSystem.is_exist(f'{full_title}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Literature\\PubMed Central\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Literature\\PubMed Central\\{full_title}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP / 2)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __gene(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/gene/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/gene/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genes_url_list = []
        if soup.find(class_='ncbi-doc-title'):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "gene-name-id"})
                for j in range(0, len(titles_list)):
                    genes_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(genes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genes_url_list[i]}')
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "title"})[0].text[0:255]
                full_title = Parser.__replace_elem_for_windows(full_title)
                try:
                    download = driver.find_element_by_id('button-1083')
                    download.click()
                    time.sleep(TIME_SLEEP * 2)
                    open_pdf = driver.find_element_by_id('menuitem-1056-itemEl')
                    open_pdf.click()
                    download = driver.find_element_by_id('button-1104')
                    time.sleep(TIME_SLEEP)
                    if not FileSystem.is_exist(f'graph_{full_title}.pdf',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Genes\\Gene\\'):
                        download.click()
                        time.sleep(TIME_SLEEP)
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Genes\\Gene\\graph_{full_title}.pdf')
                        time.sleep(TIME_SLEEP / 2)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP / 2)
                        driver.switch_to.window(driver.window_handles[1])
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(2)
                    close = driver.find_element_by_id('tool-1107-toolEl')
                    close.click()
                except (NoSuchElementException, StaleElementReferenceException):
                    pass
                finally:
                    if not FileSystem.is_exist(f'{full_title}.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Genes\\Gene\\'):
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Genes\\Gene\\{full_title}.html')
                        time.sleep(TIME_SLEEP / 2)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP / 2)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __gds(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/gds/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/gds/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genes_url_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genes_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(genes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"style": "text-align: justify"})[0].text[0:255]
                full_title = Parser.__replace_elem_for_windows(full_title)
                if not FileSystem.is_exist(f'{full_title}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genes\\GEO DataSets\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genes\\GEO DataSets\\{full_title}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __geo(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/geoprofiles/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/geoprofiles/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genes_url_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genes_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(genes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "title"})[0].text
                full_title = Parser.__replace_elem_for_windows(full_title[14:240])
                full_title = Parser.__replace_elem_for_windows(full_title)
                if not FileSystem.is_exist(f'{full_title}.html',
                                        f'{FileSystem.get_directory()}data_parser\\'
                                        f'{string_request}\\Genes\\GEO Profiles\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genes\\GEO Profiles\\{full_title}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP)
                profile = driver.find_element_by_class_name('rprt')
                profile = profile.find_element_by_tag_name('a')
                profile.click()
                if not FileSystem.is_exist(f'profile_{full_title}.html',
                                        f'{FileSystem.get_directory()}data_parser\\'
                                        f'{string_request}\\Genes\\GEO Profiles\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genes\\GEO Profiles\\profile_{full_title}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __homologene(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/homologene/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/homologene/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        title_list = []
        genes_url_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genes_url_list.append(titles_list[j].a['href'])
                    title_list.append(titles_list[j].a.text)
            for i in range(0, len(genes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genes_url_list[i]}')
                title = Parser.__replace_elem_for_windows(title_list[i])
                if not FileSystem.is_exist(f'{title}.html',
                                        f'{FileSystem.get_directory()}data_parser\\'
                                        f'{string_request}\\Genes\\Homologene\\'):
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genes\\Homologene\\{title}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()

    @staticmethod
    def __popset(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/popset/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/popset/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genes_url_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                while 'inactive' not in next.get_attribute('class'):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genes_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(genes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "rprt"})[0].text[0:255]
                full_title = Parser.__replace_elem_for_windows(full_title)
                try:
                    links = driver.find_elements_by_class_name('links')
                    if not FileSystem.is_exist(f'Citation_{full_title}.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Genes\\PopSet\\'):
                        links[1].click()
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Genes\\PopSet\\Citation_{full_title}.html')
                        time.sleep(TIME_SLEEP / 2)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP * 2)
                        driver.back()
                    links = driver.find_elements_by_class_name('links')
                    if len(links) == 3:
                        if not FileSystem.is_exist(f'Full_Text_{full_title}.html',
                                                   f'{FileSystem.get_directory()}data_parser\\'
                                                   f'{string_request}\\Genes\\PopSet\\'):
                            links[2].click()
                            time.sleep(TIME_SLEEP)
                            pyautogui.hotkey('ctrl', 's')
                            time.sleep(TIME_SLEEP * 2)
                            pyautogui.typewrite(
                                f'{FileSystem.get_directory()}data_parser\\'
                                f'{string_request}\\Genes\\PopSet\\Full_Text_{full_title}.html')
                            time.sleep(TIME_SLEEP / 2)
                            pyautogui.hotkey('enter')
                            time.sleep(TIME_SLEEP * 2)
                            driver.back()
                except (NoSuchElementException, StaleElementReferenceException):
                    pass
                finally:
                    if not FileSystem.is_exist(f'{full_title}.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Genes\\PopSet\\'):
                        time.sleep(TIME_SLEEP)
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Genes\\PopSet\\{full_title}.html')
                        time.sleep(TIME_SLEEP / 2)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP * 2)
            try:
                raise WebDriverException
            except WebDriverException:
                driver.close()