# Oscar Scraper

This Python 3 script scrapes the speeches (and related metadata) for the Oscars held
on a given year, by scraping [this site](http://aaspeechesdb.oscars.org) using
Selenium.

## Setup

To set this up on your local machine, you need to install ChromeDriver on the
computer on which you're running the script, and then you need to install the
Selenium Python package.

### Directions
* [For Windows](https://stackoverflow.com/questions/33150351/how-do-i-install-chromedriver-on-windows-10-and-run-selenium-tests-with-chrome)
* [For Mac](https://www.kenst.com/2015/03/installing-chromedriver-on-mac-osx/) (or just run `brew install chromedriver`)
* [For Ubuntu](https://christopher.su/2015/selenium-chromedriver-ubuntu/)

### Installing Selenium Python Package

Run `pip3 install selenium` and you should be good to go.

## Running the Script

Run `python oscarScraper.py [year]` to scrape the oscar awards for that
particular year. The script will save all speech data for that year within
`[year].csv` in the same directory.

If you want to scrape multiple years, run `python oscarScraper.py [start_year] [end_year]`,
and the program will scrape from the start year to the end year inclusive.
