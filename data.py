import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import re

leagues_data = None
teams_data = None
games_data = None

def readLeagues():
    global leagues_data
    try:
        leagues_data = pd.read_csv('leagues.csv', index_col=0)
    except:
        leagues_data = pd.DataFrame([{'name':'EPL', 'path':'/england/premier-league'}])
    
def readTeams():
# http://www.flashscore.com/soccer/england/premier-league/teams/
    global teams_data
    try:
        teams_data = pd.read_csv('teams.csv', index_col=0)
    except:
        for index, row in leagues_data.iterrows():
            teams_data = pd.DataFrame(columns=['name', 'path', 'id'])
            r = requests.get('http://www.flashscore.com/soccer' + row["path"] + "/teams")
            soup = BeautifulSoup(r.content, "lxml")
            teamtable = soup.find(id="tournament-page-participants")
            teams = teamtable.find("tbody").find_all("tr")
            for t in teams:
                path = row["path"] + t.find("a").get("href")
                id = path.split("/")[-1] 
                name = t.find("a").text
                new_df = pd.DataFrame([{'name':name, 'path':path, 'id':id}], columns=['name', 'path', 'id'])
                teams_data = teams_data.append(new_df, ignore_index=True)
    

def readGameIds(league_id):
    global games_data
    try:
        driver = webdriver.Chrome()
#        games_data = pd.read_csv('games.csv', index_col=0)
#        for index, row in games_data.iterrows():
#            game_id = row['game_id']
        columns = ['game_id', 'h_id', 'h_score', 'a_id', 'a_score', 'h_odds', 'tie_odds', 'a_odds']
        games_data = pd.DataFrame(columns=columns)
        driver.get("http://www.flashscore.com/soccer" + league_id + "/results")
        # would be better to use WebDriverWait and EC
        while True:
            time.sleep(5)
            more = driver.find_element_by_id("tournament-page-results-more")
            if not more.get_attribute("style"):
                a = more.find_element_by_tag_name('a')
                a.click()
                continue
            break
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
        games = soup.find_all('tr', id=re.compile("^g_1_"))
        for game in games:
            game_id = game.get('id').replace("g_1_", "")
            new_df = pd.DataFrame([{'game_id':game_id,'h_id':None, 'h_score':None, 'a_id':None, 'a_score':None, 'h_odds':None, 'tie_odds':None, 'a_odds':None}], columns=columns)
            games_data = games_data.append(new_df, ignore_index=True)
    finally:
        driver.close()
    pass

def readAllGames():
    global games_data
    games_data = pd.read_csv('games.csv', index_col=0)
    for index, row in games_data.iterrows():
        if pd.isnull(row['h_id']):
            readGame(row['game_id'])
        
def readGame(game_id):
    global games_data
    try:
        driver = webdriver.Chrome()
#        games_data = pd.read_csv('games.csv', index_col=0)
#        for index, row in games_data.iterrows():
#            game_id = row['game_id']
        columns = ['game_id', 'h_id', 'h_score', 'a_id', 'a_score', 'h_odds', 'tie_odds', 'a_odds']
#        games_data = pd.DataFrame(columns=columns)

#        game_id = 'SGPa5fvr' # temporarily hard-coded
#            from selenium.webdriver.common.by import By
#            from selenium.webdriver.support.ui import WebDriverWait
#            from selenium.webdriver.support import expected_conditions as EC

        try:
            driver.get("http://www.flashscore.com/match/" + game_id + "/#match-summary")
            # would be better to use WebDriverWait and EC
            time.sleep(2)
            source = driver.page_source
            soup = BeautifulSoup(source, "lxml")
            scores = soup.find(class_="current-result").find_all(class_="scoreboard")
            hometeam = soup.find(class_="tname-home")
            hometeam_id = hometeam.find("a").get("onclick").split("/")[-1].split("'")[0]
            hometeam_score = scores[0].text
            awayteam = soup.find(class_="tname-away")
            awayteam_id = awayteam.find("a").get("onclick").split("/")[-1].split("'")[0]
            awayteam_score = scores[1].text
            hometeam_odds = soup.find(id="default-odds").find(class_="o_1").find(class_="odds-wrap").text
            awayteam_odds = soup.find(id="default-odds").find(class_="o_2").find(class_="odds-wrap").text
            tie_odds = soup.find(id="default-odds").find(class_="o_0").find(class_="odds-wrap").text
            new_df = pd.DataFrame([{'game_id':game_id,'h_id':hometeam_id, 'h_score':hometeam_score, 'a_id':awayteam_id, 'a_score':awayteam_score, 'h_odds':hometeam_odds, 'tie_odds':tie_odds, 'a_odds':awayteam_odds}], columns=columns)
            games_data = games_data.append(new_df, ignore_index=True)
        except:
            pass
    finally:
        driver.quit()
    
def writeLeagues():
    leagues_data.to_csv('leagues.csv')
    
def writeTeams():
    teams_data.to_csv('teams.csv')
    
def writeGames():
    games_data.to_csv('games.csv')
   
    