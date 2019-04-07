from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import win10toast as wtt
import GenerateProxyIP as genIP

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

        

    # def animeSearch(self, animeTitle):
    #     """
    #     Search for anime provided as argument: animeTitle
    #     """
        
    #     #url for kissAnime anime search wepbage
    #     url = "https://kissanime.ru/AnimeList"

    #     #setting user-agent to make request legitimate
    #     myheaders = {
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    #         'referer' : 'https://kissanime.ru/'
    #         }

    #     #ping website; make requests
    #     animeSearch_response = requests.get(url, headers = myheaders, proxies = genIP.getRandomProxyIPDict(), timeout = (6,20))
        
    #     #check if request was successful
    #     if (animeSearch_response.status_code != 200):
    #         print("status code not 200", "status code is", animeSearch_response.status_code)
    #         pass

    #     #create soup
    #     soupSearch = bs(animeSearch_response.content, 'html.parser')

    #     print(soupSearch)

    #     soupElements = soupSearch.select("div.pagination.pagination-left")        

    #     # for soupElement in soupElements:
    #     #     print("se: ", soupElement)

def main():

    #test object
    scraper = kissAnimeScraper()
    #test method call
    scraper.animeSearch("Mob psycho") 

if __name__ == "__main__":

    main()