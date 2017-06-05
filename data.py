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
        leagues_data = pd.DataFrame([{'name':'EPL', 'path':'/england/premier-league'}])
    
def readTeams():
# http://www.flashscore.com/soccer/england/premier-league/teams/
    global teams_data
    try:
        raise
        teams_data = pd.read_table('teams.csv')
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
    
def readGames():
# the best way to get all may be http://www.flashscore.com/soccer/england/premier-league/results/ with 'Show more matches' selected
# http://www.flashscore.com/match/SGPa5fvr/#match-summary
# class=tname-home class=tname a.text
# id-event_detail_current_result
# class=scoreboard
# class=tname-away class=tname a.text

# id default-odds
# class kx o_1 span class odds-wrap .text
# class kx o_0 span class odds-wrap .text
# class kx o_2 span class odds-wrap .text
    global games_data
    try:
        raise
        games_data = pd.read_table('games.csv')
    except:
        games_data = pd.DataFrame(columns=['h_id', 'h_score', 'a_id', 'a_score', 'h_odds', 'tie_odds', 'a_odds'])
        r = requests.get('http://www.flashscore.com/match/SGPa5fvr/#match-summary')
        soup = BeautifulSoup(r.content, "lxml")
        scores = soup.find(class_="current-result").find_all(class_="scoreboard")
        hometeam = soup.find(class_="tname-home")
        hometeam_id = hometeam.find("a").get("onclick").split("/")[-1].split("'")[0]
        hometeam_score = scores[0].text
        awayteam = soup.find(class_="tname-away")
        awayteam_id = awayteam.find("a").get("onclick").split("/")[-1].split("'")[0]
        awayteam_score = scores[1].text
        print(r.content)
        return

        hometeam_odds = soup.find(class_="o_1").find(class_="odds-wrap").text
        awayteam_odds = soup.find(class_="o_2").find(class_="odds-wrap").text
        tie_odds = soup.find(class_="o_0").find(class_="odds-wrap").text
        print(tie_odds)
        return
        teamtable = soup.find(id="tournament-page-participants")
        teams = teamtable.find("tbody").find_all("tr")
        for t in teams:
            path = row["path"] + t.find("a").get("href")
            name = t.find("a").text
            new_df = pd.DataFrame([{'name':name, 'path':path}], columns=['name', 'path'])
            teams_data = teams_data.append(new_df, ignore_index=True)
    
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
    