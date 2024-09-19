import requests
from bs4 import BeautifulSoup


class EcoportParser:
    columns = ["title", "date", "place", "description", "link"]

    def __init__(self):
        self.url = "https://ecoportal.su/conf.html"
        self.main_url = "https://ecoportal.su"

    def gather_data_sources(self):
        page = requests.get(
            url=self.url,
            headers={"User-Agent": "PostmanRuntime/7.41.1", "Accept": "*/*"},
        )
        if page.status_code != 200:
            return page.status_code
        soup = BeautifulSoup(page.text, features="lxml")
        self.sources = list(
            [
                elem["href"]
                for div in soup.find_all("div", class_="conf_list")
                for elem in div.find_all("a")
            ]
        )
        return True

    def get_data(self):
        for link in self.sources:
            page = requests.get(
                url=self.main_url + link,
                headers={"User-Agent": "PostmanRuntime/7.41.1", "Accept": "*/*"},
            )
            page.encoding = "utf-8"
            soup = BeautifulSoup(page.text, features="lxml")
            text = list(
                filter(
                    lambda i: i, soup.find("div", class_="conf_view").text.split("\n")
                )
            )
            date_i = 7 if text[1].startswith("с") else 2
            data = {
                "title": soup.find("div", class_="conf_view").find("h1").text,
                "date": " ".join(text[1].split()[:date_i])
                + " "
                + text[1].split()[date_i][:4],
                "place": text[1].split()[date_i][4:]
                + " "
                + " ".join(text[1].split()[date_i + 1 :]),
                "description": "\n".join(text[2:-2]),
                "link": text[-1].split()[-1],
            }
            yield data
