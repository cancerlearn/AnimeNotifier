from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import win10toast as wtt
import GenerateUserAgents as genUA

class kissAnimeScraper:

    __instance = None

    @staticmethod
    def getInstance():
        """
        Static access method.
        This simply returns the instance of the class that has been created.
        """
        if kissAnimeScraper.__instance == None:
            kissAnimeScraper()

        return kissAnimeScraper.__instance


    def __init__(self):

        if kissAnimeScraper.__instance != None:
            raise Exception("This is a singleton class!")
        else:
            kissAnimeScraper.__instance = self

        #path for chromdriver
        self.chromeDriver_PATH = "selenium/chromedriver.exe"

        #making browser headless (no ui pops up)
        self.chromeOptions = Options()
        self.chromeOptions.headless = True
    
        self.driver = webdriver.Chrome(self.chromeDriver_PATH, options = self.chromeOptions)


    def animeSearch(self, animeTitle):
        """
        Search for anime provided as argument: animeTitle
        """

        matches = [] #list to hold matches found for the animeTitle given

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

            self.driver.get(dynamicURL)

            animeListTable_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.barContent>div>table.listing"
            currentPage_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.pagination.pagination-left>ul.pager>li.current"
            lastButton_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.pagination.pagination-left>ul.pager>li:last-child"

            timeout = 20

            #Ensure page has loaded
            try:
                #Determine if anime list is present
                animeList_present = ec.presence_of_element_located((By.CSS_SELECTOR, animeListTable_cssSelector))
                WebDriverWait(self.driver, timeout).until(animeList_present)
            except TimeoutException:
                print("Timed out while waiting for anime list page.")
            

            currentPage = self.driver.find_element_by_css_selector(currentPage_cssSelector).text

            last_Page = self.driver.find_element_by_css_selector(lastButton_cssSelector).text

            if (last_Page == currentPage): break


            animeName_cssSelector = "div#container>div#leftside>div.bigBarContainer>div.barContent>div>table.listing>tbody>tr:not(.head)>td:first-child"

            animeNames = self.driver.find_elements_by_css_selector(animeName_cssSelector)
    
            matches += [anime.text.strip() for anime in animeNames if animeTitle in anime.text]

            if len(matches) > 0: #If possible matches extend to next page this won't find them. Fix this!
                print (matches)  #Possible fix: check if last anime on page ends the search. If not move to next page
                break

            #Move to next page
            pageNumber += 1
            dynamicURL = (url + "page={0}").format(pageNumber)

        links = [self.driver.find_element_by_link_text(anime).get_attribute("href") for anime in matches]
        return links


    def getLatestEpisode(self, link):
        """
        Find latest episode given the *url*
        """

        self.driver.get(link)

        animeEpisodesTable_cssSelector = "#leftside>div:nth-child(4)>div.barContent.episodeList>div:nth-child(2)>table"
        animeEpisodes_cssSelector = "#leftside>div:nth-child(4)>div.barContent.episodeList>div:nth-child(2)>table>tbody>tr:nth-child(n+3):nth-child(n)>td:nth-child(1)"

        timeout = 20

        try:
            #Determine if anime list is present
            animeEpisodes_present = ec.presence_of_element_located((By.CSS_SELECTOR, animeEpisodesTable_cssSelector))
            WebDriverWait(self.driver, timeout).until(animeEpisodes_present)
        except TimeoutException:
            print("Timed out while waiting for anime episodes list page.")

        episodeList = self.driver.find_elements_by_css_selector(animeEpisodes_cssSelector)
        
        episodes = [int(episode.text.split("Episode")[1]) for episode in episodeList]

        return episodes




#Dated: A month ago from today (11th May, 2019)
#Phase one partly completed.
#Some data may need to be stored. Consider database, text file, or other possible methods
#Additionally, check if scraping can be sped up. Checking if last anime on page ends the search could help here.
#On phase two, retrieve anime url for given anime and check for new additions

#Dated: 11th May, 2019
#Phasde one complete. Current state providing multiple matches is acceptable.
#   Provided a GUI is created, the matches found would be used to zero down on what the user wants.
#Phase two (retreiveing anime url) partially completed
#Consider database, text file, or other alternatives for keeping track of latest episodes to notify on new releases
#Start GUI when possible

def main():

    #test object
    scraper = kissAnimeScraper()
    #test method call
    link = scraper.animeSearch("One Punch Man")

    print(scraper.getLatestEpisode(link[0]))

if __name__ == "__main__":

    main()