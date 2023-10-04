from random import choice, seed, uniform
from Player_Creator import s_tier, a_tier, b_tier, c_tier
from colorama import Fore, Back, Style

#todo create TeamSeason class to keep track of team season statistics

class TeamSeason:

    def __init__(self, team, season_count):
        self.season = season_count
        self.team = team

class Team:

    names = ["Phoenixes", "Dragons", "Banshees", "Wraiths", "Specters", "Revenants", "Seraphs", "Chimera", "Gorgons",
             "Minotaurs", "Harpies", "Mermaids", "Naga", "Satyrs", "Centaur", "Unicorns", "Griffins", "Rocs",
             "Sphinxes", "Cyclops", "Titans", "Fates", "Norns", "Valkyries", "Demigods", "Godkillers", "Inferno", "Hive", "Elementals", "Golems",
             "Ifrits", "Djinni", "Imps", "Sprites", "Goblins", "Trolls", "Orcs", "Zombies", "Ghosts", "Werewolves",
             "Vampires", "Liches", "Slayers", "Faeries", "Elves", "Dwarves", "Gnomes",
             "Halflings", "Ogres", "Giants", "Hydras", "Krakens", "Leviathan", "Serpents", "Basilisks",
             "Manticores", "Wyrms", "Wyverns", "Behemoths", "Manticore", "Harpy", "Merfolk", "Naiads",
             "Dryads", "Sirens", "Eladrin", "Draconians", "Demons", "Angelkin", "Succubi", "Incubi",
             "Oni", "Kitsune", "Rakshasa", "Feykin", "Impalers", "Necromancers", "Warlocks",
             "Enchanters", "Shamans", "Sorcerers", "Illusionists", "Geomancers", "Chronomancers",
              "Diviners",  "Magi", "Alchemists", "Witchdoctors", "Arcanists", "Summoners",
             "Purifiers", "Exorcists", "Warden", "Guardians", "Protectors", "Crusaders", "Paladins", "Armament", "Gravity", "Assassins",
             "Templars", "Inquisitors", "Acolytes", "Clerics", "Priests", "Druids", "Shapeshifters", "Skinwalkers",
             "Warg", "Beastmasters",  "Dervish", "Puppeteer", "Psychic", "Oracle", "Mystic", "Tar-Creepers", "Amalgam", 'Wings', 'Termites', 'Revolution',
             'Arch-Kings', 'Samurai', 'Darkness', 'Voidwalkers', 'Ghasts', 'Watchers', 'Bloodspawn', 'Night-Terrors', 'Underlords']

    names = list(set(names))
    names_copy = names.copy()

    def __init__(self,region,mine=False):
        seed()
        if Team.names:
            b = choice(Team.names)
            Team.names.remove(b)
        else:
            Team.names = [f"+{name}" for name in Team.names]

            b = choice(Team.names_copy)
        n = f"{region}_{b}"
        self.mine = mine
        if self.mine:
            self.name = f"**{n}**"
        else:
            self.name = n
        self.region = region
        self.full_name = self.name
        if region == 'House-of-Achlys':
            self.players = [s_tier(), c_tier(2.5), c_tier(2), c_tier(1.75)]
        elif region == 'Universal':
            self.players = [s_tier(), a_tier(), b_tier(round(uniform(1,2),2)), c_tier(0.5)]
        elif region == 'Labyrinth':
            self.players = [a_tier(round(uniform(1,2),2)), b_tier(round(uniform(1,2),2)), b_tier(), b_tier()]
        else:
            self.players = [s_tier(), a_tier(), b_tier(), c_tier(round(uniform(1,2),2))]
        for player in self.players:
            player.team = self.name
        self.wins = 0
        self.losses = 0
        self.trophies = 0
        self.seed = -1
        self.history = {}
        #self.seed_dict = {'RegionRegular' : -1, 'RegionPlayoffs' : -1, 'UniPlayIn' : -1, 'UniGroup' : -1, 'UniRegular' : -1}
        self.group = "None"
        self.margin = 0
        self.accolades = {'Regional-Playoffs' : 0, 'Regional-Champ' : 0, 'Last-Stand' : 0, 'Pre-Qualifying' : 0, 'Universal-Qualifying' : 0, 'Universal-Playoffs' : 0, 'Uni-Playoff-Wins' : 0, 'Universal-Champ' : 0}
        #self.generate_player_names()

    def make_mine(self):
        self.mine = True
        self.name = f"**{self.name}**"

    def print_team_name(self, season_count):
        if self.mine:
            with open('my_teams', 'a') as m:
                m.write(f"S{season_count}_{self.name}\n")
        with open('history', 'a') as h:
            h.write(f"S{season_count}_{self.name}\n")

    def print_team_info(self,test=False):

        if not test:
            print(Fore.RED + Back.CYAN + Style.BRIGHT + f"{self.full_name.upper()}" + Style.RESET_ALL)
            print(Fore.RED + Back.CYAN + Style.BRIGHT + f"Wins: {self.wins} ({round((self.wins/(self.wins+self.losses)*100),2)}%)"
                  + Style.RESET_ALL)
            print(Fore.RED + Back.CYAN + Style.BRIGHT + f"Losses: {self.losses}" + Style.RESET_ALL)
        for player in self.players:
            print(str(player))

    def print_history(self, season_count):
        if self.mine:
            with open('my_teams', 'a') as h:
                if season_count != 1:
                    for s in range(1, season_count + 1):
                        h.write(f"Season {s}: {self.history[s]}\n")
                else:
                    h.write(f"Season 1: {self.history[1]}\n")
                h.write('--------------\n')
        with open('history', 'a') as h:
            if season_count != 1:
                for s in range(1, season_count + 1):
                    h.write(f"Season {s}: {self.history[s]}\n")
            else:
                h.write(f"Season 1: {self.history[1]}\n")
            h.write('--------------\n')

    def print_accolades(self):
        if self.mine:
            with open('my_teams', 'a') as h:
                i = 0
                for key in self.accolades.keys():
                    h.write(f"{key}: {self.accolades[key]}, ")
                    i += 1
                    if i % 4 == 0:
                        h.write('\n')
                h.write('\n')

        with open('history', 'a') as h:
            i=0
            for key in self.accolades.keys():
                h.write(f"{key}: {self.accolades[key]}, ")
                i+=1
                if i%4 == 0:
                    h.write('\n')
            h.write('\n')

    def most_kills_on_team(self):
        max_kills = 0
        index = 0
        for player in self.players:
            if player.kills > max_kills:
                max_kills = player.kills
                max_index = index
            index += 1
        return self.players[max_index]

    def sort_players_by_tier(self):
        players = self.players
        tier_order = {'S': 4, 'A': 3, 'B': 2, 'C': 1}  # Map tier characters to numerical values
        sorted_players = sorted(players, key=lambda p: (tier_order[p.tier], p.power), reverse=True)
        return sorted_players

    def print_roster(self,finale=False):
        if self.mine:
            print(f"{self.name.upper()} ROSTER\n")
            i = 0
            for player in self.players:
                print(f"({i})")
                i += 1
                print(str(player))
            print('\n----------------------\n')
        else:
            if not finale:
                with open('rosters', 'a', buffering=1) as f:
                    f.write(f"{self.name.upper()} ROSTER\n\n")
                    i = 0
                    for player in self.players:
                        f.write(f"({i})\n")
                        i += 1
                        f.write(str(player))
                    f.write('\n----------------------\n\n')
            else:
                with open('rosters', 'w', buffering=1) as f:
                    f.write(f"{self.name.upper()} ROSTER\n\n")
                    i = 0
                    for player in self.players:
                        f.write(f"({i})\n")
                        i += 1
                        f.write(str(player))
                    f.write('\n----------------------\n\n')


    def trade(self, other):
        rec_index = input("Enter the index of the player being received.")
        trad_index = input("Enter the index of the player being traded.")

