import pandas as pd
import requests
from bs4 import BeautifulSoup

leagues_data = None
teams_data = None
games_data = None

def readLeagues():
    global leagues_data
    try:
        leagues_data = pd.read_csv('leagues.csv')
    except:
# http://www.flashscore.com/soccer/england/premier-league/teams/
        leagues_data = pd.DataFrame([{'name':'EPL', 'path':'england/premier-league/'}])
    
def readTeams():
    global teams_data
    try:
        teams_data = pd.read_table('teams.csv')
    except:
        for index, row in leagues_data.iterrows():
            teams_data = pd.DataFrame(columns=['name', 'path'])
            r = requests.get('http://www.flashscore.com/soccer/' + row["path"] + "teams/")
            soup = BeautifulSoup(r.content, "lxml")
            teamtable = soup.find(id="tournament-page-participants")
            teams = teamtable.find("tbody").find_all("tr")
            for t in teams:
                path = row["path"] + t.find("a").get("href")
                name = t.find("a").text
                new_df = pd.DataFrame([{'name':name, 'path':path}], columns=['name', 'path'])
                teams_data = teams_data.append(new_df, ignore_index=True)
    
def readGames():
    try:
        games_table = pd.read_table('games.csv')
    except:
        pass
    
def writeLeagues():
    leagues_data.to_csv('leagues.csv')
    
def writeTeams():
    teams_data.to_csv('teams.csv')
    
def writeGames():
    games_data.to_csv('teams.csv')
    
def read():
    readLeagues()
    readTeams()
    readGames()
    
def write():
    writeLeagues()
    writeTeams()
    writeGames()
    