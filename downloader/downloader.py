import os
import re
import requests
from colorama import Fore, init
from bs4 import BeautifulSoup
from requests import Response

init()


class Downloader:
    def __init__(self, url: str) -> None:
        self.__url: str = url
        try:
            self.__base: str = re.match("^(https?:\/\/)?([a-z0-9]+\.)*([a-z0-9]+\.[a-z]+)", self.__url).group(0)
        except AttributeError:
            ...
        self.__formats: list[str] = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'tiff']

    def __get(self) -> bytes | None:
        print(Fore.GREEN + f"[+] Checking url {self.__url}")
        response: Response = requests.get(self.__url)
        if response.status_code == 200:
            return response.content
        print(Fore.RED + f"[-] Fail to access {self.__url}")
        return None

    def __parser(self) -> str:
        data: bytes = self.__get()
        if data:
            parse = BeautifulSoup(data, 'html.parser')
            images = parse.find_all("img")
            for image in images:
                if "http" not in image["src"]:
                    yield self.__base + image['src']
                else:
                    yield image['src']

    def save(self) -> None:
        if not os.path.exists(r'images_from_war'):
            os.makedirs(r'images_from_war')
        for index, image in enumerate(self.__parser()):
            print(image)
            try:
                img = requests.get(image)
                print(Fore.GREEN + f"[+] Downloading images from {image}")
                if img.status_code == 200:
                    format_ = image.split('.')[-1]
                    if format_ in self.__formats:
                        with open(f"images_from_war/{index}.{format_}", "wb") as f:
                            f.write(img.content)
            except Exception:
                ...


if __name__ == '__main__':
    d: Downloader = Downloader("https://www.serradacantareirahoje.com/2023/05/06/03-a-05-05-2023-bem-vindo-ao-blog-oficial-da-policia-militar-do-estado-de-sao-paulo-site-oficial-%E2%A4%B5%EF%B8%8F/")
    d.save()
