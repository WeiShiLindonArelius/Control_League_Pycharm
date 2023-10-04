def single_elim_64(TEAMS):

    R_64 = TEAMS.copy()
    R_32 = []
    R_16 = []
    R_8 = []
    FinalFour = []
    GrandFinal = []

    for i in range(32):
        team1 = choice(R_64)
        R_64.remove(team1)
        team2 = choice(R_64)
        R_64.remove(team2)
        og.write(f"{team1.name} VERSUS {team2.name}\n")
        result = game(team1, team2)
        og.write(f"WINNER: {result.name}\n")
        R_32.append(result)

    for i in range(16):
        team1 = choice(R_32)
        R_32.remove(team1)
        team2 = choice(R_32)
        R_32.remove(team2)
        og.write(f"{team1.name} VERSUS {team2.name}\n")
        result = game(team1, team2)
        og.write(f"WINNER: {result.name}\n")
        R_16.append(result)

    for i in range(8):
        team1 = choice(R_16)
        R_16.remove(team1)
        team2 = choice(R_16)
        R_16.remove(team2)
        og.write(f"{team1.name} VERSUS {team2.name}\n")
        result = game(team1, team2)
        og.write(f"WINNER: {result.name}\n")
        R_8.append(result)

    for i in range(4):
        team1 = choice(R_8)
        R_8.remove(team1)
        team2 = choice(R_8)
        R_8.remove(team2)
        og.write(f"{team1.name} VERSUS {team2.name}\n")
        result = game(team1, team2)
        og.write(f"WINNER: {result.name}\n")
        FinalFour.append(result)

    for i in range(2):
        team1 = choice(FinalFour)
        FinalFour.remove(team1)
        team2 = choice(FinalFour)
        FinalFour.remove(team2)
        og.write(f"{team1.name} VERSUS {team2.name}\n")
        result = game(team1, team2)
        og.write(f"WINNER: {result.name}\n")
        GrandFinal.append(result)

    team1 = choice(GrandFinal)
    GrandFinal.remove(team1)
    team2 = choice(GrandFinal)
    GrandFinal.remove(team2)
    og.write(f"Grand Final: {team1.name} VERSUS {team2.name}\n")
    result = game(team1, team2)
    og.write(f"GRAND CHAMPION: {result.name}!!!\n")
    result.trophies += 1
    return result

def written_game(team1, team2,amp=4):
    t = open("test_spec_output", 'a')
    def true_game(team1, team2):
        o = open("play_by_play", 'w')
        if not PLAY_BY_PLAY:
            o.write = no_op
        if not TEST_OUTPUT:
            t.write = no_op
        TESSERACT = 0
        length = 1
        length *= amp
        length += 1
        for tick in range(1,length):
            living_team1 = []
            living_team2 = []
            for player in team1.players:
                if player.is_alive:
                    living_team1.append(player)
                elif player.countdown == 0:
                    player.respawn()
                    o.write(f"Team 1 {player.tier} respawned.")
                    living_team1.append(player)
                else:
                    player.countdown -= 1

            for player in team2.players:
                if player.is_alive:
                    living_team2.append(player)
                elif player.countdown == 0:
                    player.respawn()
                    o.write(f"Team 2 {player.tier} respawned.")
                    living_team2.append(player)
                else:
                    player.countdown -= 1

            sub_count = 0
            while True:

                #this is a loop which iterates through every player for every single tick!
                #first, check if there are players who have not yet gone
                if not living_team1 and not living_team2:
                    o.write(f"END TICK NO. {tick}. ({sub_count} sub-ticks)\n")
                    break
                #if coin is 0, check and run team 1 first.
                #if coin is 1, vice versa
                coin = randint(0, 999)
                #print(f"tick no. {tick}")
                write = f"tick no. {tick}\n"
                o.write(write)
                if coin%2 == 0:
                    if living_team1:
                        attacker = living_team1[0]
                        if tick % attacker.atk_spd == 0:
                            if living_team2:
                                defender = choice(living_team2)
                                attacker.attack(defender)
                                write = (f"Team 1 {attacker.tier} attacks Team 2 {defender.tier}\n")
                                o.write(write)
                                if not defender.is_alive:
                                    o.write(f"Team 2 {defender.tier} ELIMINATED!")
                                    living_team2.remove(defender)

                            else:
                                TESSERACT += (attacker.crit_dmg)
                                write = (f"No living Team 2 defender. Tesseract hit for {(attacker.crit_dmg)} damage by Team 1 {attacker.tier}.\n")
                                o.write(write)

                        TESSERACT += attacker.power
                        write = (f"Tesseract value increased by {attacker.power}\n")
                        o.write(write)
                        living_team1.remove(attacker)
                    else:
                        attacker = living_team2[0]
                        if tick % attacker.atk_spd == 0:
                            TESSERACT -= (attacker.crit_dmg)
                            write = f"No living Team 1 defender. Tesseract hit for {(attacker.crit_dmg)} damage by Team 2 {attacker.tier}.\n"
                            o.write(write)
                        TESSERACT -= attacker.power
                        write = (f"Tesseract value decreased by {attacker.power}\n")
                        o.write(write)
                        living_team2.remove(attacker)
                elif coin%2 == 1:
                    if living_team2:
                        attacker = living_team2[0]
                        if tick % attacker.atk_spd == 0:
                            if living_team1:
                                defender = choice(living_team1)
                                attacker.attack(defender)
                                write = (f"Team 2 {attacker.tier} attacks Team 1 {defender.tier} for {attacker.atk_dmg} damage\n")
                                o.write(write)
                                if not defender.is_alive:
                                    o.write(f"Team 1 {defender.tier} ELIMINATED!")
                                    living_team1.remove(defender)
                            else:
                                TESSERACT -= (attacker.crit_dmg)
                                write = f"No living Team 1 defender. Tesseract hit for {(attacker.crit_dmg)} damage by Team 2 {attacker.tier}.\n"
                                o.write(write)

                        TESSERACT -= attacker.power
                        write = (f"Tesseract value decreased by {attacker.power}\n")
                        o.write(write)
                        living_team2.remove(attacker)
                    else:
                        attacker = living_team1[0]
                        if tick % attacker.atk_spd == 0:
                            TESSERACT -= (attacker.crit_dmg)
                            write = f"No living Team 2 defender. Tesseract hit for {(attacker.crit_dmg)} damage by Team 1 {attacker.tier}.\n"
                            o.write(write)
                        TESSERACT += attacker.power
                        write = (f"Tesseract value increased by {attacker.power}\n")
                        o.write(write)
                        living_team1.remove(attacker)
                sub_count += 1
        if TESSERACT > 0:
            #print("Team 1 wins with a tesseract value of", TESSERACT)
            team1.wins += 1
            team1.margin += abs(round(TESSERACT,2))
            team2.losses += 1
            team2.margin -= abs(round(TESSERACT,2))
            return team1

        else:
            #print("Team 2 wins with a tesseract value of", TESSERACT)
            team2.wins += 1
            team2.margin += abs(round(TESSERACT,2))
            team1.losses += 1
            team1.margin -= abs(round(TESSERACT,2))
            return team2
    bb_coin = randint(1,999)
    if bb_coin%2 == 0:
        result = true_game(team1,team2)
        if result == team1:
            t.write("Team 1 Wins\n")
        elif result == team2:
            t.write("Team 2 Wins\n")
        else:
            t.write("ERROR\n")
        return result
    elif bb_coin%2 == 1:
        result = true_game(team2, team1)
        if result == team1:
            t.write("Team 1 Wins\n")
        elif result == team2:
            t.write("Team 2 Wins\n")
        else:
            t.write("ERROR\n")
        return result

  print(Fore.GREEN + "DARKWING REGION, " + Fore.RESET, end='')
        dw_teams = league_season(dw_teams,False,season_count=season_count,final_reversed=False,region='Darkwing Regional')


        print(Fore.GREEN + "SHINING CORE REGION, " + Fore.RESET, end='')
        sc_teams = league_season(sc_teams,False,season_count=season_count,final_reversed=False,region='Shining-Core Regional')


        print(Fore.GREEN + "DIAMOND SEA REGION, " + Fore.RESET, end='')
        ds_teams = league_season(ds_teams,False,season_count=season_count,final_reversed=False,region='Diamond-Sea Regional')


        print(Fore.GREEN + "WEB OF NATIONS, " + Fore.RESET, end='')
        wof_teams = league_season(wof_teams,False,season_count=season_count,final_reversed=False, region='Web-of-Nations Regional')


        print(Fore.GREEN + "ICE WALL REGION, " + Fore.RESET, end='')
        iw_teams = league_season(iw_teams,False,season_count=season_count,final_reversed=False, region='Ice-Wall Regional')


        print(Fore.GREEN + "CANDYLAND REGION, " + Fore.RESET, end='')
        cl_teams = league_season(cl_teams,False,season_count=season_count,final_reversed=False,region='Candyland Regional')


        print(Fore.GREEN + "HELL'S CIRCLE, " + Fore.RESET, end='')
        hc_teams = league_season(hc_teams,False,season_count=season_count,final_reversed=False,region="Hell's-Circle Regional")


        print(Fore.GREEN + "STEEL HEART REGION, " + Fore.RESET, end='')
        sh_teams = league_season(sh_teams,False,season_count=season_count,final_reversed=False,region="Steel-Heart Regional")


