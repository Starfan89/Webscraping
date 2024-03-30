import requests
from bs4 import BeautifulSoup
import json


class PyUdvikler():
    def __init__(self) -> None:
        self.kaldenavn = 'Steffan Holst Hansen'
        self.stedord = Stedord(' ')
        self.cases = [RecursiveWebScraper('http://www.sik.dk', 2)]


class Stedord():
    def __init__(self, boejning) -> None:
        self.ejefald = 'Steffans'
        self.grundform = 'Steffan'


class Case():
    pass


class RecursiveWebScraper(Case):
    """
    En klasse til at udføre rekursiv webscraping af en given hjemmeside,
    gemme data i en JSON-fil, og holde styr på "dybden" af scraping.

    Attributes
    ----------
    base_url : string
        Grundlæggende URL for webscraping.
    max_depth : integer
        Maksimal dybde for rekursion under scraping.
    visited : dictionary
        En ordbog til at spore besøgte URLs og deres relationer.

    Methods
    -------
    scrape(url, depth=0)
        Rekursivt scraper givne URL og dens henvisninger indtil maksimal dybde.
    _get_html(url)
        Returnerer HTML-indholdet af en given URL.
    _extract_links(html)
        Finder og returnerer alle links på en given HTML-side.
    _save_to_json()
        Gemmer de besøgte URLs og deres relationer i en JSON-fil.
    """

    def __init__(self, base_url, max_depth):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited = {base_url: []}

    def scrape(self, url, depth=0):
        """
        Rekursivt scraper givne URL og dens henvisninger indtil maksimal dybde.

        Parameters
        ----------
        url : string
            URL'en der skal scrapes.
        depth : integer
            Den aktuelle dybde af rekursion (default er 0).
        """
        if depth > self.max_depth:
            return
        html = self.get_html(url)
        if html:
            links = self.extract_links(html)
            self.visited[url] = links
            for link in links:
                if link not in self.visited:
                    self.scrape(link, depth + 1)

    def get_html(self, url):
        """
        Returnerer HTML-indholdet af en given URL.

        Parameters
        ----------
        url : string
            URL'en hvis HTML-indhold skal hentes.

        Returns
        -------
        string
            HTML-indholdet af den givne URL, hvis tilgængeligt.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def extract_links(self, html):
        """
        Finder og returnerer alle links på en given HTML-side.

        Parameters
        ----------
        html : string
            HTML-indholdet fra en webside.

        Returns
        -------
        list
            En liste af unikke URLs fundet på siden.
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.add(href)
        return list(links)

    def save_to_json(self):
        """
        Gemmer de besøgte URLs og deres relationer i en JSON-fil.
        """
        with open('visited_links.json', 'w') as file:
            json.dump(self.visited, file, indent=4)

    def beregn(self):
        self.scrape(self.base_url)
        return self.visited
