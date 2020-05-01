from datetime import datetime
from typing import Set

from providers import BaseScraper


class Immoscout(BaseScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soup = self.get_soup(use_requests=True)

    @property
    def title(self) -> str:
        return self.soup.find("title").text

    @property
    def cold_rent(self) -> str:
        try:
            return self.soup.find("div", {"class": "is24-preis-section"}).text.strip().split("  ")[0]
        except (AttributeError, ValueError, IndexError):
            return "Unable to extract cold rent"

    @property
    def warm_rent(self) -> str:
        try:
            return self.soup.find("dd", {"class": "is24qa-gesamtmiete"}).text.strip()
        except (AttributeError, ValueError, IndexError):
            return "Unable to extract warm rent"
        pass

    @property
    def address(self) -> str:
        try:
            return self.soup.find("div", {"class": "address-block"}).text.strip()
        except (AttributeError, ValueError):
            return "Unable to extract address"

    @property
    def available_from(self) -> str:
        try:
            date_str = self.soup.find("dd", {"class": "is24qa-bezugsfrei-ab"}).text.strip()
            return datetime.strptime(date_str, "%d%m%Y").strftime("%d-%m-%Y")
        except (ValueError, TypeError, AttributeError):
            return "Unable to extract available from date"

    @property
    def size(self) -> str:
        try:
            return self.soup.find("dd", {"class": "is24qa-wohnflaeche-ca"}).text.strip()
        except (ValueError, TypeError):
            return "Unable to extract size."

    @property
    def construction_year(self) -> str:
        try:
            return self.soup.find("dd", {"class": "is24qa-baujahr"}).text.strip()
        except (ValueError, TypeError):
            return "Unable to extract construction year"

    @property
    def images(self) -> Set[str]:
        try:
            images = {
                list(div.children)[1].attrs.get("data-src")
                for div in self.soup.findAll("div", {"class": "sp-thumbnail"})
            }
            return {url[: url.find("/ORIG")] for url in images}
        except (ValueError, TypeError, AttributeError, IndexError):
            return set()
