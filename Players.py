from random import uniform, seed
from colorama import Fore, Style
import math

def calculate_standard_deviation(number, sample_size, sample_average):
    deviation = number - sample_average
    standard_deviation = deviation / math.sqrt(sample_size)
    return standard_deviation


def grade_seasons(seasons):
    #iterate through each object, and create lists with values corresponding to each player
    #put each list through calculate_standard_deviations and use it to assign a coefficient variable to each player equivalent
    #a total season's grade is determined by the sum of all coefficients

    total_kills = 0
    total_deaths = 0
    total_damage = 0
    total_effect = 0
    total_overkill = 0
    total_mitigated = 0


    size = len(seasons)

    for season in seasons:
        total_kills += season.kills
        total_deaths += season.deaths
        total_damage += season.damage
        total_effect += season.effect
        total_overkill += season.overkill
        total_mitigated += season.mitigated
    avg_kills = total_kills / size
    avg_deaths = total_deaths / size
    avg_damage = total_damage / size
    avg_effect = total_effect / size
    avg_overkill = total_overkill / size
    avg_mitigated = total_mitigated / size

    for season in seasons:
        season.season_grade_dict['Kills'] = calculate_standard_deviation(season.kills, size, avg_kills)
        season.season_grade_dict['Deaths'] = calculate_standard_deviation(season.deaths, size, avg_deaths)
        season.season_grade_dict['Damage'] = calculate_standard_deviation(season.damage, size, avg_damage)
        season.season_grade_dict['Effect'] = calculate_standard_deviation(season.effect, size, avg_effect)
        season.season_grade_dict['Overkill'] = calculate_standard_deviation(season.overkill, size, avg_overkill)
        season.season_grade_dict['Mitigated'] = calculate_standard_deviation(season.mitigated, size, avg_mitigated)

        season.season_grade_data = (season.season_grade_dict['Kills'] * 2) + (season.season_grade_dict['Deaths'] * -1) + (season.season_grade_dict['Damage']) + (season.season_grade_dict['Effect'] * 2.5) + (season.season_grade_dict['Overkill'] / 4) + (season.season_grade_dict['Mitigated'])



    # takes in a list of PlayerSeason objects

class PlayerSeason:
    def __init__(self, player, season_count):
        self.season = season_count
        self.player = player
        self.game_count = player.games_played['This-Season']

        self.season_grade_dict = {'Kills' : 0, 'Deaths' : 0, 'Damage' : 0, 'Effect' : 0, 'Overkill' : 0, 'Mitigated' : 0,}
        self.season_grade_data = 0
        if self.game_count != 0:
            self.kills = player.kills / self.game_count
            self.deaths = player.deaths / self.game_count
            self.damage = player.damage_data['Total-Damage'] / self.game_count
            self.effect = player.damage_data['Tesseract'] / self.game_count
            self.overkill = player.damage_data['Overkill'] / self.game_count
            self.streak = player.kill_streak['Peak']
            self.mitigated = player.crit_data['Mitigated'] / self.game_count
            self.crit_pct = player.crit_data['Ratio']
            self.parry_pct = player.crit_data['P_Ratio']

    def print_kills_deaths(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
            f"Kills Per Game: {self.kills :.3f}\n"
            f"Deaths Per Game: {self.deaths :.3f}\n\n")

    def print_effect(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Total Effect: {self.effect :.3f}\n"
                    f"Overkill Effect: {self.overkill :.3f}\n\n")

    def print_streak(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Best Kill Streak: {self.streak}\n\n")

    def print_mitigated(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Damage Mitigated Per Game: {self.mitigated :.3f}\n\n")

    def print_damage(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Damage Dealt Per Game: {self.damage :.3f}\n\n")


    def print_player_season(self, filename=None):
        if not filename:
            print(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
             f"Season Grade: {round(self.season_grade_data, 3)}\n"
             f"Games Played: {self.player.games_played['This-Season']}\n"
             f"Kills Per Game: {self.kills :.3f}\n"
             f"Deaths Per Game: {self.deaths :.3f}\n"
             f"Damage Dealt Per Game: {self.damage :.3f}\n"
             f"Damage Mitigated Per Game: {self.mitigated :.3f}\n"
             f"Total Effect Per Game: {self.effect :.3f}\n"
             f"Overkill Effect Per Game: {self.overkill :.3f}\n"
             f"Best Kill Streak: {self.streak}\n\n")
        else:
            with open(filename, 'a') as p:
                p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                        f"Season Grade: {round(self.season_grade_data, 3)}\n"
                        f"Games Played: {self.player.games_played['This-Season']}\n"
                f"Kills Per Game: {self.kills :.3f}\n"
                f"Deaths Per Game: {self.deaths :.3f}\n"
                f"Damage Dealt Per Game: {self.damage :.3f}\n"
                f"Damage Mitigated Per Game: {self.mitigated :.3f}\n"
                        f"Total Effect Per Game: {self.effect :.3f}\n"
                        f"Overkill Effect Per Game: {self.overkill :.3f}\n"
                        f"Best Kill Streak: {self.streak}\n\n")

class Player:
    def __init__(self, tier, atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, name, team="None"):
        self.tier = tier
        self.delayed_atk = 0
        self.atk_dmg = atk_dmg
        self.atk_spd = atk_spd
        self.crit_pct = crit_pct
        self.crit_x = crit_x
        self.overkill_x = 3
        self.max_health = health
        self.health = health
        self.power = power
        self.spawn_time = spawn_time
        self.is_alive = True
        self.countdown = 0
        self.kills = 0
        self.crit_kills = 0
        self.deaths = 0
        self.age = 0
        self.name = name
        self.crit_dmg = crit_dmg
        self.crit_data = {'Hit' : 0, 'Miss' : 0, 'Ratio' : 0.0, 'Parry' : 0, 'P_Miss' : 0, "P_Ratio" : 0.0, "Mitigated" : 0.0}
        self.grade_data = 0
        self.grade_dict = {'Power' : 0, 'DPS' : 0, 'Critical-X' : 0, 'Critical-PCT' : 0, 'Health' : 0, 'Spawn' : 0, 'Kills' : 0, 'Deaths' : 0, 'Effect' : 0, 'Overkill' : 0, 'Mitigated' : 0, 'Damage' : 0}
        self.ratio = -1
        self.team = team
        self.dps = self.atk_dmg / self.atk_spd
        self.no_power = 0
        self.kill_streak = {'Current' : 0, 'Peak' : 0}
        self.damage_data = {'Tesseract' : 0.0, 'Total-Attacks' : 0, 'Total-Damage' : 0.0, 'Total-Delayed-Damage' : 0.0, 'Total-Delayed-X' : 0.0, 'Delayed-Count' : 0, 'Avg-Delayed-X' : 0.0, 'Avg-Delayed-Damage' : 0.0, 'Overkill' : 0.0, 'Overkill-Count' : 0}
        self.games_played = {'All' : 0, 'This-Season' : 0, 'Playoffs' : 0}
        self.game_stats = []

    def __str__(self):
        if self.deaths != 0:
            self.ratio = round((self.kills/self.deaths),4)
        if self.kills != 0:
            holder = f"{self.name}\n" \
            f"\t{self.team}\n"\
            f"Rating: {self.grade_data}\n" \
            f"({self.grade_dict['Kills'] :.3f} in kills, {self.grade_dict['Deaths'] :.3f} in deaths, {self.grade_dict['Effect'] :.3f} in total effect, {self.grade_dict['Overkill'] :.3f} in overkill effect, {self.grade_dict['Mitigated'] :.3f} in damage mitigated, {self.grade_dict['Damage'] :.3f} in damage output.)\n" \
            f"Attack Damage: {self.atk_dmg}\n" \
            f"Attack Speed: {self.atk_spd}\n" \
            f"Crit %: {self.crit_pct}\n" \
            f"Crit X: {self.crit_x}\n" \
            f"Health: {self.max_health}\n" \
            f"Power: {self.power}\n" \
            f"Spawn Time: {self.spawn_time}\n" \
            f"AGE: {self.age}\n" \
            f"KILLS: {self.kills}\n" \
            f"DEATHS: {self.deaths}\n" \
            f"RATIO: {self.ratio}\n" \
            f"CRITICAL HIT KILLS: {self.crit_kills}\n" \
            f"NON-CRIT KILLS: {self.kills-self.crit_kills}\n"
        else:
            holder = f"{self.name}\n" \
            f"\t{self.team}\n" \
            f"Rating: {self.grade_data}\n" \
            f"Attack Damage: {self.atk_dmg}\n" \
            f"Attack Speed: {self.atk_spd}\n" \
            f"Crit %: {self.crit_pct}\n" \
            f"Crit X: {self.crit_x}\n" \
            f"Health: {self.max_health}\n" \
            f"Power: {self.power}\n" \
            f"Spawn Time: {self.spawn_time}\n" \
            f"AGE: {self.age}\n"
        return holder

    def attack(self, defender):
        self.damage_data['Total-Attacks'] += 1
        damage = self.atk_dmg * (1 + self.delayed_atk)
        if self.delayed_atk > 0:
            self.damage_data['Total-Delayed-Damage'] += damage
            self.damage_data['Total-Delayed-X'] += self.delayed_atk
            self.damage_data['Delayed-Count'] += 1
        crit = False
        crit_roll = uniform(0, 1)
        if crit_roll <= self.crit_pct:
            damage *= self.crit_x
            crit = True
            if self.crit_data:
                self.crit_data['Hit'] += 1
        else:
            if self.crit_data:
                self.crit_data['Miss'] += 1

        parry_roll = uniform(0,1)
        if parry_roll <= defender.crit_pct:
            if defender.crit_data:
                defender.crit_data['Parry'] += 1
                defender.crit_data['Mitigated'] += damage
            damage = 0

        else:
            if defender.crit_data:
                defender.crit_data['P_Miss'] += 1
        defender.health -= damage
        self.damage_data['Total-Damage'] += damage
        if defender.health <= 0:
            defender.die()
            self.damage_data['Overkill'] += abs(3 * defender.health)
            self.damage_data['Overkill-Count'] += 1
            defender.deaths += 1
            if crit:
                self.crit_kills += 1
            self.kills += 1
            self.kill_streak['Current'] += 1
            self.delayed_atk = 0
            return True
        else:
            self.delayed_atk = 0
            return False

    def die(self):
        self.no_power += 1
        self.is_alive = False
        self.countdown = self.spawn_time
        if self.kill_streak['Current'] >= self.kill_streak['Peak']:
            self.kill_streak['Peak'] = self.kill_streak['Current']
        self.kill_streak['Current'] = 0

    def tesseract(self):
        self.damage_data['Tesseract'] += self.power
        return self.power

    def respawn(self):
        self.health = self.max_health
        self.is_alive = True

