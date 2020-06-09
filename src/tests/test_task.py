from task import get_formatted_info


def test_get_formatted_info():
    result = {
        "title": "title",
        "cold_rent": "cold_rent",
        "warm_rent": "warm_rent",
        "available_from": "available_from",
        "address": "address",
        "size": "size",
        "construction_year": "construction_year",
    }
    expected_desc = "# title\n\n**address**: address\n**cold**: cold_rent\n**warm**: warm_rent\n**size**: size\n"
    expected_desc += "**available from**: available_from\n**construction year**: construction_year"
    expected_desc.strip()
    name, desc = get_formatted_info(result)
    assert name == "address"
    assert desc == expected_desc
