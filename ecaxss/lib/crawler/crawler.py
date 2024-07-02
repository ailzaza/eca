import requests
from lib.helper.Log import *
from lib.helper.helper import *
from lib.core import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Process

class crawler:
    visited = []

    @classmethod
    def getLinks(cls, base):
        lst = []
        conn = requests.Session()
        text = conn.get(base).text
        isi = BeautifulSoup(text, "html.parser")

        for obj in isi.find_all("a", href=True):
            url = obj["href"]

            if urljoin(base, url) in cls.visited:
                continue
            elif url.startswith("mailto:") or url.startswith("javascript:"):
                continue
            elif url.startswith(base) or "://" not in url:
                lst.append(urljoin(base, url))
                cls.visited.append(urljoin(base, url))

        return lst

    @classmethod
    def crawl(cls, base, payload, method, user_agent=None):
        urls = cls.getLinks(base)

        for url in urls:
            if "mhs_jadkul.php" in url:
                if url.startswith("https://") or url.startswith("http://"):
                    p = Process(target=core.main, args=(url, payload, method, user_agent))
                    p.start()
                    p.join()

                # Recursively crawl the URL if it contains the desired endpoint
                cls.crawl(url, payload, method, user_agent)
