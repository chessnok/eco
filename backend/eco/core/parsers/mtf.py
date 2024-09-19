from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver


class MTFParser:
    columns = ["date", "title", "text", "link"]

    def __init__(self):
        self.url = "https://www.m24.ru/rubrics/ecology/"
        self.main_url = "https://www.m24.ru/"

    def gather_data_sources(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        options.add_argument("--disable-web-security")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--headless=new")
        options.add_argument("--log-level=3")
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(options=options)
        self.driver = driver
        driver.get(self.url)
        self.sources = list(
            map(
                lambda elem: elem.get_attribute("href"),
                driver.find_elements(By.XPATH, ".//a[@class='b-effect2']"),
            )
        )
        return True

    def get_data(self):
        print(self.sources)
        for link in self.sources:
            self.driver.get(link)
            print(link)
            title = None
            date = ""
            try:
                date = self.driver.find_element(
                    By.XPATH, './/p[@class="b-material__date"]'
                ).text
            except NoSuchElementException:
                pass
            try:
                title = self.driver.find_element(
                    By.XPATH, './/div[@class="b-material-before-body"]/h1'
                ).text
            except NoSuchElementException:
                pass
            try:
                title = self.driver.find_element(
                    By.XPATH, './/div[@class="b-material__header"]'
                ).text
            except NoSuchElementException:
                pass
            if not title:
                continue
            try:
                text = self.driver.find_element(
                    By.XPATH, './/div[@class="b-material-body"]'
                ).text
            except NoSuchElementException:
                continue
            if "эко" not in text.lower() or "моск" not in text.lower():
                continue
            data = {
                "date": date,
                "title": title,
                "text": text,
                "link": link,
            }
            yield data
