import pandas as pd

leagues_data = None
teams_data = None
games_data = None

def readLeagues():
    global leagues_data
    try:
        leagues_data = pd.read_csv('leagues.csv')
    except:
# http://www.flashscore.com/soccer/england/premier-league/teams/
        leagues_data = pd.DataFrame([{'name':'EPL', 'path':'england/premier-league'}])
    
def readTeams():
    global leagues_data
    try:
        teams_table = pd.read_table('teams.csv')
    except:
        pass
    
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
    