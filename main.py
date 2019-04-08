from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import win10toast as wtt
import GenerateUserAgents as genUA

class kissAnimeScraper:

    def __init__(self):
        pass

    def animeSearch(self, animeTitle):
        """
        Search for anime provided as argument: animeTitle
        """
        
        #path for chromdriver
        chromeDriver_PATH = "selenium/chromedriver.exe"

        #making browser headless (no ui pops up)
        chromeOptions = Options()
        chromeOptions.headless = True

        driver = webdriver.Chrome(chromeDriver_PATH, options = chromeOptions)

        #First letter in animeTitle stored to make search faster by modifying url
        animeTitle_firstLetter = animeTitle[0]

        #url for kissAnime anime search wepbage
        url = ""
        if (animeTitle_firstLetter.isalpha()):
            url = "https://kissanime.ru/AnimeList?c="+animeTitle_firstLetter.lower() + "&"
        else:
            url = "https://kissanime.ru/AnimeList?"

        pageNumber = 1

        #url of website which would be changing as the pages of anime are iterated through
        dynamicURL = url

        #while 'next' button is being clicked
        while True:

            driver.get(dynamicURL)

            animeListTable_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.barContent>div>table.listing"
            currentPage_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.pagination.pagination-left>ul.pager>li.current"
            lastButton_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.pagination.pagination-left>ul.pager>li:last-child"

            timeout = 10

            #Ensure page has loaded
            try:
                #Determine if anime list is present
                animeList_present = ec.presence_of_element_located((By.CSS_SELECTOR, animeListTable_cssSelector))
                WebDriverWait(driver, timeout).until(animeList_present)
            except TimeoutException:
                print("Timed out while waiting for anime list page")
            

            currentPage = driver.find_element_by_css_selector(currentPage_cssSelector).text

            last_Page = driver.find_element_by_css_selector(lastButton_cssSelector).text

            if (last_Page == currentPage): break


            animeName_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.barContent>div>table.listing>tbody>tr:not(.head)>td:first-child"

            animeNames = driver.find_elements_by_css_selector(animeName_cssSelector)
    
            matches = [anime.text.replace(" ","") for anime in animeNames if animeTitle in anime.text]

            if len(matches) > 0: #If possible matches extent to next page this won't find them. Fix this!
                print (matches)  #Possible fix: check if last anime on page ends the search. If not move to next page
                break

            #Move to next page
            pageNumber += 1
            dynamicURL = (url + "page={0}").format(pageNumber)


#Phase one partly completed.
#Some data may need to be stored. Consider database, text file, or other possible methods
#Additionally, check if scraping can be sped up. Checking if last anime on page ends the search could help here.
#On phase two, retrieve anime url for given anime and check for new additions

def main():

    #test object
    scraper = kissAnimeScraper()
    #test method call
    scraper.animeSearch("Naruto (Sub)") 

if __name__ == "__main__":

    main()