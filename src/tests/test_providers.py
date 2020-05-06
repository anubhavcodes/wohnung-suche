import os
from unittest import mock

import pytest
from bs4 import BeautifulSoup
from config import Config
from providers.immoscout import Immoscout
from providers.immowelt import Immowelt

EXPECTED_RESPONSES = {
    "immowelt": {
        "title": "Doppelhaushälfte (KfW 70) in Hamburg-Niendorf Doppelhaushälfte Hamburg (2VZAU4E)",
        "cold_rent": "2.000 €\xa0 ",
        "warm_rent": "2.150 €",
        "available_from": "Baujahr: 2015",
        "address": "22453 Hamburg (Niendorf)\n22453 Hamburg (Niendorf)\nZur Karte",
        "size": "140 m²",
        "construction_year": "Doppelhaushälfte",
        "images": {
            "/App_Themes/MID_0/images/misc/clear.gif",
            "https://media-pics1.immowelt.org/2/4/D/3/600_A72CBA68FBAB4400B359D7228B853D42.jpg",
            "https://media-pics2.immowelt.org/A/A/7/B/600_364B37110DC3443D9F7537F812EBB7AA.jpg",
            "https://media-pics2.immowelt.org/F/5/4/8/600_91612ECED5044A75999B4596A15B845F.jpg",
            "https://media-pics2.immowelt.org/E/E/8/7/600_8443051711324056B036737E4C1078EE.jpg",
            "https://media-pics1.immowelt.org/2/B/A/1/600_41D5FC7946F64F27BBE56C0356671AB2.jpg",
        },
    },
    "immoscout": {
        "title": "Wohnen in der Gartenstadt",
        "cold_rent": "1.650 €",
        "warm_rent": "2.039 €",
        "available_from": "Unable to extract available from date",
        "address": "Pillauer Straße 25-27,\n22049 Hamburg, Wandsbek",
        "size": "139 m²",
        "construction_year": "2019",
        "images": {
            "https://pictures.immobilienscout24.de/listings/c3361def-932e-4f71-82ce-00b3681e7837-1376755925.jpg",
            "https://pictures.immobilienscout24.de/listings/347a7cd6-8272-42b9-8c95-01c6605578e7-1376755941.jpg",
            "https://pictures.immobilienscout24.de/listings/c3362578-957e-4bc1-b476-72251e3ba8ce-1376755936.jpg",
            "https://pictures.immobilienscout24.de/listings/51872a25-9f25-4100-8640-b9e35e012bf1-1376755928.jpg",
            "https://pictures.immobilienscout24.de/listings/005dc9a3-2e7e-4c39-9761-d4b0bb5a3a44-1376755924.jpg",
            "https://pictures.immobilienscout24.de/listings/db0c3aa9-6509-4dae-b136-d091b46eaec3-1376755933.jpg",
            "https://pictures.immobilienscout24.de/listings/5eb1a94f-7a36-47b3-9ef4-95b11d40679b-1376755931.jpg",
            "https://pictures.immobilienscout24.de/listings/67937e99-02c5-44e7-b17d-c10fa88d2154-1376755934.jpg",
            "https://pictures.immobilienscout24.de/listings/dc2bcf1a-ab63-42ee-8628-f610b5cd4184-1376755922.jpg",
            "https://pictures.immobilienscout24.de/listings/4b77eb96-09d6-4dc8-ac2a-b273e9bbc468-1376755939.jpg",
            "https://pictures.immobilienscout24.de/listings/865115cf-88e3-4bcf-8ca7-19c76a576e5f-1376755938.jpg",
            "https://pictures.immobilienscout24.de/listings/0a974d21-4f44-42cc-a962-2f2e56243e07-1376755937.jpg",
            "https://pictures.immobilienscout24.de/listings/71cc86dd-5763-41c4-a4a1-66a984b8ca02-1376755935.jpg",
        },
    },
}

PROVIDERS = {"immowelt": Immowelt, "immoscout": Immoscout}


@pytest.fixture
def source():
    fixtures_dir = os.path.join(Config.BASE_DIR, "tests", "fixtures")
    html = {}
    for source in ["immowelt.html", "immoscout.html"]:
        with open(os.path.join(fixtures_dir, source)) as f:
            html[source.split(".")[0]] = f.read()
    return html


@pytest.mark.parametrize("provider", ["immowelt", "immoscout"])
@mock.patch("providers.BaseScraper.get_soup")
def test_provides_return_correct_api_for_known_values(mocked_soup, provider, source):
    soup = BeautifulSoup(source[provider], "html.parser")
    mocked_soup.return_value = soup
    provider_cls = PROVIDERS[provider]
    p = provider_cls(url="foo")
    result = p.scrape()
    assert result["title"] == EXPECTED_RESPONSES[provider]["title"]
    assert result["address"] == EXPECTED_RESPONSES[provider]["address"]
    assert result["construction_year"] == EXPECTED_RESPONSES[provider]["construction_year"]
