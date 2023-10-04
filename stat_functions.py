from scipy.stats import binom_test
from colorama import Fore
import numpy as np
from Players import PlayerSeason, grade_seasons




def season_stats(league, season_count, season_stats_list, alt_stats_list = None,  do_print=False):
    #make season_stats_list into a dict with int keys for season number and values of lists of PlayerSeasons
    season_stats_list[season_count] = []

    for team in league:
        for player in team.players:
            if player.games_played['This-Season'] > 0:
                stats = PlayerSeason(player, season_count)
                season_stats_list[season_count].append(stats)
                if alt_stats_list:
                    alt_stats_list.append(stats)
                if do_print:
                    stats.print_player_season('playerstats')

def best_of_stats(season_stats_list, season_count, alt_stats_list=None):
    full_season_list = []

    with open('best_stats', 'w') as bst:
        bst.write('')
    for val in season_stats_list.values():
        for season in val:
            full_season_list.append(season)


    if alt_stats_list:
        with open('best_stats', 'a') as p:
            p.write("BEST UNIVERSAL LEAGUE SEASONS: \n")
            grade_seasons(alt_stats_list)
            alt_stats_list.sort(key=lambda s : s.season_grade_data, reverse=True)
        for i in range(5):
            alt_stats_list[i].print_player_season('best_stats')

    with open('best_stats', 'a') as p:
        p.write("ALL TIME BEST SEASONS: \n")
        grade_seasons(full_season_list)
        full_season_list.sort(key=lambda s : s.season_grade_data, reverse=True)
    for i in range(5):
        full_season_list[i].print_player_season('best_stats')




    season_stats_list[season_count].sort(key=lambda s : s.kills, reverse=True)
    with open('best_stats', 'a') as p:
        p.write('MOST KILLS\n\n')
    for i in range(3):
        season_stats_list[season_count][i].print_kills_deaths()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nLEAST DEATHS\n\n')
    season_stats_list[season_count].sort(key=lambda s: s.deaths)
    for i in range(3):
        season_stats_list[season_count][i].print_kills_deaths()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nMOST DAMAGE DEALT\n\n')
    season_stats_list[season_count].sort(key=lambda s: s.damage, reverse=True)
    for i in range(3):
        season_stats_list[season_count][i].print_damage()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nMOST DAMAGE MITIGATED\n\n')
    season_stats_list[season_count].sort(key=lambda s: s.mitigated, reverse=True)
    for i in range(3):
        season_stats_list[season_count][i].print_mitigated()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nLARGEST TOTAL EFFECT\n\n')
    season_stats_list[season_count].sort(key=lambda s: s.effect, reverse=True)
    for i in range(3):
        season_stats_list[season_count][i].print_effect()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nLARGEST OVERKILL EFFECT\n\n')
    season_stats_list[season_count].sort(key=lambda s: s.overkill, reverse=True)
    for i in range(3):
        season_stats_list[season_count][i].print_effect()



def series_test(wins, losses):
    p_val = binom_test(wins, wins+losses, 0.50)
    np.set_printoptions(precision=4, suppress=True)
    return Fore.CYAN + f"There is a {round((p_val*100),8)}% chance the result was due to chance alone." + Fore.RESET