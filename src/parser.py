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
        FileSystem.create_folder('Genomes', request)
        FileSystem.create_folder('Proteins', request)
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
            Parser.__gene(request)
            Parser.__gds(request)
            Parser.__geo(request)
            Parser.__homologene(request)
            Parser.__popset(request)
        elif catalog == '2.1':
            Parser.__gene(request)
        elif catalog == '2.2':
            Parser.__gds(request)
        elif catalog == '2.3':
            Parser.__geo(request)
        elif catalog == '2.4':
            Parser.__homologene(request)
        elif catalog == '2.5':
            Parser.__popset(request)
        elif catalog == '3':
            Parser.__assembly(request)
            Parser.__biocollections(request)
            Parser.__bioproject(request)
            Parser.__biosample(request)
            Parser.__genome(request)
            Parser.__nuccore(request)
            Parser.__sra(request)
        elif catalog == '3.1':
            Parser.__assembly(request)
        elif catalog == '3.2':
            Parser.__biocollections(request)
        elif catalog == '3.3':
            Parser.__bioproject(request)
        elif catalog == '3.4':
            Parser.__biosample(request)
        elif catalog == '3.5':
            Parser.__genome(request)
        elif catalog == '3.6':
            Parser.__nuccore(request)
        elif catalog == '3.7':
            Parser.__sra(request)
        elif catalog == '4':
            Parser.__cdd(request)
            Parser.__ipg(request)
            Parser.__proteinclusters(request)
            Parser.__sparcle(request)
            Parser.__structure(request)
        elif catalog == '4.1':
            Parser.__cdd(request)
        elif catalog == '4.2':
            Parser.__ipg(request)
        elif catalog == '4.3':
            Parser.__protein(request)
        elif catalog == '4.4':
            Parser.__proteinclusters(request)
        elif catalog == '4.5':
            Parser.__sparcle(request)
        elif catalog == '4.6':
            Parser.__structure(request)

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
    def __close_chrome(driver):
        try:
            raise WebDriverException
        except WebDriverException:
            driver.close()

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

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
            Parser.__close_chrome(driver)

    @staticmethod
    def __assembly(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/assembly/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/assembly/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            if soup.findAll(True, {'class': 'ncbi-doc-title'}):
                try:
                    elem = driver.find_element_by_class_name('ncbi-doc-title')
                    full_title = elem.text
                    if not FileSystem.is_exist(f'{full_title}.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Genomes\\Assembly\\'):

                        elem.find_element_by_tag_name('a').click()
                        time.sleep(TIME_SLEEP * 4)
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Genomes\\Assembly\\{full_title}.html')
                        time.sleep(TIME_SLEEP)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP)
                        driver.back()
                except (NoSuchElementException, StaleElementReferenceException):
                    pass
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
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
            for i in range(0, len(full_title_list)):
                full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\Assembly\\'):
                    time.sleep(TIME_SLEEP * 6)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genomes\\Assembly\\{full_title_list[i]}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __biocollections(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/biocollections/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/biocollections/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
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
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\Biocollections\\'):
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genomes\\Biocollections\\{full_title_list[i]}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __bioproject(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/bioproject/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/bioproject/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
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
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\Bioprojects\\'):
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genomes\\Bioproject\\{full_title_list[i]}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __biosample(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/biosample/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/biosample/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
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
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\Biosample\\'):
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genomes\\Biosamples\\{full_title_list[i]}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __genome(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/genome/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/genome/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            if soup.findAll(True, {'class': 'GenomeTitle'}):
                if not FileSystem.is_exist(f'{string_request}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\Genome\\'):
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genomes\\Genome\\{string_request}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            else:
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
                        genomes_url_list.append(titles_list[j].a['href'])
                        full_title_list.append(titles_list[j].text)
                    for i in range(0, len(full_title_list)):
                        full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
                for i in range(0, len(genomes_url_list)):
                    driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Genomes\\Biosample\\'):
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Genomes\\Biosample\\{full_title_list[i]}.html')
                        time.sleep(TIME_SLEEP / 2)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __nuccore(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/nuccore/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/nuccore/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(20):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                count = 0
                if i != 0:
                    if full_title_list[i - 1] == full_title_list[i]:
                        count += 1
                    else:
                        count = 0
                if not FileSystem.is_exist(f'{full_title_list[i]}[{count}].html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\Nucleotide\\'):
                    driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                    time.sleep(TIME_SLEEP * 2)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    div = soup.find('pre', {'class': 'genbank'}).prettify()
                    with open(f'{FileSystem.get_directory()}data_parser\\{string_request}\\Genomes\\'
                              f'Nucleotide\\{full_title_list[i]}[{count}].html', 'w') as page:
                        page.write(div)
            Parser.__close_chrome(driver)

    @staticmethod
    def __sra(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/sra/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/sra/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(20):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                full_title = soup.findAll(True, {"class": "details"})[0].b.text
                full_title = Parser.__replace_elem_for_windows(full_title)
                if not FileSystem.is_exist(f'{full_title}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Genomes\\SRA\\'):
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Genomes\\SRA\\{full_title}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __cdd(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/cdd/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/cdd/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(20):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Proteins\\Conversed Domains\\'):
                    time.sleep(TIME_SLEEP * 5)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Proteins\\Conversed Domains\\{full_title_list[i]}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __ipg(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/ipg/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/ipg/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(20):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                time.sleep(TIME_SLEEP * 4)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                div_title = soup.findAll(True, {'class': 'ipg-title'})
                div_title = div_title[0].div.find_all('p')
                full_title = div_title[0].text[4:len(div_title[0].text)] + div_title[1].text
                full_title = Parser.__replace_elem_for_windows(full_title)
                for k in range(0, 20):
                    if not FileSystem.is_exist(f'{full_title}{k+1}.20.html',
                                               f'{FileSystem.get_directory()}data_parser\\'
                                               f'{string_request}\\Proteins\\Identical Protein Group\\'):
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.hotkey('ctrl', 's')
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.typewrite(
                            f'{FileSystem.get_directory()}data_parser\\'
                            f'{string_request}\\Proteins\\Identical Protein Group\\{full_title}{k+1}.20.html')
                        time.sleep(TIME_SLEEP * 2)
                        pyautogui.hotkey('enter')
                        time.sleep(TIME_SLEEP * 2)
                    try:
                        next = driver.find_element_by_class_name('next')
                        for i in range(2):
                            next.click()
                            next = driver.find_element_by_class_name('next')
                    except NoSuchElementException:
                        pass
            Parser.__close_chrome(driver)

    @staticmethod
    def __proteinclusters(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/proteinclusters/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/proteinclusters/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        if not soup.findAll(True, {'class': 'warn'}):
            full_title = soup.findAll(True, {'class':'Title'})[0].text
            full_title = Parser.__replace_elem_for_windows(full_title)
            if not FileSystem.is_exist(f'{full_title}.html',
                                       f'{FileSystem.get_directory()}data_parser\\'
                                       f'{string_request}\\Proteins\\Protein Clusters\\'):
                time.sleep(TIME_SLEEP * 2)
                pyautogui.hotkey('ctrl', 's')
                time.sleep(TIME_SLEEP * 2)
                pyautogui.typewrite(
                    f'{FileSystem.get_directory()}data_parser\\'
                    f'{string_request}\\Proteins\\Protein Clusters\\{full_title}.html')
                time.sleep(TIME_SLEEP * 2)
                pyautogui.hotkey('enter')
                time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __sparcle(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/sparcle/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/sparcle/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(20):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                count = 0
                driver.get(url=f'{genomes_url_list[i]}')
                if i != 0:
                    if full_title_list[i-1] == full_title_list[i]:
                        count += 1
                    else:
                        count = 0
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}[{count}].html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Proteins\\Sparcle\\'):
                    time.sleep(TIME_SLEEP * 4)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Proteins\\Sparcle\\{full_title_list[i]}[{count}].html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __structure(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/structure/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/structure/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(2):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if not FileSystem.is_exist(f'{full_title_list[i]}.html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Proteins\\Structure\\'):
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(TIME_SLEEP * 2)
                    pyautogui.typewrite(
                        f'{FileSystem.get_directory()}data_parser\\'
                        f'{string_request}\\Proteins\\Structure\\{full_title_list[i]}.html')
                    time.sleep(TIME_SLEEP / 2)
                    pyautogui.hotkey('enter')
                    time.sleep(TIME_SLEEP * 2)
            Parser.__close_chrome(driver)

    @staticmethod
    def __protein(request):
        string_request = request
        request = Parser.__replace_elem_in_request(request)
        content = requests.get(f'https://www.ncbi.nlm.nih.gov/protein/?term={request}').content.decode('utf-8')
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(executable_path=FileSystem.get_driver(), options=options)
        driver.get(url=f'https://www.ncbi.nlm.nih.gov/protein/?term={request}')
        soup = BeautifulSoup(content, 'html.parser')
        content_list = []
        genomes_url_list = []
        full_title_list = []
        if not soup.findAll(True, {'class': 'warn'}):
            content_list.append(driver.page_source)
            try:
                next = driver.find_element_by_class_name('next')
                for i in range(20):
                    next.click()
                    content_list.append(driver.page_source)
                    next = driver.find_element_by_class_name('next')
            except NoSuchElementException:
                pass
            for i in range(0, len(content_list)):
                soup = BeautifulSoup(content_list[i], 'html.parser')
                titles_list = soup.findAll(True, {"class": "title"})
                for j in range(0, len(titles_list)):
                    genomes_url_list.append(titles_list[j].a['href'])
                    full_title_list.append(titles_list[j].text)
                for i in range(0, len(full_title_list)):
                    full_title_list[i] = Parser.__replace_elem_for_windows(full_title_list[i])
            for i in range(0, len(genomes_url_list)):
                count = 0
                if i != 0:
                    if full_title_list[i - 1] == full_title_list[i]:
                        count += 1
                    else:
                        count = 0
                if not FileSystem.is_exist(f'{full_title_list[i]}[{count}].html',
                                           f'{FileSystem.get_directory()}data_parser\\'
                                           f'{string_request}\\Proteins\\Protein\\'):
                    driver.get(url=f'https://www.ncbi.nlm.nih.gov{genomes_url_list[i]}[{count}]')
                    time.sleep(TIME_SLEEP * 2)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    div = soup.find('pre', {'class': 'genbank'}).prettify()
                    with open(f'{FileSystem.get_directory()}data_parser\\{string_request}\\Proteins\\'
                              f'Protein\\{full_title_list[i]}[{count}].html', 'w') as page:
                        page.write(div)
            Parser.__close_chrome(driver)