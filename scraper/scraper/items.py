# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class HouseItem(Item):
    property_id = Field()
    type_of_property = Field()
    subtype_of_property = Field()
    rooms = Field()
    bedrooms = Field()
    bathrooms = Field()
    region = Field()
    province = Field()
    postal_code = Field()
    floor = Field()
    living_area = Field()
    state_of_property = Field()
    year_of_construction = Field()
    facade_count = Field()
    heating = Field()
    kitchen = Field()
    epc_score = Field()
    price = Field()
    garden = Field()
    terrace = Field()
    neighborhood_type = Field()
    fireplace = Field()
    furnished = Field()
    pools = Field()
