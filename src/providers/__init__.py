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
            "title": self.title if self.is_active else "DEACTIVATED",
            "cold_rent": self.cold_rent if self.is_active else "DEACTIVATED",
            "warm_rent": self.warm_rent if self.is_active else "DEACTIVATED",
            "available_from": self.available_from if self.is_active else "DEACTIVATED",
            "address": self.address if self.is_active else "DEACTIVATED",
            "size": self.size if self.is_active else "DEACTIVATED",
            "construction_year": self.construction_year if self.is_active else "DEACTIVATED",
            "images": self.images or "" if self.is_active else "DEACTIVATED",
            "url": self.url if self.is_active else [],
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

    @property
    def is_active(self) -> bool:
        raise NotImplementedError
