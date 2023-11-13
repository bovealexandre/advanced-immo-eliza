import os

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from machine_learning.main import machine_learning
from scraper.scraper.spiders.immowebscraper import ImmowebScraper

if __name__ == "__main__":
    settings = Settings()
    os.environ["SCRAPY_SETTINGS_MODULE"] = "scraper.scraper.settings"
    settings_module_path = os.environ["SCRAPY_SETTINGS_MODULE"]
    settings.setmodule(settings_module_path, priority="project")
    process = CrawlerProcess(settings)
    process.crawl(ImmowebScraper)
    process.start()

    machine_learning()
