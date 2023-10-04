from Games import game, no_op, blockPrint, enablePrint, best_of
from random import choice
from colorama import Fore
from load_pickle import season_wipe

def print_standings(TEAMS,universal=False):
    enablePrint()
    print(Fore.GREEN + f"ROBIN STANDINGS" + Fore.RESET)

    idx = 0
    TEAMS.sort(key=lambda x: (x.wins, x.margin), reverse=True)
    for team in TEAMS:
        idx += 1
        team.seed = idx
        if team.margin <= 0:
            sign = ''
        else:
            sign = '+'
        print(f"{idx}. {team.name} ({team.wins}-{team.losses}), {sign}{round(team.margin,2)}")

def round_robin(TEAMS,r,qualify_range,amp=4,alt_qualify_range = None):

    SIZE = len(TEAMS)
    for k in range(r):
        for i in range(SIZE):
            for j in range(i + 1, SIZE):
                team1 = TEAMS[i]
                team2 = TEAMS[j]
                game(team1, team2,amp)
        if k == r-1:
            TEAMS.sort(key=lambda x: (x.wins, x.margin), reverse=True)
            print_standings(TEAMS, True)
    if qualify_range == 1:
        return TEAMS[0]
    else:
        bebop = []
        bebop2 = []
        for q in range(qualify_range):
            bubba = TEAMS[q]
            bebop.append(bubba)
        if alt_qualify_range:
            for q in range(qualify_range, qualify_range+alt_qualify_range):
                bubba2 = TEAMS[q]
                bebop2.append(bubba2)
            return bebop, bebop2
        else:
            return bebop

def chain(teams):
    size = len(teams)
    winner = best_of(teams[size], teams[size-1], 100, win_by=10)
    for i in range(size):
        winner = best_of(winner, teams[size-i], 100+i, win_by=10)
    return winner