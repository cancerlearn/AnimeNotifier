from bs4 import BeautifulSoup as bs
import requests as rs
import random as rnd

def getAllUserAgents(browser):
    """
    This method generates a list of all user agents for the browser passed as an argument,
    from the webpage "https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/".

    This list is returned.

    Possible browser arguments: 'chrome', 'internet explorer', 'firefox', 'opera-mini', 'android-browser', 'opera', 'uc-browser', 'safari', 'outlook'
    """

    #Dictionary for 'browser'(key) to 'userAgents url'
    browsers = {
        "chrome" : "https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/",
        "internet explorer" : "https://developers.whatismybrowser.com/useragents/explore/software_name/internet-explorer/",
        "firefox" : "https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/",
        "opera-mini" : "https://developers.whatismybrowser.com/useragents/explore/software_name/opera-mini/",
        "android-browser" : "https://developers.whatismybrowser.com/useragents/explore/software_name/android-browser/",
        "opera" : "https://developers.whatismybrowser.com/useragents/explore/software_name/opera/",
        "uc-browser" : "https://developers.whatismybrowser.com/useragents/explore/software_name/uc-browser/",
        "safari" : "https://developers.whatismybrowser.com/useragents/explore/software_name/safari/",
        "outlook" : "https://developers.whatismybrowser.com/useragents/explore/software_name/outlook/"
        }

    #List of all chrome user agents to be returned
    useragent_List = []

    #headers for this request
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'referer' : 'https://developers.whatismybrowser.com/useragents/explore/'
    }
    
    pageNumber = 0

    wpgURL = browsers[browser.lower()]

    #Iterating through pages of chrom user agents
    while True:

        #webpage response
        wpg = rs.get(wpgURL, headers = headers, timeout = 5)

        #If end of pages has been reached
        if (wpg.status_code == 404):
            break

        #If pages have not endend, check if request was successful
        if (wpg.status_code != 200):
            print("status code not 200", "status code is", wpg.status_code)
            return

        #html-parsed "soup" of page content
        useragents_Soup = bs(wpg.content, 'html.parser')

        #rows of data of user agents
        userAgentTable = useragents_Soup.select("div.corset>table.table-useragents>tbody>tr")

        #Iterating through rows in table containing data of user agents
        for row in userAgentTable:
            
            #Add user agent to list
            useragent_List.append(row.select_one("td.useragent>a").string)

        #Move to next page
        pageNumber += 1
        wpgURL = wpgURL + "{0}".format(pageNumber)

    return useragent_List

def getRandomUserAgent(browser):
    """
    This method returns a random user agent for the browser specified as an argument

    Possible browser arguments: 'chrome', 'internet explorer', 'firefox', 'opera-mini', 'android-browser', 'opera', 'uc-browser', 'safari', 'outlook'
    """

    useragent_List = getAllUserAgents(browser)
    return useragent_List[rnd.randint(0, len(useragent_List)-1)]