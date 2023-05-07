import os
import PIL
from PIL import Image  # pip install Pillow
from colorama import Fore, init
from PIL.ExifTags import TAGS, GPSTAGS
import exifread

init()


class Analyser:
    def __init__(self, img_path: str) -> None:
        self.__img_path = img_path

    def __remove(self, path: str) -> None:
        try:
            os.remove(path)
        except PermissionError as e:
            print(Fore.RED + f"[-] {e}")
        except FileNotFoundError:
            pass

    def execute(self) -> None:
        print(Fore.YELLOW + f"[+] Getting data from image...")
        to_remove: list[str] = list()
        for images in os.listdir(self.__img_path):
            print(self.__img_path + '/' + images)
            with open(self.__img_path + '/' + images, 'rb') as f:
                tags = exifread.process_file(f)
                print(tags)
                lat_tag = 'GPS GPSLatitude' in tags
                long_tag = 'GPS GPSLongitude' in tags
                if lat_tag and long_tag:
                    lat = tags['GPS GPSLatitude']
                    long = tags['GPS GPSLongitude']
                    print(Fore.CYAN + f'Latitude: {lat} \nLongitude: {long}')
                else:
                    to_remove.append(self.__img_path + images)
            for img in to_remove:
                print(Fore.BLUE + f"[+] Deleting {img}")
                self.__remove(img)


if __name__ == '__main__':
    a: Analyser = Analyser(r"../images_from_war/")
    a.execute()
