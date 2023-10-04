from Games import best_of, enablePrint, blockPrint
from contests import round_robin, chain
from Player_Creator import s_tier, a_tier, b_tier, c_tier
from random import choice, randint
from colorama import Fore, Back
# from dump_pickle import dump_pkl
from load_pickle import load_pkl, season_wipe
from numpy import mean
from Players import calculate_standard_deviation, PlayerSeason
import math


#this will allow me to manually draft players for each team

def ordinal_string(n: int) -> str:
    if 10 <= n % 100 < 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
def half_to_one(num):
    x = (abs(num - 1)) / 2
    return (num + x) if num < 1 else (num - x)

def grade_players(players,is_team=False):
    #should take in a list of players, not a dict draft class
    size = len(players)

    avg_power = mean([player.power for player in players])
    avg_dps = mean([player.dps for player in players])
    avg_crit_x = mean([player.crit_x for player in players])
    avg_crit_pct = mean([player.crit_pct for player in players])
    avg_health = mean([player.max_health for player in players])
    avg_spawn = mean([player.spawn_time for player in players])

    avg_kills = mean([player.kills for player in players])
    avg_deaths = mean([player.deaths for player in players])
    avg_damage = mean([player.damage_data['Total-Damage'] for player in players])
    avg_effect = mean([player.damage_data['Tesseract'] for player in players])
    avg_overkill = mean([player.damage_data['Overkill'] for player in players])
    avg_mitigated = mean([player.crit_data['Mitigated'] for player in players])


    for player in players:
        player.grade_dict['Power'] = calculate_standard_deviation(player.power, size, avg_power)
        player.grade_dict['DPS'] = calculate_standard_deviation(player.dps, size, avg_dps)
        player.grade_dict['Critical-X'] = calculate_standard_deviation(player.crit_x, size, avg_crit_x)
        player.grade_dict['Critical-PCT'] = calculate_standard_deviation(player.crit_pct, size, avg_crit_pct) * 25
        player.grade_dict['Health'] = calculate_standard_deviation(player.max_health, size, avg_health) / 10
        player.grade_dict['Spawn'] = calculate_standard_deviation(player.spawn_time, size, avg_spawn)

        if is_team:
            player.grade_dict['Kills'] = calculate_standard_deviation(player.kills, size, avg_kills)
            player.grade_dict['Deaths'] = calculate_standard_deviation(player.deaths, size, avg_deaths)
            player.grade_dict['Damage'] = calculate_standard_deviation(player.damage_data['Total-Damage'], size, avg_damage)
            player.grade_dict['Effect'] = calculate_standard_deviation(player.damage_data['Tesseract'], size, avg_effect)
            player.grade_dict['Overkill'] = calculate_standard_deviation(player.damage_data['Overkill'], size, avg_overkill)
            player.grade_dict['Mitigated'] = calculate_standard_deviation(player.crit_data['Mitigated'], size, avg_mitigated)

            player.grade_data = player.grade_dict['Kills'] + (player.grade_dict['Deaths'] * -1/2) + player.grade_dict[
                'Damage'] + player.grade_dict['Effect'] + (player.grade_dict['Overkill']/4) + (player.grade_dict['Mitigated']/4)
        else:
            player.grade_data = (player.grade_dict['Power'] * 3) + (player.grade_dict['DPS'] * 2) + player.grade_dict[
                'Critical-X'] + player.grade_dict['Critical-PCT'] + player.grade_dict['Health'] + player.grade_dict[
                                    'Spawn']

def user_draft(teams, season_count, is_regional=False, void=False, draft_name='Default'):
    from random import uniform
    number = -1
    with open('draft_history', 'w') as bruh:
        bruh.write('')
    draft_class = {}
    if not is_regional and not void:
        for i in [0,1,25,26,27,37]:
            add = s_tier()
            add.team = i
            draft_class[i] = add
        for i in [38,39]:
            add = s_tier(randint(1,5))
            add.team = i
            draft_class[i] = add
        for i in [2,3,4,5,6,7,8,40,41]:
            add = a_tier()
            add.team = i
            draft_class[i] = add
        for i in [9,27,28,29]:
            add = a_tier(randint(1,5))
            add.team = i
            draft_class[i] = add
        for i in [10,11,12,13,14,15,16,32]:
            add = b_tier()
            add.team = i
            draft_class[i] = add
        for i in [17,29,30,31]:
            add = b_tier(randint(1,5))
            add.team = i
            draft_class[i] = add
        for i in [18,19,20,21,22,23,35,36]:
            add = c_tier()
            add.team = i
            draft_class[i] = add
        for i in [24,33,34]:
            add = c_tier(randint(1,5))
            add.team = i
            draft_class[i] = add
    elif is_regional and not void:
        for i in [25,26,27]:
            add = s_tier(1)
            add.team = i
            draft_class[i] = add
        for i in [0,1,2,3,4,5,6,7,8,9]:
            add = a_tier(1)
            add.team = i
            draft_class[i] = add
        for i in [10,11,12,13,14,15,16,17,18,19,20]:
            add = b_tier(1)
            add.team = i
            draft_class[i] = add
        for i in [21,22,23,24,28,29,30]:
            add = c_tier(1)
            add.team = i
            draft_class[i] = add
    elif void:
        for i in range(len(teams) + 4):
            add = b_tier(round(uniform(1,5),2))
            add.team = i
            draft_class[i] = add

    p = draft_class.copy()
    grade_players(list(p.values()))
    p = dict(sorted(p.items(), key=lambda plyr:plyr[1].grade_data, reverse=True))

    for i in range(len(teams)):
        with open('draft_list', 'w', buffering=10) as f:
            f.write(f"{draft_name}")
        with open('draft_list', 'a', buffering=10) as f:

            f.write(f" {len(p.values())} of {len(draft_class)} players remaining.\n")
            for player in p.values():
                f.write(str(player.grade_data))
                f.write('\n')
                f.write(
                    f"({player.grade_dict['Power'] :.3f} in power, {player.grade_dict['DPS'] :.3f} in damage output, {player.grade_dict['Critical-X'] :.3f} in critical multiplier, {player.grade_dict['Critical-PCT'] :.3f} in critical percent, {player.grade_dict['Health'] :.3f} in health, {player.grade_dict['Spawn'] :.3f} in spawn.)\n")
                f.write(str(player))
                f.write('\n')

        with open('draft_history', 'a') as x:
            x.write(f"{i+1}. {teams[i].name} to select.\n")
        grade_players(teams[i].players)
        if teams[i].mine:
            enablePrint()
            x=0
            for player in teams[i].players:
                temp = PlayerSeason(player, season_count)
                temp.print_player_season(filename='my_teams')
                print(f"({x})")
                temp.print_player_season()
                x+=1
            print(f"{teams[i].name} to select.")
            try:
                terminate = int(input("Choose player index to terminate."))
            except IndexError:
                terminate = int(input("Choose 0, 1, 2, or 3."))
            index = int(input("Choose player index to draft."))
            try:
                draft(p[index], teams[i], index=i, season_count=season_count, void=void, repl=terminate)
            except KeyError:
                print("Index unavailable. Options are:",end=' ')
                for key in p.keys():
                    print(key,end=', ')
                print('')
                index = int(input("Choose player index to draft."))
                draft(p[index], teams[i], index=i, season_count=season_count, void=void, repl=terminate)
            del p[index]
        else:
            index = i
            teams[i].players.sort(key=lambda pl: pl.grade_data, reverse=True)
            while True:
                try:
                    draft(p[index], teams[i], index=i, season_count=season_count, void=void)
                    break
                except KeyError:
                    index += 1
            del p[index]


def draft(player, team, index, season_count, repl=3, void=False):
    if void:
        team.region = 'Void'
    # team.print_roster()
    old = team.players[repl]
    team.players[repl] = player
    player.team = team.name
    team.history[season_count] += f"\n\tWith the {ordinal_string(index+1)} pick in the {team.region} draft, selected {player.name}\n"
    with open('draft_history', 'a') as x:
        x.write(f"{player.name} has been drafted to {team.name}\n{old.name} terminated.\n")

def player_changes(teams):
        for team in teams:
            for player in team.players:
                age_factor = [1.25, 1.2, 1.1, 1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0, 0]
                tier_factor = {'S' : -0.05, 'A' : -0.02, 'B' : 0.01, 'C' : 0.02}
                t_factor = tier_factor[player.tier]*half_to_one(age_factor[player.age])
                factor = age_factor[player.age] + t_factor
                coin = choice([True,False])
                if coin:
                    player.power += 1
                    if player.power > 100:
                        player.power = 100
                    player.crit_pct = round(player.crit_pct*factor,4)
                else:
                    player.max_health = round(player.max_health*factor, 2)
                    player.atk_dmg = round(player.atk_dmg*factor, 2)
                    player.crit_x = round(player.crit_x*factor, 3)
                player.crit_dmg = player.crit_x * player.atk_dmg
                player.age += 1

def double_elim_16(t, r1_thresh=55, r2_thresh=70, r3_thresh=90, r4_thresh=125, final_thresh=160, is_relegation=False):

    out1 = [0,0,0,0]
    out2 = [0,0,0,0]
    out3 = [0,0]
    out4 = [0,0]
    m1,m2,m3,m4,mF,mGF = round(r1_thresh/6)+11, round(r2_thresh/7)+7, round(r3_thresh/7)+5, round(r4_thresh/9)+9, round(final_thresh/10)+10, round(final_thresh/10)+21

    one, two, three, four, five, six, seven, eight = t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]
    nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen = t[8], t[9], t[10], t[11], t[12], t[13], t[14], t[15]
    if is_relegation:
        one.seed, two.seed, three.seed, four.seed, five.seed, six.seed, seven.seed, eight.seed, nine.seed, ten.seed, eleven.seed, twelve.seed, thirteen.seed, fourteen.seed, fifteen.seed, sixteen.seed = 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
        print(Fore.RED + "RELEGATION TOURNAMENT" + Fore.RESET)
    else:
        one.seed, two.seed, three.seed, four.seed, five.seed, six.seed, seven.seed, eight.seed, nine.seed, ten.seed, eleven.seed, twelve.seed, thirteen.seed, fourteen.seed, fifteen.seed, sixteen.seed = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
        print(Fore.RED + "UNIVERSAL PLAYOFFS" + Fore.RESET)
    print(Fore.GREEN + "R1 winner bracket" + Fore.RESET)
    w1, l1 = best_of(one, sixteen, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w2, l2 = best_of(eight, nine, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w3, l3 = best_of(five, twelve, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w4, l4 = best_of(four, thirteen, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w5, l5 = best_of(three, fourteen, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w6, l6 = best_of(six, eleven, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w7, l7 = best_of(seven, ten, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    w8, l8 = best_of(two, fifteen, r1_thresh,10,True,m1,test_output=True,is_uni=True)
    print(Fore.GREEN + "R1 loser bracket" + Fore.RESET)
    w9, out1[0] = best_of(l1, l2, r1_thresh, 10, True,m1,test_output=True,is_uni=True)
    w10, out1[1] = best_of(l3, l4, r1_thresh, 10,True,m1,test_output=True,is_uni=True)
    w11, out1[2] = best_of(l5, l6, r1_thresh, 10, True,m1,test_output=True,is_uni=True)
    w12, out1[3] = best_of(l7, l8, r1_thresh, 10, True,m1,test_output=True,is_uni=True)
    print(Fore.GREEN + "R2 winner bracket" + Fore.RESET)
    w13, l13 = best_of(w1, w2, r2_thresh, 11, True,m2,test_output=True,is_uni=True)
    w14, l14 = best_of(w3, w4, r2_thresh, 11, True,m2,test_output=True,is_uni=True)
    w15, l15 = best_of(w5, w6, r2_thresh, 11, True,m2,test_output=True,is_uni=True)
    w16, l16 = best_of(w7, w8, r2_thresh, 11, True,m2,test_output=True,is_uni=True)
    print(Fore.GREEN + "R2 loser bracket" + Fore.RESET)
    w17, out2[0] = best_of(w9, l16, r2_thresh, 10, True,m2,test_output=True,is_uni=True)
    w18, out2[1] = best_of(w10, l15, r2_thresh, 10, True,m2,test_output=True,is_uni=True)
    w19, out2[2] = best_of(w11, l14, r2_thresh, 10, True,m2,test_output=True,is_uni=True)
    w20, out2[3] = best_of(w12, l13, r2_thresh, 10, True,m2,test_output=True,is_uni=True)
    print(Fore.GREEN + "R3 winner bracket" + Fore.RESET)
    w21, l21 = best_of(w13, w14, r3_thresh, 12, True,m3,test_output=True,is_uni=True)
    w22, l22 = best_of(w15, w16, r3_thresh, 12, True,m3,test_output=True,is_uni=True)
    print(Fore.GREEN + "R3 loser bracket" + Fore.RESET)
    w23, out3[0] = best_of(w17, w18, r3_thresh, 10, True,m3,test_output=True,is_uni=True)
    w24, out3[1] = best_of(w19, w20, r3_thresh, 10, True,m3,test_output=True,is_uni=True)
    print(Fore.GREEN + "R4 loser bracket" + Fore.RESET)
    w25, out4[0] = best_of(w23, l21, r4_thresh, 10, True,m4,test_output=True,is_uni=True)
    w26, out4[1] = best_of(w24, l22, r4_thresh, 10, True,m4,test_output=True,is_uni=True)
    print(Fore.GREEN + "winner bracket finals" + Fore.RESET)
    w27, l27 = best_of(w21, w22, r4_thresh, 13, True,mF,test_output=True,is_uni=True)
    print(Fore.GREEN + "loser bracket finals" + Fore.RESET)
    w28, out5 = best_of(w25, w26, r4_thresh, 10, True,mF,test_output=True,is_uni=True)
    print(Fore.GREEN + "winner bracket finals LOSER vs loser bracket champ" + Fore.RESET)
    w29, out6 = best_of(w28, l27, r4_thresh, 13, True,mF,test_output=True,is_uni=True)
    print(Fore.GREEN + "grand finals" + Fore.RESET)
    w30, out7 = best_of(w27, w29, final_thresh, 14, True,mGF,test_output=True,is_uni=True)
    if w30 == w27:
        print(Fore.GREEN + f"{w30.full_name} are flawless." + Fore.RESET)
        champ = w30
    else:
        print(Fore.GREEN + f"{w27.full_name} has only lost once. {w29.full_name} must win again." + Fore.RESET)
        w31, out7 = best_of(w27, w29, final_thresh, 14, True,mGF+1,test_output=True,is_uni=True)
        champ = w31
    out1.sort(key = lambda t : t.seed)
    out2.sort(key=lambda t: t.seed)
    out3.sort(key=lambda t: t.seed)
    out4.sort(key=lambda t: t.seed)
    return champ, out7, out6, out5, out4[0], out4[1], out3[0], out3[1], out2[0], out2[1], out2[2], out2[3], out1[0], out1[1], out1[2], out1[3]


def double_elim_8(t,r1_thresh=75, r2_thresh=85, r3_thresh=100, r4_thresh=150, final_thresh=200):
    out_1 = []
    out_2 = []

    r1_margin, r2_margin, r3_margin, r4_margin, final_margin = round(r1_thresh/5)+5, round(r2_thresh/5)+5, round(r3_thresh/5)+5, round(r4_thresh/5)+5, round(final_thresh/5)+1

    one, two, three, four, five, six, seven, eight = t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]
    one.seed, two.seed, three.seed, four.seed, five.seed, six.seed, seven.seed, eight.seed = 1, 2, 3, 4, 5, 6, 7, 8
    print(Fore.GREEN + "R1 winner bracket" + Fore.RESET)
    w1, l1 = best_of(one, eight, r1_thresh,3, True,r1_margin)
    w2, l2 = best_of(four, five, r1_thresh,3,True,r1_margin)
    w3, l3 = best_of(three, six, r1_thresh,3,True,r1_margin)
    w4, l4 = best_of(two, seven, r1_thresh,3,True,r1_margin)
    print(Fore.GREEN + "R1 loser bracket" + Fore.RESET)
    w5, out_temp = best_of(l1, l2, r1_thresh, 3, True,r1_margin)
    out_1.append(out_temp)
    w6, out_temp = best_of(l3, l4, r1_thresh, 3, True,r1_margin)
    out_1.append(out_temp)
    print(Fore.GREEN + "R2 winner bracket" + Fore.RESET)
    w7, l7 = best_of(w1, w2, r2_thresh, 4, True,r2_margin)
    w8, l8 = best_of(w3, w4, r2_thresh, 4, True,r2_margin)
    print(Fore.GREEN + "R2 loser bracket" + Fore.RESET)
    w9, out_temp = best_of(w5, l8, r2_thresh, 4, True,r2_margin)
    out_2.append(out_temp)
    w10, out_temp = best_of(w6, l7, r2_thresh, 4, True,r2_margin)
    out_2.append(out_temp)
    print(Fore.GREEN + "winner bracket finals" + Fore.RESET)
    w11, l11 = best_of(w7, w8, r3_thresh, 5, True,r3_margin,test_output=True)
    print(Fore.GREEN + "loser bracket finals" + Fore.RESET)
    w12, out_final = best_of(w9, w10, r3_thresh, 5, True,r3_margin,test_output=True)
    print(Fore.GREEN + "winner bracket finals LOSER vs loser bracket champ" + Fore.RESET)
    w13, out_third = best_of(w12, l11, r4_thresh, 5, True,r4_margin,test_output=True)
    print(Fore.GREEN + "grand finals" + Fore.RESET)
    w14 = best_of(w11, w13, final_thresh, 6, False,final_margin,test_output=True)
    if w14 == w11:
        print(Fore.GREEN + f"{w14.name} are flawless." + Fore.RESET)
        champ = w14
        runner_up = w13
    else:
        print(Fore.GREEN + f"{w11.name} has only lost once. {w13.full_name} must win again." + Fore.RESET)
        champ, runner_up = best_of(w11, w13, final_thresh, 6, True,final_margin+1,test_output=True)
    out_1.sort(key=lambda x: x.seed, reverse=False)
    out_2.sort(key=lambda x: x.seed, reverse=False)
    s = [out_1[1], out_1[0], out_2[1], out_2[0], out_final, out_third, runner_up, champ]
    return s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]

def swiss_format(teams, base_thresh, base_margin, win_thresh=3):
    advanced = []
    eliminated = []
    def round(wins, losses):
        print(Fore.RED + f"ROUND ({wins},{losses})" + Fore.RESET)
        while len(league_records[(wins,losses)]) >= 2:
            cont1 = choice(league_records[(wins, losses)])
            league_records[(wins, losses)].remove(cont1)
            cont2 = choice(league_records[(wins, losses)])
            winner, loser = best_of(cont1, cont2, base_thresh, amp=4, both_return=True, win_by=base_margin)
            league_records[(wins, losses)].remove(cont2)
            if wins+1 < win_thresh:
                league_records[(wins+1, losses)].append(winner)
            elif wins+1 == win_thresh:
                print(Fore.GREEN + f"{winner.name} advances." + Fore.RESET)
                advanced.append(winner)
            if losses+1 < win_thresh:
                league_records[(wins, losses+1)].append(loser)
            elif losses+1 == win_thresh:
                print(Fore.GREEN + f"{loser.name} is eliminated." + Fore.RESET)
                eliminated.append(loser)


    league_records = {} # keys = list which contains wins and losses
    # values are lists of teams which have that record
    for j in range(0,win_thresh):
        for i in range(0,win_thresh):
            league_records[(i,j)] = []
    league_records[(0, 0)] = teams.copy()
    for j in range(0,win_thresh):
        for i in range(0,win_thresh):
            round(i,j)

    return advanced, eliminated



def league_season(TEAMS,use_saved=False,season_count=-1,final_reversed=True,region='Universal'):
    # 20 team league is standard
    missed_playoffs = []
    play_in = []
    if use_saved:
        TEAMS = load_pkl()
    if len(TEAMS) < 30:
        post_range = 10
        chain_range = None
    elif len(TEAMS) >= 30:
        post_range = 14
        chain_range = 16
    else:
        chain_range = None
        post_range = None
    # see scratch_paper notes on relegation chain



    if region == 'Universal':
        if chain_range:
            postseason, relegation_chain = round_robin(TEAMS, 30, amp=4, qualify_range=post_range, alt_qualify_range=chain_range)
        else:
            postseason = round_robin(TEAMS, 5, qualify_range=post_range)
            relegation_chain = None
    else:
        postseason = round_robin(TEAMS, 5, qualify_range=post_range)
        relegation_chain = None

    for team in TEAMS:
        if team not in postseason:
            if chain_range:
                if team in relegation_chain:
                    team.history[season_count] += f" {ordinal_string(team.seed)} in Universal League -> Relegation Tournament."
                else:
                    team.history[season_count] += f" {ordinal_string(team.seed)} in Universal League -> S_{season_count+1} Universal Qualifying."
                    missed_playoffs.append(team)
            else:
                missed_playoffs.append(team)
                team.history[season_count] += f" {ordinal_string(team.seed)} in {region} League, missed playoffs."

    if post_range == 10:
        one, two, three, four, five, six = postseason[0], postseason[1], postseason[2], postseason[3], postseason[4],postseason[5]
        for i in [6,7,8,9]:
            play_in.append(postseason[i])
        seven, p1 = best_of(play_in[0], play_in[1], 75, 8, True, 4)
        p2, tenth = best_of(play_in[2], play_in[3], 75, 8, True, 4)
        eight, ninth = best_of(p1, p2, 35, 8, True, 4)

        tenth.history[season_count] += f" Lost in {region} play-in, finished 10th."
        ninth.history[season_count] += f" Lost in {region} play-in, finished 9th."

        playoff_one = [one, two, three, four, five, six, seven, eight]

        eighth, seventh, sixth, fifth, fourth, third, second, champ = double_elim_8(
            playoff_one) if region == 'Universal' else double_elim_8(playoff_one, 45, 55, 65, 75, 90)



        for team in playoff_one:
            team.accolades['Regional-Playoffs'] += 1
        champ.accolades['Regional-Champ'] += 1
        relegation_standings = None
        playoff_standings = [champ, second, third, fourth, fifth, sixth, seventh, eighth]
    elif post_range == 16 or post_range == 14 or chain_range:
        relegation_standings = list(double_elim_16(relegation_chain, is_relegation=True))
    if chain_range:
        for i in [0,1]:
            relegation_standings[i].history[season_count] += f" {ordinal_string(i+1)} in Relegation Tournament -> UNI Playoffs."
            postseason.append(relegation_standings[i])
            print(Fore.BLUE + f"{relegation_standings[i].name} will remain in the Universal League." + Fore.RESET)

        for i in [2,3,4,5]:
            relegation_standings[i].history[
                season_count] += f" {ordinal_string(i+1)} in Relegation Tournament -> S_{season_count+1} Universal League."
            missed_playoffs.insert(i-2, relegation_standings[i])
            print(Fore.BLUE + f"{relegation_standings[i].name} will remain in the Universal League." + Fore.RESET)

        for i in range(6,len(relegation_standings)):
            relegation_standings[i].history[
                season_count] += f" {ordinal_string(i+1)} in Relegation Tournament -> S_{season_count+1} Universal Qualifying."
            print(Fore.BLUE + f"{relegation_standings[i].name} is on the chopping block." + Fore.RESET)
            missed_playoffs.insert(i-2, relegation_standings[i])


        playoff_one = list(postseason)
        champ, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth = double_elim_16(postseason, 200, 250, 350, 400, 500)
        playoff_standings = [champ, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth]
        for team in playoff_one:
            team.accolades['Universal-Playoffs'] += 1
        champ.accolades['Universal-Champ'] += 1




    playoff_standings_alt = [second, third, fourth, fifth, sixth, seventh, eighth] if post_range == 10 else [second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth]
    place = 1
    for team in playoff_standings_alt:
        place+=1
        team.history[season_count] += f" {region} playoffs as {team.seed} seed, finished {ordinal_string(place)}."
    if region != 'Universal':
        champ.history[
            season_count] += f" {region} playoffs as {champ.seed} seed, WON CHAMPIONSHIP. -> UNI Qualifier."
        for team in [second, third, fourth]:
            team.history[season_count] += f" -> PQ Swiss."
        for team in [fifth, sixth, seventh, eighth]:
            team.history[season_count] += f" -> Last Stand Tournament."
    else:
        champ.history[season_count] += f" Universal playoffs as {champ.seed} seed, WON CHAMPIONSHIP."

    print(Fore.RED + f"{champ.name} has won the {region} League." + Fore.RESET)

    if ninth and tenth:
        play_in_standings = [ninth, tenth]
        final_standings = playoff_standings + play_in_standings + missed_playoffs
    else:
        final_standings = playoff_standings + missed_playoffs
    for team in final_standings:
        if team.mine:
            print(Fore.BLUE + f"{team.name}: {team.history[season_count]}"
                  + Fore.RESET)

    for pos in range(len(final_standings)):
        final_standings[pos].seed = pos
    if final_reversed:
        final_standings.reverse()
    return final_standings

