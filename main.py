import argparse
import time
from analyzer import Analyser
from downloader import Downloader


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tarefa para o ifmg")
    parser.add_argument("-u", "--url", required=True)
    args = parser.parse_args()
    down: Downloader = Downloader(args.url)
    analyzer: Analyser = Analyser("images_from_war")
    down.save()
    time.sleep(2)
    analyzer.execute()
