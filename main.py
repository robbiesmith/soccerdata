import data

def main():
    data.readLeagues()
    data.readTeams()
    data.writeLeagues()
    data.writeTeams()
    pass
    # read available pandas structure
    # read all team ids for leagues (if incomplete)
    # read all game ids for teams (if incomplete)
    # read all game data for games (if incomplete)

if __name__ == '__main__':
    main()