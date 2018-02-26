# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



#%%
from selenium import webdriver as wb
import time


# Loads up Selenium WebDriver with Google Chrome
driver = wb.Chrome()

try:
    # Directs the slave browser to the Oscars DB Site
    url = "http://aaspeechesdb.oscars.org/"
    driver.get(url)
    
    # Selects the Input Box corresponding to the Awards Year
    year_xpath = '//input[@id="QI0"]'
    r = driver.find_element_by_xpath(year_xpath)
    r.send_keys("1998")
 
    driver.find_element_by_xpath("//input[@id='body_SearchButton']").click()
    
    speechLinkElements = driver.find_elements_by_xpath("//div[@id='main']/div/p")
#    awardText = list(map(lambda x : x.text, speechLinkElements))
    
    
    speechResult = []
    for i in range(0, len(speechLinkElements)):
        speechLinkElements[i].find_element_by_tag_name("a").click()
        yearData = driver.find_element_by_xpath("//div[@class='fullModule2 fullContainer']").text
        speechResult.append(yearData)
        time.sleep(1)
        driver.back()
        speechLinkElements = driver.find_elements_by_xpath("//div[@id='main']/div/p")

    time.sleep(15)
except Exception as e:
    print("Exception hit", e)
driver.close()