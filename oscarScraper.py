"""
Oscar Scraper
February 26th, 2018
Elliot Williams
"""
#%%
from selenium import webdriver as wb


def scrapeOscars(year="1998"):
    # Loads up Selenium WebDriver with Google Chrome
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
        print("Exception hit", e)
    driver.close()
    return speechResult
    
year = "1998"
speechResult = scrapeOscars(year)

#%%
import re

# Basic Stripping of Boilerplate from the speeches, leaving only useful information
speechResult = list(map(lambda x: x.replace("Watch the video", "").strip(), speechResult))
speechResult = list(map(lambda x: x.replace("""© Academy of Motion Picture Arts and Sciences
[Note: All winners are present except where noted; NOT all winners may have spoken.]""", "").strip(), speechResult))

'''
Helper function to parse regex on a list, analogous to sapply in R
(I prefer this because it prevents me from having to make ugly map lambda 
expressions in every line)
'''
def sapplyParseRegex(pattern, results, returnAfterMatch=False):
    match_list = list(map(lambda x: re.search(pattern, x), speechResult))
    if not returnAfterMatch:
        attr_list = list(map(lambda x: x.group(0) if x else None, match_list))
        return attr_list
    else:
        index_list = list(map(lambda x: x.start() if x else None, match_list))
        speech_index_list = zip(speechResult, index_list)
        return list(map(lambda x: x[0][x[1]:], speech_index_list))

# Utilizing Regex to get various measures of interest from the scraped text
year_data = sapplyParseRegex("(?<=Year: ).*", speechResult)
cat_data = sapplyParseRegex("(?<=Category: ).*", speechResult)
title_data = sapplyParseRegex("(?<=Film Title: ).*", speechResult)
winner_data = sapplyParseRegex("(?<=Winner: ).*", speechResult)
presenter_data = sapplyParseRegex("(?<=Presenter: ).*", speechResult)

# Returns the speech if it exists, otherwise returns the empty string
speech_data = sapplyParseRegex("[A-Z ]+:|(?<=\[Winner not present\.\])", 
                               speechResult, True)

#%%
# Writes result to csv
import csv
result_df = zip(year_data, cat_data, title_data, winner_data, presenter_data, speech_data)
with open(year+".csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Awards", "Category", "Film Title", "Winner", "Presenter", "Speech"])
    for row in result_df:
        writer.writerow(row)
