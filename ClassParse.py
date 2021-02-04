import os
import uuid
import zipfile
from urllib import parse

import requests
from bs4 import BeautifulSoup

from settings import base_dir
class PathsParse:

    default_url = 'Not url'

    def __init__(self, base_url=default_url):
        self._url = base_url
        self.name_archive = 'archive'
        self.dir_archive = os.path.join(base_dir, self.name_archive)
        self.name_file_archive = f"{uuid.uuid5(uuid.NAMESPACE_DNS, self._url).hex}.zip"
        self.dir_name_file_archive = os.path.join(self.dir_archive, self.name_file_archive)
        self.name_subdir = None
        self.path_archive_files = None
        self.__create_directory(self.dir_archive)


    """получить имя поддиректории"""
    def get_name_subdir(self, url):
        self.name_subdir =  url.replace('/', '_')

    """получить путь с подпапкой для распределения файлов по ссылкам вложенности"""
    def get_path_archive_files(self, file_name):
        self.path_archive_files = os.path.join(self.name_subdir, file_name)

    """Создать директорию папки архива"""
    def __create_directory(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)



class LinkParse:

    list_ext = ['svg', 'png', 'jpg', 'pdf', 'xml', 'css', 'js', 'gif', 'ico', 'html']
    default_url = 'Not url'

    def __init__(self, base_url=default_url):
        self._base_url = base_url
        self.links_levels = []
        self.urls_files = []


    """получить данные для обработки вложености ссылок"""
    def __get_data_link(self):
        url_obj = parse.urlparse(self._base_url)
        path = f"{url_obj.netloc}{url_obj.path}"
        length_list = len(path.split('/'))
        return url_obj, path, length_list

    """собрать вложенность ссылок"""
    def link_levels(self):
        url_obj, path, length_list = self.__get_data_link()
        for num in range(length_list)[::-1]:
            anchor = path.rsplit('/', num)[0]
            self.links_levels.append(f"{url_obj.scheme}://{anchor}")

    """проверка ссылки на валидность"""
    def is_link_valid(self, link):
        parsed = parse.urlparse(link)
        return bool(parsed.netloc) and bool(parsed.scheme)

    """убрать окончание двоучных запросов в ссылке"""
    def __trim_link(self, url):
        if '?' in url:
            pos = url.index("?")
            return url[:pos]
        return url

    """проверяем есть расширение собранных файлов в указанном списке LIS_EXT"""
    def __is_ext_list(self, ext):
        if not ext[1:] in LinkParse.list_ext:
            return True

    """проверка ссылки на валидность"""
    def __is_valid(self, url):
        parsed = parse.urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    """собираем все ссылки из контента в список"""
    def get_urls_files(self, bs_content):
        for content in bs_content:
            link = content.attrs.get("href") or content.attrs.get("src")
            if not link:
                continue
            link_ = self.__trim_link(link)
            _, ext = os.path.splitext(link_)
            if self.__is_ext_list(ext):
                continue
            url_ = parse.urljoin(self._base_url, link_)
            if not self.__is_valid(url_): # проверить ссылку на целостность перед тем как упаковывать
                continue
            self.urls_files.append(url_)



class FilesParse:

    default_url = 'Not url'

    def __init__(self, path_obj):
        self._path_obj = path_obj
        self._res_obj = ResponseParse()
        self.urls_files = []
        self.file_name = None


    """Получить имя файла"""
    def __get_file_name(self, url_file):
        string = url_file.split("/")[-1]
        if not string == "":
            self.file_name = string


    """сохраняем файлы"""
    def save_files(self, urls_files):
        for url_file in urls_files:
            self.__get_file_name(url_file)
            self._res_obj.get_response(url_file, stream=True) # self._res_obj.response
            self._path_obj.get_path_archive_files(self.file_name)
            self.__create_file()


    """создание файла"""
    def __create_file(self):
        with zipfile.ZipFile(self._path_obj.dir_name_file_archive, "a") as zip:
            if not self.file_name in zip.namelist():
                zip.writestr(self._path_obj.path_archive_files, self._res_obj.response.content)



class ResponseParse():

    def __init__(self):
        self.buf_size= 1024
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        self.response = None

    """получить ответ запроса"""
    def get_response(self, url, stream=False):
        res = self.session.get(url=url, headers=self.session.headers, stream=stream)
        if not res.status_code == 200:
            self.response = True
        self.response = res



class ContentParse:

    def __init__(self, res_obj):
        self._res_obj = res_obj
        self.bs_content = None


    """собираем все данные с сылками из контента"""
    def content_list(self):
        soup = BeautifulSoup(self._res_obj.response.content, "lxml")
        href = soup.find_all(href=True)
        src = soup.find_all(src=True)
        href.extend(src)
        self.bs_content =  href



class Parse:

    default_url = 'Not url'
    default_limit = 0

    def __init__(self, url=default_url, limit=default_limit):
        self.url = url
        self.limit = limit
        self.count = 0
        self._link_obj = LinkParse(self.url)
        self._path_obj = PathsParse(self.url)
        self._res_obj = ResponseParse()
        self._cont_obj = ContentParse(self._res_obj)
        self._file_obj = FilesParse(self._path_obj)


    """проверка указанного лимита вложенности"""
    def __is_limit_exc(self):
        self.count += 1
        if self.limit == 0:
            return False
        elif self.count > self.limit:
            return True

    """получить список имен файлов в папке"""
    @property
    def get_names_files(self):
        return [os.path.splitext(file)[0] for file in os.listdir(self._path_obj.dir_archive)]

    def run(self):

        self._link_obj.link_levels() # self.links_levels

        for link in self._link_obj.links_levels:

            if self.__is_limit_exc():
                break

            print(link)

            self._res_obj.get_response(link) # self._res_obj.response проверить что каждый объект создает свой запрос для своего класса
            self._path_obj.get_name_subdir(link)  # self.name_subdir получить имя подпапки

            if not self._res_obj.response:
                continue

            if not self._link_obj.is_link_valid(link):
                continue

            self._cont_obj.content_list() # self._cont_obj.bs_content
            self._link_obj.get_urls_files(self._cont_obj.bs_content) # self._link_obj.urls_files

            print(self._link_obj.urls_files)

            self._file_obj.save_files(self._link_obj.urls_files)

            self._link_obj.urls_files.clear() # обнуляем массив с ссылками файлов, переделать сделать метод для удаления совйства


