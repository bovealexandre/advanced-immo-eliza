# Immo Eliza

Immo Eliza is a Python project designed to scrape real estate data from Immoweb using Scrapy. The collected data is stored in a SQL database using psycopg2 and can be further utilized for training with CatBoost.

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:bovealexandre/advanced-immo-eliza.git
   ```
2. Navigate to the project directory:
   ```
   cd immo-eliza
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Scrape Immoweb

To initiate the scraping process using Scrapy, run the following command:

```
 python main.py

```

### Store Data in SQL Database

The collected data will be stored in a SQL database using psycopg2. Make sure to set up your database credentials before running the scraping process.

### Train with CatBoost

To train the collected data using CatBoost, refer to the specific training scripts or modules available in the project.

## Configuration

### Scrapy Settings

Adjust Scrapy settings and configurations in `settings.py` according to your scraping requirements.

## Contributing

Feel free to contribute by forking the repository and creating pull requests. For major changes, please open an issue first to discuss what you would like to change.
