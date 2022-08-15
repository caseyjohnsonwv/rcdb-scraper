# rcdb-scraper

Using Selenium and Python to scrape roller coaster data from the official [Roller Coaster Database](http://rcdb.com/).

## Quickstart

Assuming you have Docker installed and your daemon is running:

1. Clone this repo, setup a virtual env, etc etc
2. `docker-compose up --abort-on-container-exit --build`

Sample CSV output:
```
1,Raptor,Cedar Point
2,Texas Giant,Six Flags Over Texas
3,Demon,Six Flags Great America
```