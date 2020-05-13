from time import sleep
from typing import Dict, List

import attr
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


@attr.s
class BaseScraper:
    url = attr.ib()
    headers = {"User-Agent": "github.com/anubhavcodes/wohnung-suche"}

    def get_soup(self, use_requests=False):
        if use_requests:
            r = requests.get(self.url, headers=self.headers)
            return BeautifulSoup(r.text, "html.parser")
        opts = Options()
        opts.headless = True
        browser = Firefox(options=opts)
        browser.get(self.url)
        sleep(2)
        return BeautifulSoup(browser.page_source, "html.parser")

    def scrape(self) -> Dict:
        return {
            "title": self.title,
            "cold_rent": self.cold_rent,
            "warm_rent": self.warm_rent,
            "available_from": self.available_from,
            "address": self.address,
            "size": self.size,
            "construction_year": self.construction_year,
            "images": self.images or "",
            "url": self.url,
        }

    @property
    def title(self) -> str:
        raise NotImplementedError

    @property
    def cold_rent(self) -> str:
        raise NotImplementedError

    @property
    def warm_rent(self) -> str:
        raise NotImplementedError

    @property
    def available_from(self) -> str:
        raise NotImplementedError

    @property
    def address(self) -> str:
        raise NotImplementedError

    @property
    def size(self) -> str:
        raise NotImplementedError

    @property
    def construction_year(self) -> str:
        raise NotImplementedError

    @property
    def images(self) -> List[str]:
        raise NotImplementedError
