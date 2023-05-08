import os
import re
import sys
from typing import Callable, Optional, Any
import requests
from colorama import Fore, init
from bs4 import BeautifulSoup
from requests import Response

init()


class Downloader:
    def __init__(self, url: str) -> None:
        self.__url: str = url
        self.__links = list()
        try:
            self.__base: str = re.match("^(https?:\/\/)?([a-z0-9]+\.)*([a-z0-9]+\.[a-z]+)", self.__url).group(0)
        except AttributeError:
            ...
        self.__formats: list[str] = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'tiff']

    def __get(self, url: str = None) -> bytes | None:
        if url:
            print(Fore.GREEN + f"[+] Checking url {url}")
            response: Response = requests.get(url)
        else:
            print(Fore.GREEN + f"[+] Checking url {self.__url}")
            response: Response = requests.get(self.__url)
        if response.status_code == 200:
            return response.content
        print(Fore.RED + f"[-] Fail to access {self.__url}")
        return None

    def __parser(self, url: str = None) -> str:
        if url:
            data: bytes = self.__get(url)
        else:
            data: bytes = self.__get()
        if data:
            parse = BeautifulSoup(data, 'html.parser')
            images = parse.find_all("img")
            links = parse.find_all("a")
            for image in images:
                try:
                    if "http" not in image["src"]:
                        yield self.__base + image['src'].split("?")[0]
                    else:
                        yield image["src"].split("?")[0]
                except KeyError:
                    ...
            for link in links:
                if link.get("href") and link.get("href") != '#' and "https://www.depoisdosquinze" in link.get("href"):
                    if link.get("href") not in self.__links:
                        self.__links.append(link.get("href"))

    def navigate(self) -> None:
        try:
            if not self.__links:
                self.save()
            for link in self.__links:
                self.save(link)
        except Exception as e:
            ...

    def save(self, url: str = None):
        if not os.path.exists(r'../images_from_war'):
            os.makedirs(r'../images_from_war')
        if url is None:
            data = self.__parser()
        else:
            data = self.__parser(url)
        for index, image in enumerate(data):
            try:
                img = requests.get(image)
                print(Fore.GREEN + f"[+] Downloading images from {image}")
                if img.status_code == 200:
                    format_ = image.split('.')[-1]
                    if format_ in self.__formats:
                        with open(f"../images_from_war/{index}.{format_}", "wb") as f:
                            f.write(img.content)
            except Exception:
                ...


if __name__ == '__main__':
    d: Downloader = Downloader("https://www.depoisdosquinze.com/2017/03/30/dica-de-viagem-um-roteiro-especial-por-campos-do-jordao/")
    d.navigate()
