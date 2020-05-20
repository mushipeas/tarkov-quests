# Tarkov Quests

Escape from Tarkov quest data scraped from the EFT wiki and reshaped for easier use.

## Scraper
Uses scrapy to parse all quest pages and gather necessary data.

Run with :

    scrapy crawl questspider -o quests_XX.X.json -o quests_XX.X.csv

## Latest File
Each significant patch will have its own json and csv file as part of this repo, so there's no need to unneccesarily scrape the site, unless you're drastically changing the data collection/format.

## Format

The output json contains the following information for all quests:

    "title" = str,
    "dealer" = str,
    "type" = str,
    "location" = List[str],
    "min_level" = int,
    "requirements" = List[str],
    "previous" = List[str],
    "leads_to" = List[str],
    "objectives" = List[str],
    "rewards" = List[str],
    "exp" = int

Any information that is not present on the wiki or has no value (ie. `previous` for initial quests) is set to `null`.
`min_level` and `exp` are zero when no value is provided in the wiki.