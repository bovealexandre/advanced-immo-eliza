import json
import random

import scrapy
from scrapy.http import Request

from scraper.scraper.items import HouseItem
from utils.func import get_nested_value


class ImmowebScraper(scrapy.Spider):
    name = "immowebscraper"
    allowed_domains = ["www.immoweb.be"]
    start_urls = [
        f"https://www.immoweb.be/fr/recherche/maison/a-vendre?countries=BE&page={x+1}&orderBy=newest"
        for x in range(0, 332)
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="card__title-link"]/@href').extract()
        for u in urls:
            yield Request(
                u,
                callback=self.parse_property,
            )

    def parse_property(self, response):
        jscript = response.xpath("/html/body/div[1]/div[1]/div[2]/script/text()")[
            0
        ].get()
        jscript = jscript.replace("window.classified = ", "").replace(";", "")
        jscript = json.loads(jscript)
        house = HouseItem()
        house["property_id"] = get_nested_value(jscript, ["id"])
        house["price"] = get_nested_value(jscript, ["price", "mainValue"], 0)
        house["type_of_property"] = get_nested_value(
            jscript, ["property", "type"], "unknown"
        )
        house["subtype_of_property"] = get_nested_value(
            jscript, ["property", "subtype"], "unknown"
        )
        house["bedrooms"] = get_nested_value(
            jscript, ["property", "bedroomCount"], None
        )
        house["bathrooms"] = get_nested_value(
            jscript, ["property", "bathroomCount"], None
        )
        house["region"] = get_nested_value(
            jscript, ["property", "location", "region"], "unknown"
        )
        house["province"] = get_nested_value(
            jscript, ["property", "location", "province"], "unknown"
        )
        house["postal_code"] = get_nested_value(
            jscript, ["property", "location", "postalCode"], None
        )
        house["floor"] = get_nested_value(
            jscript, ["property", "location", "floor"], None
        )
        house["living_area"] = get_nested_value(
            jscript, ["property", "netHabitableSurface"], None
        )
        house["state_of_property"] = get_nested_value(
            jscript, ["property", "building", "condition"], "unknown"
        )
        house["year_of_construction"] = get_nested_value(
            jscript, ["property", "building", "constructionYear"], None
        )
        house["facade_count"] = get_nested_value(
            jscript, ["property", "building", "facadeCount"], None
        )
        house["heating"] = get_nested_value(
            jscript, ["property", "energy", "heatingType"], "unknown"
        )
        house["kitchen"] = get_nested_value(
            jscript, ["property", "kitchen", "type"], "unknown"
        )
        house["epc_score"] = get_nested_value(
            jscript, ["transaction", "certificates", "epcScore"], "unknown"
        )
        house["garden"] = get_nested_value(jscript, ["property", "gardenSurface"], None)
        house["terrace"] = get_nested_value(
            jscript, ["property", "terraceSurface"], None
        )
        house["neighborhood_type"] = get_nested_value(
            jscript, ["property", "location", "type"], "unknown"
        )
        house["fireplace"] = get_nested_value(
            jscript, ["property", "fireplaceExists"], False
        )
        house["rooms"] = get_nested_value(jscript, ["property", "roomCount"], None)
        house["furnished"] = get_nested_value(
            jscript, ["transaction", "sale", "isFurnished"], False
        )
        house["pools"] = get_nested_value(
            jscript, ["property", "hasSwimmingPool"], False
        )
        yield house
