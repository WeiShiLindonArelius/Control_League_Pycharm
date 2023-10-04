from random import randint, choice, seed
from stat_functions import series_test
import sys
from colorama import Fore, Back, Style

def nothing():
    pass

def no_op(args):
    pass

def blockPrint():
    sys.stdout = nothing()

def enablePrint():
    sys.stdout = sys.__stdout__

PLAY_BY_PLAY= False
TEST_OUTPUT = False




def game(team1, team2, amp=4, type_of='None'):
    # enable / disable to have a constant / non-constant amp
    if amp != 4:
        amp = 4

    for ply in team1.players:
        ply.no_power = 0
        ply.is_alive = True
    for ply in team2.players:
        ply.no_power = 0
        ply.is_alive = True
    def true_game(team1, team2):
        TESSERACT = 0
        length = 56
        length *= amp
        length += 1
        for tick in range(1, length):
            living_team1 = []
            living_team2 = []
            yta_team1 = []
            yta_team2 = []
            for pl in team1.players:
                if pl.is_alive:
                    living_team1.append(pl)
                    yta_team1.append(pl)
                elif pl.countdown == 0:
                    pl.respawn()
                    living_team1.append(pl)
                    yta_team1.append(pl)
                else:
                    pl.countdown -= 1

            for pl in team2.players:
                if pl.is_alive:
                    living_team2.append(pl)
                    yta_team2.append(pl)
                elif pl.countdown == 0:
                    pl.respawn()
                    living_team2.append(pl)
                    yta_team2.append(pl)
                else:
                    pl.countdown -= 1

            sub_count = 0
            while True:
                if not living_team1 and not living_team2:
                    break
                coin = randint(0, 999)
                if coin%2 == 0:
                    #TEAM1 ATTACKING
                    if yta_team1:
                        attacker = choice(yta_team1)
                        yta_team1.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            if living_team2:
                                defender = choice(living_team2)
                                attacker.attack(defender)
                                if not defender.is_alive:
                                    living_team2.remove(defender)
                                    TESSERACT += abs(3*defender.health)
                            else:
                                attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT += attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    elif yta_team2:
                        #TEAM2 DELAYED ATTACK
                        attacker = choice(yta_team2)
                        yta_team2.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT -= attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    else:
                        break
                elif coin%2 == 1:
                    #TEAM2 ATTACKING
                    if yta_team2:
                        attacker = choice(yta_team2)
                        yta_team2.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            if living_team1:
                                defender = choice(living_team1)
                                attacker.attack(defender)
                                if not defender.is_alive:
                                    living_team1.remove(defender)
                                    TESSERACT -= abs(3*defender.health)
                            else:
                                attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT -= attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    elif yta_team1:
                        #TEAM1 DELAYED ATTACK
                        attacker = choice(yta_team1)
                        yta_team1.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT += attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    else:
                        break
                sub_count += 1
        if TESSERACT > 0:
            team1.wins += 1
            team1.margin += abs(round(TESSERACT,2))
            team2.losses += 1
            team2.margin -= abs(round(TESSERACT,2))
            return team1
        else:
            team1.losses += 1
            team1.margin -= abs(round(TESSERACT,2))
            team2.wins += 1
            team2.margin += abs(round(TESSERACT,2))
            return team2
    cc_coin = randint(1,999)
    if cc_coin%2 == 0:
        result = true_game(team1,team2)
    else:
        result = true_game(team2,team1)

    for player in team2.players:
        player.games_played['This-Season'] += 1
    for player in team1.players:
        player.games_played['This-Season'] += 1
    return result

def best_of(team1,team2,thresh,amp=4,both_return=False,win_by=1,test_output=False,is_uni=False):


    blockPrint()
    team1_wins = 0
    team2_wins = 0
    game_count = 0

    while True:
        winner = game(team1, team2, amp)
        team1_wins += 1 if winner == team1 else 0
        team2_wins += 1 if winner == team2 else 0
        game_count += 1
        if team1_wins == thresh or team2_wins == thresh:
            break

    while abs(team1_wins - team2_wins) < win_by:
        winner = game(team1, team2, amp)
        team1_wins += 1 if winner == team1 else 0
        team2_wins += 1 if winner == team2 else 0
        game_count += 1
        if game_count > thresh*35:
            win_by -= 1

    for player in team2.players:
        player.games_played['Playoffs'] += 1
    for player in team1.players:
        player.games_played['Playoffs'] += 1

    if team1_wins > team2_wins:
        enablePrint()
        if team1.seed != -1:
            print(Back.RED + Fore.BLACK +
                f"{team1.name}({team1.seed}) defeats {team2.name}({team2.seed}) by a score of {team1_wins}-{team2_wins}." + Back.RESET + Fore.RESET)
        else:
            print(Back.RED + Fore.BLACK +
                f"{team1.name} defeats {team2.name} by a score of {team1_wins}-{team2_wins}." + Back.RESET + Fore.RESET)
        if test_output:
            print(series_test(team1_wins, team2_wins))

        if is_uni:
            team1.accolades['Uni-Playoff-Wins'] += 1
        if not both_return:
            return team1
        else:
            return team1, team2
    else:
        enablePrint()
        if team2.seed != -1:
            print(Back.RED + Fore.BLACK +
                f"{team2.name}({team2.seed}) defeats {team1.name}({team1.seed}) by a score of {team2_wins}-{team1_wins}." + Back.RESET + Fore.RESET)
        else:
            print(Back.RED + Fore.BLACK +
                f"{team2.name} defeats {team1.name} by a score of {team2_wins}-{team1_wins}." + Back.RESET + Fore.RESET)
        if test_output:
            print(series_test(team2_wins, team1_wins))
        if is_uni:
            team2.accolades['Uni-Playoff-Wins'] += 1
        if not both_return:
            return team2
        else:
            return team2, team1
