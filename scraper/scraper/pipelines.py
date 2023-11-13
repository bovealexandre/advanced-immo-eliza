# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline:
    def __init__(self):
        try:
            ## Connection Details
            hostname = "localhost"
            username = "postgres"
            password = "postgres"
            database = "properties"

            self.connection = psycopg2.connect(
                host=hostname, user=username, password=password, database=database
            )
            self.cur = self.connection.cursor()

        except psycopg2.OperationalError as e:
            # Handle the connection error, e.g., log the error message
            print(f"Error connecting to the database: {e}")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        try:
            self.cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    property_id INT PRIMARY KEY,
                    type_of_property VARCHAR(255),
                    subtype_of_property VARCHAR(255),
                    bedrooms INT,
                    bathrooms INT,
                    region VARCHAR(255),
                    province VARCHAR(255),
                    postal_code VARCHAR(255),
                    floor INT,
                    living_area INT,
                    state_of_property VARCHAR(255),
                    year_of_construction INT,
                    facade_count INT,
                    heating VARCHAR(255),
                    kitchen VARCHAR(255),
                    epc_score VARCHAR(255),
                    price INT,
                    garden INT,
                    terrace INT,
                    neighborhood_type VARCHAR(255),
                    fireplace BOOLEAN,
                    rooms INT,
                    furnished BOOLEAN,
                    pools BOOLEAN
                )
                """
            )
            self.connection.commit()
        except psycopg2.Error as e:
            spider.logger.error(f"Error creating table: {e}")

    def process_item(self, item, spider):
        self.cur.execute(
            "SELECT * FROM sales WHERE property_id = %s", (item["property_id"],)
        )
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Item already in database: %s" % item["property_id"])

        elif item["price"] is None:
            spider.logger.warn("Item has no price!")
        else:
            self.cur.execute(
                """
            INSERT INTO sales (
                property_id,
                type_of_property,
                subtype_of_property,
                bedrooms,
                bathrooms,
                region,
                province,
                postal_code,
                floor,
                living_area,
                state_of_property,
                year_of_construction,
                facade_count,
                heating,
                kitchen,
                epc_score,
                price,
                terrace,
                garden,
                neighborhood_type,
                fireplace,
                rooms,
                furnished,
                pools
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
                (
                    item["property_id"],
                    item["type_of_property"],
                    item["subtype_of_property"],
                    item["bedrooms"],
                    item["bathrooms"],
                    item["region"],
                    item["province"],
                    item["postal_code"],
                    item["floor"],
                    item["living_area"],
                    item["state_of_property"],
                    item["year_of_construction"],
                    item["facade_count"],
                    item["heating"],
                    item["kitchen"],
                    item["epc_score"],
                    item["price"],
                    item["terrace"],
                    item["garden"],
                    item["neighborhood_type"],
                    item["fireplace"],
                    item["rooms"],
                    item["furnished"],
                    item["pools"],
                ),
            )

            self.connection.commit()
        return item

    def close_spider(self, spider):
        try:
            self.cur.close()
            self.connection.close()
        except psycopg2.Error as e:
            spider.logger.error(f"Error closing the database connection: {e}")
