"""
Elliot Williams
Oscar Award Speeches Scraper
Computer Networks w Prof. Manfredi
May 11th, 2018
"""

from selenium import webdriver as wb
import sys
import re
import csv

class OscarScraper:

    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year   = end_year

        print("Welcome to my Oscar Scraper program")
        if start_year == end_year:
            print("It seems we're scraping from {}\n\n".format(start_year))
        else:
            print("It seems we're scraping from {} to {}\n\n".format(start_year, end_year))

        for year in range(start_year, end_year+1):
            print("Collecting data using Chrome Slave for year {}".format(year))
            self.year = str(year)
            speechResult = self.scrapeOscars(year)
            print("Parsing + Writing to csv data for year {}".format(year))
            self.parseAndWriteData(speechResult)


    '''
    This function directs the slave Chrome browser to load the
    AA speeches site, load the results corresponding to the year we're
    interested in, click the link for each category in that year, and scrape
    all of the speech data text from each result we click onself.

    Input:
        year -- year of interest for scraping : int

    Output:
        Returns an array of speech results, to be parsed by parseAndWriteData
    '''
    def scrapeOscars(self, year=1998):
        year = str(year)
        # Loads up Selenium's WebDriver implementation for Google Chrome
        driver = wb.Chrome()

        try:
            # Directs the slave browser to the Oscars DB Site
            url = "http://aaspeechesdb.oscars.org/"
            driver.get(url)

            # Selects the Input Box corresponding to the Awards Year
            year_xpath = '//input[@id="QI0"]'
            r = driver.find_element_by_xpath(year_xpath)
            r.send_keys(year)

            # Finds the Search button, and clicks it
            driver.find_element_by_xpath("//input[@id='body_SearchButton']").click()

            # Gets all of the links to each speech made at the Oscars that year
            speechLinkElements = driver.find_elements_by_xpath("//div[@id='main']/div/p")

            # Scrapes the speech data and metadata for each link
            speechResult = []
            for i in range(0, len(speechLinkElements)):
                # Finds the link to get to speech, and clicks on it
                speechLinkElements[i].find_element_by_tag_name("a").click()
                # Finds the div containing all relevant text, and scrapes it
                yearData = driver.find_element_by_xpath("//div[@class='fullModule2 fullContainer']").text
                # Appends the data to the speechResult list
                speechResult.append(yearData)
                # Makes the driver go back, and repeats for a different link
                driver.back()
                # Rescrapes all the links (necessary to keep elements not 'stale')
                speechLinkElements = driver.find_elements_by_xpath("//div[@id='main']/div/p")

        except Exception as e:
            print("Exception hit when scraping {}".format(year), e)
            driver.close()
            sys.exit(1)

        driver.close()
        return speechResult

    '''
    Helper function to parse regex on a list, analogous to sapply in R
    (I prefer this because it prevents me from having to make ugly map lambda
    expressions in every line)
    '''
    def sapplyParseRegex(self, pattern, speechResult, returnAfterMatch=False):
        match_list = list(map(lambda x: re.search(pattern, x), speechResult))
        if not returnAfterMatch:
            attr_list = list(map(lambda x: x.group(0) if x else None, match_list))
            return attr_list
        else:
            index_list = list(map(lambda x: x.start() if x else None, match_list))
            speech_index_list = zip(speechResult, index_list)
            return list(map(lambda x: x[0][x[1]:], speech_index_list))

    '''
    This function parses the speechResult data returned from `scrapeOscars`
    into the various data points of interest, and writes the produced data
    to csv file format.
    '''
    def parseAndWriteData(self, speechResult):
        # Basic Stripping of Boilerplate from the speeches, leaving only useful information
        speechResult = list(map(lambda x:
            x.replace("Watch the video", "").strip(), speechResult))
        speechResult = list(map(lambda x:
            x.replace("""© Academy of Motion Picture Arts and Sciences
        [Note: All winners are present except where noted; NOT all winners may have spoken.]""",
            "").strip(), speechResult))

        # Utilizing Regex to get various data of interest from the results
        year_data = self.sapplyParseRegex("(?<=Year: ).*",
            speechResult)
        cat_data = self.sapplyParseRegex("(?<=Category: ).*",
            speechResult)
        title_data = self.sapplyParseRegex("(?<=Film Title: ).*",
            speechResult)
        winner_data = self.sapplyParseRegex("(?<=Winner: ).*",
            speechResult)
        presenter_data = self.sapplyParseRegex("(?<=Presenter: ).*",
            speechResult)

        # Returns the speech if it exists, otherwise returns the empty string
        speech_data = self.sapplyParseRegex("[A-Z ]+:|(?<=\[Winner not present\.\])",
                                       speechResult, True)

        # Writes result to csv
        result_df = zip(year_data, cat_data, title_data, winner_data,
                        presenter_data, speech_data)
        with open(self.year+".csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Awards", "Category", "Film Title",
                             "Winner", "Presenter", "Speech"])
            for row in result_df:
                writer.writerow(row)

if __name__ == "__main__":
    # If there is a single command line argument, that's the year we want
    if len(sys.argv) == 2:
        year = int(sys.argv[1])
        OscarScraper(year, year)

    # If there are two command line arguments, that's the year range we want
    if len(sys.argv) == 3:
        start = int(sys.argv[1])
        end   = int(sys.argv[2])
        OscarScraper(start, end)

    # Otherwise, let's scrape 1998 by default
    if len(sys.argv) == 1:
        OscarScraper(1998)
