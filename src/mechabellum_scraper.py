"""Contains an scraping script for the mechamonarch.com tier list."""

import re

import requests
from bs4 import BeautifulSoup, Comment


def get_unit_tiers() -> list[dict[(str, str)]]:
    """Scrapes mechamonarch.com and returns a dictionary that contains the Mechabellum units tier list.

    Returns:
        A dictionary of all unit tiers that includes an array of tuples of the unit name and link.
    """
    r = requests.get("https://mechamonarch.com/guide/mechabellum-unit-tier-list/", timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")

    comments = soup.find_all(string=lambda string: isinstance(string, Comment))

    tier_divs = []
    for comment in comments:
        if any(f"tier {tier} list" in comment.lower() for tier in "sabcdef") and "tier list end" not in comment.lower():
            next_element = comment.find_next()
            if next_element and next_element.name == "div":
                tier_divs.append(next_element)

    unit_tiers = {}
    for div in tier_divs:
        tier_mark = div.find("span", class_="tier-block").text
        unit_tiers[tier_mark] = []
        links = div.find_all('a', href=re.compile("/unit/"))
        for link in links:
            name = link.find_next("small").text
            unit_tiers[tier_mark].append((name, link.get("href")))

    return unit_tiers

get_unit_tiers()
