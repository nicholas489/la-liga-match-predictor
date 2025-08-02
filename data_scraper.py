from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import datetime


def getUrlsFromHtmlDoc(document, endpoint):
    urls= []
    for link in document.find_all("a", href=True):
        hrefLink = link.get("href")
        if endpoint in hrefLink:
            urls.append(f"https://fbref.com{hrefLink}")
    return urls

def getMatchDataFromPreviousYears(driver, standingsUrl):
    allMatches = []
    years = [num for num in range(datetime.date.today().year, datetime.date.today().year - 3, -1)]
    
    for year in years:
        driver.get(standingsUrl)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        standingsTable = soup.select("table.stats_table")[0]
        
        teamUrls = getUrlsFromHtmlDoc(standingsTable, "/squads/")
        
        previousSeason = soup.select("a.prev")[0].get("href")
        standingsUrl = f"https://fbref.com{previousSeason}"
        
        
        for teamUrl in teamUrls:
            teamUrlArray = teamUrl.split("/")
            teamName = teamUrlArray[len(teamUrlArray) - 1].replace("-Stats", "")
            
            driver.get(teamUrl)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            matches = pd.read_html(StringIO(soup.prettify()), match="Scores & Fixtures")[0]
            
            shootingsStatsUrls = getUrlsFromHtmlDoc(soup, "/all_comps/shooting/")    
            shootingsStatsUrl = shootingsStatsUrls[0]
            driver.get(shootingsStatsUrl)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            shooting = pd.read_html(StringIO(soup.prettify()), match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()
            
            try:
                teamData = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
            except ValueError:
                continue
            
            teamData = teamData[teamData["Comp"] == "La Liga"]
            teamData["Season"] = year
            teamData["Team"] = teamName
            
            allMatches.append(teamData)
            time.sleep(1)
            
    return allMatches
        
    

if __name__ == "__main__":
    start = time.time()
    
    standingsUrl = "https://fbref.com/en/comps/12/La-Liga-Stats"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    allMatchData = getMatchDataFromPreviousYears(driver, standingsUrl)
    
    matchDataFrame = pd.concat(allMatchData)
    matchDataFrame.columns = [column.lower() for column in matchDataFrame.columns]
    matchDataFrame.to_csv("matches.csv")
    
    end = time.time()
    print(f"Program took {end - start} seconds to run till completion")