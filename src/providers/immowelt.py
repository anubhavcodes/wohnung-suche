from typing import Set

from providers import BaseScraper


class Immowelt(BaseScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soup = self.get_soup()

    @property
    def title(self) -> str:
        try:
            return self.soup.find("title").text
        except (AttributeError, IndexError):
            return "Unable to extract title"

    @property
    def address(self) -> str:
        try:
            return self.soup.find("div", {"class": "location"}).text.strip("\n")
        except AttributeError:
            return "Unable to extract location"

    @property
    def cold_rent(self) -> str:
        try:
            return self.soup.find("div", {"class": "hardfact"}).text.strip("\n").split("\n")[0]
        except (AttributeError, IndexError):
            return "Unable to extract cold rent"

    @property
    def warm_rent(self) -> str:
        try:
            return self.soup.findAll("div", {"class": "datatable"})[0].findAll("div")[-1].text
        except (AttributeError, IndexError):
            return "Unable to extract warm rent"

    @property
    def available_from(self) -> str:
        try:
            return [x for x in self.soup.findAll("div", {"class": "section_content"})[4].text.strip().split("\n") if x][
                1
            ]
        except (AttributeError, IndexError):
            return "Unable to extract date of availability"

    @property
    def construction_year(self) -> str:
        try:
            return self.soup.findAll("div", {"class": "section_content"})[4].text.strip().split("\n")[0]
        except (AttributeError, IndexError):
            return "Unable to extract construction year"

    @property
    def size(self) -> str:
        try:
            return self.soup.findAll("div", {"class": "hardfact"})[1].text.split("\n")[1].strip()
        except (AttributeError, IndexError):
            return "Unable to extract size"

    @property
    def images(self) -> Set[str]:
        try:
            return {div.find("img").attrs.get("src") for div in self.soup.findAll("div", {"class": "carousel-item"})}
        except (AttributeError, IndexError, TypeError):
            return set()
