from Teams import Team
from contests import round_robin
from colorama import Fore, Style
from dump_pickle import dump_pkl
from load_pickle import season_wipe, load_pkl
import time
from random import choice
from leagues import league_season, user_draft, player_changes, grade_players, double_elim_8, double_elim_16, swiss_format
from Games import best_of
import concurrent.futures
from stat_functions import season_stats, best_of_stats
import multiprocessing

GENERAL_OUTPUT = False

start = time.time()

def create_teams(count,region='None'):
    TEAMS = []
    for i in range(count):
        temp = Team(region)
        TEAMS.append(temp)
    return TEAMS

def ordinal_string(n: int) -> str:
    if 10 <= n % 100 < 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def user_season():
    #simulate a league which gives me a specific team and allows me to make draft picks and other actions for my team
    #all other teams are run automatically
    #18 team regional leagues, 8 team playoff (with play-in), champs auto-advance to universal tournament, 2-4 seed (12 teams) automatically go to qualifying tournament
    #5-8 seed (16 teams + 16 universal teams) enter Last Stand round-robin, top 12 advance to qualifying.
    #qualifying tournament is 24 team swiss, top 12 advance to universal playoffs alongside the regional champs
    #universal tournament is 16 team double elimination
    #all teams in the universal tournament participate in the following season's Last Stand tournament
    #there are four classes of draft: regional draft (worst) given to the 40 teams that did not qualify for the regional playoffs
    #Stand draft (second) given to 20 (8 in season 1) teams that did not qualify from LS.
    #Q draft (third) given to the 12 teams eliminated in the qualifying swiss
    #Uni draft (best) given to all 16 teams in the universal tournament

    season_count = 1
    north_teams = create_teams(19, 'North')
    north_teams.append(Team('North', mine=True))
    south_teams = create_teams(20, 'South')
    east_teams = create_teams(20, 'East')
    west_teams = create_teams(20, 'West')

    north_standings = league_season(north_teams, False, final_reversed=False, region='North', season_count=season_count)


def main():
    # file clearing:
    with open('my_teams', 'w') as f:
        f.write('')

    my_team_count = 5

    SEASONS = 20

    season_stats_list = {}
    uni_stats_list = []

    #todo fix error which occurs with team history when the code is run with use_saved
    use_saved = False

    if use_saved:
        try:
            upl_standings, dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams, season_count = load_pkl()
            uni_teams = upl_standings
        except ValueError:
            use_saved = False
    if not use_saved:
        season_count = 0
        uni_teams = create_teams(26, "Universal")
        #my_uni_team = choice(uni_teams)
        #my_uni_team.make_mine()
        for team in uni_teams:
            team.history[season_count] = ""
        upl_standings = league_season(uni_teams, use_saved=False, season_count=0)
        dw_teams = create_teams(20, "Darkwing")
        sc_teams = create_teams(20, "Shining-Core")
        ds_teams = create_teams(20, "Diamond-Sea")
        wof_teams = create_teams(20, "Web-of-Nations")
        iw_teams = create_teams(20, "Ice-Wall")
        cl_teams = create_teams(20, "Candyland")
        hc_teams = create_teams(20, "Hell's-Circle")
        sh_teams = create_teams(20, "Steel-Heart")
        for league in [dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
            lab_teams = create_teams(2,'House-of-Achlys')
            league.append(lab_teams[0])
            league.append(lab_teams[1])
        for _ in range(my_team_count):
            chance = choice([dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams])
            my_team = choice(chance)
            my_team.make_mine()

    def regional_leagues(dw_teams,sc_teams,ds_teams,wof_teams,iw_teams,cl_teams,hc_teams,sh_teams,season_count):
            pre_qualif_tournament = []
            last_stand_tournament = []

            print(Fore.GREEN + "DARKWING REGION, " + Fore.RESET, end='')
            dw_teams = league_season(dw_teams, False, season_count=season_count, final_reversed=False,
                                     region='Darkwing Regional')
            dw_qualified = dw_teams[:9]

            print(Fore.GREEN + "SHINING CORE REGION, " + Fore.RESET, end='')
            sc_teams = league_season(sc_teams, False, season_count=season_count, final_reversed=False,
                                     region='Shining-Core Regional')
            sc_qualified = sc_teams[:9]

            print(Fore.GREEN + "DIAMOND SEA REGION, " + Fore.RESET, end='')
            ds_teams = league_season(ds_teams, False, season_count=season_count, final_reversed=False,
                                     region='Diamond-Sea Regional')
            ds_qualified = ds_teams[:9]

            print(Fore.GREEN + "WEB OF NATIONS, " + Fore.RESET, end='')
            wof_teams = league_season(wof_teams, False, season_count=season_count, final_reversed=False,
                                      region='Web-of-Nations Regional')
            wof_qualified = wof_teams[:9]

            print(Fore.GREEN + "ICE WALL REGION, " + Fore.RESET, end='')
            iw_teams = league_season(iw_teams, False, season_count=season_count, final_reversed=False,
                                     region='Ice-Wall Regional')
            iw_qualified = iw_teams[:9]

            print(Fore.GREEN + "CANDYLAND REGION " + Fore.RESET, end='')
            cl_teams = league_season(cl_teams, False, season_count=season_count, final_reversed=False,
                                     region='Candyland Regional')
            cl_qualified = cl_teams[:9]

            print(Fore.GREEN + "HELL'S CIRCLE, " + Fore.RESET, end='')
            hc_teams = league_season(hc_teams, False, season_count=season_count, final_reversed=False,
                                     region="Hell's-Circle Regional")
            hc_qualified = hc_teams[:9]

            print(Fore.GREEN + "STEEL HEART REGION, " + Fore.RESET, end='')
            sh_teams = league_season(sh_teams, False, season_count=season_count, final_reversed=False,
                                     region="Steel-Heart Regional")
            sh_qualified = sh_teams[:9]

            dw_champ = dw_qualified[0]
            regional_champs.append(dw_champ)
            sc_champ = sc_qualified[0]
            regional_champs.append(sc_champ)
            ds_champ = ds_qualified[0]
            regional_champs.append(ds_champ)
            wof_champ = wof_qualified[0]
            regional_champs.append(wof_champ)
            iw_champ = iw_qualified[0]
            regional_champs.append(iw_champ)
            cl_champ = cl_qualified[0]
            regional_champs.append(cl_champ)
            hc_champ = hc_qualified[0]
            regional_champs.append(hc_champ)
            sh_champ = sh_qualified[0]
            regional_champs.append(sh_champ)

            # trans_region = ['Darkwing', 'Shining-Core', 'Diamond-Sea', 'Web-of-Nations', 'Ice-Wall', 'Candyland', "Hell's-Circle", 'Steel-Heart']
            count = 0
            for region in [dw_qualified, sc_qualified, ds_qualified, wof_qualified, iw_qualified, cl_qualified,
                           hc_qualified, sh_qualified]:
                season_wipe(region)
                for i in [1, 2, 3, 4]:
                    pre_qualif_tournament.append(region[i])
                for i in [5, 6, 7, 8]:
                    last_stand_tournament.append(region[i])
                count += 1
            return regional_champs, pre_qualif_tournament, last_stand_tournament
    another = 'y'
    relegated = {} # int keys, team object values
    promoted = {}

    for num in range(SEASONS):
        season_count += 1
        relegated[season_count] = []
        promoted[season_count] = []
        for league in [dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
            season_wipe(league)
            for team in league:
                team.history[season_count] = ""
        if season_count != 0:
            season_wipe(uni_teams)
            for team in uni_teams:
                team.history[season_count] = ""

        uni_qualif_g1 = []
        uni_qualif_g2 = []
        regional_champs = []
        regional_champs, pqt, last_stand = regional_leagues(dw_teams,sc_teams,ds_teams,wof_teams,iw_teams,cl_teams,hc_teams,sh_teams,season_count=season_count)
        print(Fore.GREEN + "LAST STAND TOURNAMENT, " + Fore.RESET, end='')
        for team in last_stand:
            team.accolades['Last-Stand'] += 1
        pre, pre_elim = swiss_format(last_stand, 70, 14, 4)
        season_wipe(pre)
        for team in pre:
            team.history[season_count] += f" Advanced from Last Stand Swiss -> Pre-Qualif. Swiss."
            pqt.append(team)
        for team in pre_elim:
            team.history[season_count] += f" Failed to advance from Last Stand Swiss."

        print(Fore.GREEN + "PRE-QUALIFYING TOURNAMENT, " + Fore.RESET, end='')
        for team in pqt:
            team.accolades['Pre-Qualifying'] += 1
        pre2, pre2_gone = swiss_format(pqt,75,17)

        for i in range(int(len(pre2)/2)):
            g1 = choice(pre2)
            pre2.remove(g1)
            uni_qualif_g1.append(g1)
            g1.history[season_count] += f" Advanced from PQ Swiss. -> UNI Qualifier."

            g2 = choice(pre2)
            pre2.remove(g2)
            uni_qualif_g2.append(g2)
            g2.history[season_count] += f" Advanced from PQ Swiss. -> UNI Qualifier."
        for team in pre2_gone:
            team.history[season_count] += f" Failed to advance from PQ Swiss."

        for i in range(8):
            if i % 2 == 0:
                uni_qualif_g1.append(regional_champs[i])
            elif i % 2 == 1:
                uni_qualif_g2.append(regional_champs[i])
        for group in [uni_qualif_g1, uni_qualif_g2]:
            season_wipe(group)

        if len(upl_standings) < 30:
            drop_range1 = [0, 2, 5]
            drop_range2 = [1, 3, 4]
        else:
            drop_range1 = [0, 2, 5, 6, 9, 11, 12,14]
            drop_range2 = [1, 3, 4, 7, 8, 10, 13,15]

        for i in drop_range1:
            uni_qualif_g1.append(upl_standings[i])
            uni_teams.remove(upl_standings[i])
            relegated[season_count].append(upl_standings[i])

        for i in drop_range2:
            uni_qualif_g2.append(upl_standings[i])
            uni_teams.remove(upl_standings[i])
            relegated[season_count].append(upl_standings[i])

        for team in uni_qualif_g1:
            team.accolades['Universal-Qualifying'] += 1
        for team in uni_qualif_g2:
            team.accolades['Universal-Qualifying'] += 1

        print(Fore.GREEN + "GROUP 1 QUALIFYING ROUND, " + Fore.RESET, end='')
        g1_pre_advance = round_robin(uni_qualif_g1, 40, len(uni_qualif_g1), amp=3)
        print(Fore.GREEN + "GROUP 2 QUALIFYING ROUND, " + Fore.RESET, end='')
        g2_pre_advance = round_robin(uni_qualif_g2, 40, len(uni_qualif_g2), amp=3)
        uni_teams.reverse()
        g1_advance = []
        g2_advance = []



        for i in range(7):
            g1_advance.append(g1_pre_advance[i])
            g1_pre_advance[i].history[season_count] += f" {ordinal_string(i+1)} in Group 1 Qualifying. -> UNI League."
            g2_advance.append(g2_pre_advance[i])
            g2_pre_advance[i].history[season_count] += f" {ordinal_string(i+1)} in Group 2 Qualifying. -> UNI League."
        for i in range(7,9):
            g1_advance.append(g1_pre_advance[i])
            g1_pre_advance[i].history[season_count] += f" {ordinal_string(i + 1)} in Group 1 Qualifying."
            g2_advance.append(g2_pre_advance[i])
            g2_pre_advance[i].history[season_count] += f" {ordinal_string(i + 1)} in Group 2 Qualifying."
        for i in range(9,len(g1_pre_advance)):
            g1_pre_advance[i].history[season_count] += f" {ordinal_string(i+1)} in Group 1 Qualifying. Failed to qualify."
            g2_pre_advance[i].history[season_count] += f" {ordinal_string(i+1)} in Group 2 Qualifying. Failed to qualify."


        for i in range(7):
            if g1_advance[i] in relegated[season_count]:
                relegated[season_count].remove(g1_advance[i])
            else:
                promoted[season_count].append(g1_advance[i])
            uni_teams.append(g1_advance[i])
            if g2_advance[i] in relegated[season_count]:
                relegated[season_count].remove(g2_advance[i])
            else:
                promoted[season_count].append(g2_advance[i])
            uni_teams.append(g2_advance[i])
        fin1, tough1 = best_of(g1_advance[7], g2_advance[8], 100, 10, True, 25)
        if fin1 in relegated[season_count]:
            relegated[season_count].remove(fin1)
        else:
            promoted[season_count].append(fin1)
        fin2, tough2 = best_of(g1_advance[8], g2_advance[7], 100, 10, True, 25)
        if fin2 in relegated[season_count]:
            relegated[season_count].remove(fin2)
        else:
            promoted[season_count].append(fin2)
        uni_teams.append(fin1)
        uni_teams.append(fin2)
        fin1.history[season_count] += f" Won Play-In against {tough1.name} -> UNI League."
        fin2.history[season_count] += f" Won Play-In against {tough2.name} -> UNI League."
        tough1.history[season_count] += f" Lost Play-In against {fin1.name}"
        tough2.history[season_count] += f" Lost Play-In against {fin2.name}"
        season_wipe(uni_teams)
        upl_standings = league_season(uni_teams, use_saved=False, season_count=season_count)

        #todo fix the order in which promotion and relegation history is assigned
        #currently, teams which make it into the qualifying for next season are being considered Promoted

        for team in promoted[season_count]:
            print(f"{team.name} PROMOTED.")
            team.history[season_count] += "\n\tPROMOTED to Universal League."
        for team in relegated[season_count]:
            print(f"{team.name} RELEGATED.")
            team.history[season_count] += "\n\tRELEGATED to "
        with open('history', 'w') as b:
            b.write('')
        with open('playerstats', 'w') as c:
            c.write('')
        reverse_upl_standings = list(reversed(upl_standings))

        season_stats(uni_teams, season_count, season_stats_list, alt_stats_list=uni_stats_list, do_print=True)
        for league in [dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
            season_stats(league, season_count, season_stats_list, do_print=False)
        best_of_stats(season_stats_list, season_count, alt_stats_list=uni_stats_list)


        # todo give teams who make each stage of advancement a better draft opportunity and guaranteed spots for some

        if True:
            all_players = []

            for league in [dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
                league.reverse()
            for team in uni_teams:
                if team in dw_teams:
                    dw_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        dw_teams.append(add)
                        add.history[season_count] += "Darkwing Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Darkwing Regional."
                        dw_teams.insert(0, add)
                elif team in sc_teams:
                    sc_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        sc_teams.append(add)
                        add.history[season_count] += "Shining-Core Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Shining-Core Regional."
                        sc_teams.insert(0, add)
                elif team in ds_teams:
                    ds_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        ds_teams.append(add)
                        add.history[season_count] += "Diamond-Sea Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Diamond-Sea Regional."
                        ds_teams.insert(0, add)
                elif team in wof_teams:
                    wof_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        wof_teams.append(add)
                        add.history[season_count] += "Web-of-Nations Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Web-of-Nations Regional."
                        wof_teams.insert(0, add)
                elif team in iw_teams:
                    iw_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        iw_teams.append(add)
                        add.history[season_count] += "Ice-Wall Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Ice-Wall Regional."
                        iw_teams.insert(0, add)
                elif team in cl_teams:
                    cl_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        cl_teams.append(add)
                        add.history[season_count] += "Candyland Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Candyland Regional."
                        cl_teams.insert(0, add)
                elif team in hc_teams:
                    hc_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        hc_teams.append(add)
                        add.history[season_count] += "Hell's-Circle Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Hell's-Circle Regional."
                        hc_teams.insert(0, add)
                elif team in sh_teams:
                    sh_teams.remove(team)
                    if relegated[season_count]:
                        add = choice(relegated[season_count])
                        relegated[season_count].remove(add)
                        sh_teams.append(add)
                        add.history[season_count] += "Steel-Heart Regional."
                    else:
                        add = Team('Labyrinth')
                        add.history[season_count] = "Introduced into the Steel-Heart Regional."
                        sh_teams.insert(0, add)


            #todo when a team is promoted to the universal league, the draft function initializes a player season to print and these teams have 0 games played fix this
            for league in [uni_teams, dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
                player_changes(league)
            with open("rosters", 'w') as l:
                l.write('')
            with open("rosters", 'a') as w:
                w.write(f"SEASON NO. {season_count}\n")
                trans_region = ['Universal', 'Darkwing', 'Shining-Core', 'Diamond-Sea', 'Web-of-Nations', 'Ice-Wall', 'Candyland', "Hell's-Circle", 'Steel-Heart']
                trans_i = -1
                for league in [uni_teams, dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
                    trans_i +=1
                    for team in league:
                        team.region = trans_region[trans_i]
                        for player in team.players:
                            all_players.append(player)
                grade_players(all_players,is_team=True)
                for player in all_players:
                    w.write(f"{str(player)}\n")


            user_draft(dw_teams, season_count, is_regional=True, draft_name="Darkwing-Regional-Draft")
            user_draft(sc_teams, season_count, is_regional=True, draft_name="Shining-Core-Regional-Draft")
            user_draft(ds_teams, season_count, is_regional=True, draft_name="Diamond-Sea-Regional-Draft")
            user_draft(wof_teams, season_count, is_regional=True, draft_name="Web-of-Nations-Regional-Draft")
            user_draft(iw_teams, season_count,  is_regional=True, draft_name="Ice-Wall-Regional-Draft")
            user_draft(cl_teams, season_count, is_regional=True, draft_name="Candyland-Regional-Draft")
            user_draft(hc_teams, season_count,  is_regional=True, draft_name="Hell's-Circle-Regional-Draft")
            user_draft(sh_teams, season_count, is_regional=True, draft_name="Steel-Heart-Regional-Draft")

            upl_draft = reverse_upl_standings[0:20]
            upl_draft.reverse()
            #This takes the top 20 from the UPL and reverses them

            void_draft = reverse_upl_standings[20:]
            void_draft.reverse()
            #This takes the 16 teams which were eliminated and puts the draft in order from worst to best by reversing

            user_draft(upl_draft, season_count, draft_name='Universal-Draft')
            user_draft(void_draft, season_count, void=True, draft_name='Void-Draft')

            for league in [uni_teams, dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams,
                           sh_teams]:
                for team in league:
                    team.print_team_name(season_count)
                    team.print_accolades()
                    team.print_history(season_count)
                    if team.mine:
                        print("\n" + Fore.BLUE + team.history[season_count] + Fore.RESET)

            system = [upl_standings,dw_teams,sc_teams,ds_teams,wof_teams,iw_teams,cl_teams,hc_teams,sh_teams,season_count]
            dump_pkl(system)
    # uni_champions.sort(key=lambda x : (x.wins / x.losses), reverse=True)
    end = time.time()
    print(f"\nTotal Execution Time: {round((end-start)/60)} minutes, {round(((end-start)%60),2)} seconds.")


def not_main():
    def regional_leagues(dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams, season_count):
        pre_qualif_tournament = []
        last_stand_tournament = []
        regional_champs = []
        regional_qualifiers = {'dw': [], 'sc': [], 'ds': [], 'wof': [], 'iw': [], 'cl': [],
                               'hc': [], 'sh': []}
        args_list = [(dw_teams, False, season_count, False, "Darkwing Regional"),
                     (sc_teams, False, season_count, False, "Shining-Core Regional"),
                     (ds_teams, False, season_count, False, "Diamond-Sea Regional"),
                     (wof_teams, False, season_count, False, "Web-of-Nations Regional"),
                     (iw_teams, False,season_count, False, "Ice-Wall Regional"),
                     (cl_teams, False,season_count, False, "Candyland Regional"),
                     (hc_teams, False,season_count, False, "Hell's-Circle Regional"),
                     (sh_teams, False,season_count, False, "Steel-Heart Regional")]

        if __name__ == '__main1__':
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = list(executor.map(league_season, args_list))
                v = 0
                prefixes =  ['dw', 'sc', 'ds', 'wof', 'iw', 'cl', 'hc', 'sh']
                for result in results:
                    regional_qualifiers[prefixes[v]] = result
                    v+=1

                dw_qualified = regional_qualifiers['dw']
                sc_qualified = regional_qualifiers['sc']
                ds_qualified = regional_qualifiers['ds']
                wof_qualified = regional_qualifiers['wof']
                iw_qualified = regional_qualifiers['iw']
                cl_qualified = regional_qualifiers['cl']
                hc_qualified = regional_qualifiers['hc']
                sh_qualified = regional_qualifiers['sh']

                dw_champ = dw_qualified[0]
                regional_champs.append(dw_champ)
                sc_champ = sc_qualified[0]
                regional_champs.append(sc_champ)
                ds_champ = ds_qualified[0]
                regional_champs.append(ds_champ)
                wof_champ = wof_qualified[0]
                regional_champs.append(wof_champ)
                iw_champ = iw_qualified[0]
                regional_champs.append(iw_champ)
                cl_champ = cl_qualified[0]
                regional_champs.append(cl_champ)
                hc_champ = hc_qualified[0]
                regional_champs.append(hc_champ)
                sh_champ = sh_qualified[0]
                regional_champs.append(sh_champ)

            # trans_region = ['Darkwing', 'Shining-Core', 'Diamond-Sea', 'Web-of-Nations', 'Ice-Wall', 'Candyland', "Hell's-Circle", 'Steel-Heart']
            count = 0
            for region in [dw_qualified, sc_qualified, ds_qualified, wof_qualified, iw_qualified, cl_qualified,
                           hc_qualified, sh_qualified]:
                season_wipe(region)
                for i in [1, 2, 3, 4]:
                    pre_qualif_tournament.append(region[i])
                for i in [5, 6, 7, 8]:
                    last_stand_tournament.append(region[i])
                count += 1
            return regional_champs, pre_qualif_tournament, last_stand_tournament
    dw_teams = create_teams(20, "Darkwing")
    sc_teams = create_teams(20, "Shining-Core")
    ds_teams = create_teams(20, "Diamond-Sea")
    wof_teams = create_teams(20, "Web-of-Nations")
    iw_teams = create_teams(20, "Ice-Wall")
    cl_teams = create_teams(20, "Candyland")
    hc_teams = create_teams(20, "Hell's-Circle")
    sh_teams = create_teams(20, "Steel-Heart")
    for league in [dw_teams, sc_teams, ds_teams, wof_teams, iw_teams, cl_teams, hc_teams, sh_teams]:
        lab_teams = create_teams(2, 'House-of-Achlys')
        league.append(lab_teams[0])
        league.append(lab_teams[1])
    regional_leagues(dw_teams,sc_teams,ds_teams,wof_teams,iw_teams,cl_teams,hc_teams,sh_teams,1)



main()



