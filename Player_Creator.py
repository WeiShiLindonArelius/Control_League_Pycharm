from Players import Player
from random import randint, choice, uniform
names = [
  "Aria", "Ashton", "Amara", "Ari", "Anya",
  "Bryce", "Brennan", "Briar", "Brodie",
  "Calla", "Cameron", "Carson", "Cassius", "Chase",
  "Dakota", "Darcy", "Dallas", "Darian", "Devin",
  "Ellis", "Elliott", "Emery", "Eris", "Evelyn",
  "Finley", "Flynn", "Finnegan", "Felicity", "Freya",
  "Gia", "Gael", "Gwen", "Gunnar", "Giselle",
  "Harlow", "Harper", "Hayden", "Hadley", "Hunter",
  "Iris", "Indiana", "Isadora", "Isla", "Imogen",
  "Jude", "Jordan", "Jax", "Jasper", "Jocelyn",
  "Kai", "Carter", "Keegan", "Kendall", "Kyra",
  "Lennon", "Linden", "Landon", "Logan", "Lorelei",
  "Madden", "Marley", "Maddox", "Mason", "Mila",
  "Nova", "Nash", "Nico", "Nolan", "Naya",
  "Oakley", "Odessa", "Orion", "Oliver", "Ophelia",
  "Parker", "Phoenix", "Presley", "Paxton", "Primrose",
  "Quinn", "Quincy", "Quest", "Queenie", "Quinten",
  "Rowan", "Reagan", "Reeve", "Raven", "Ryder",
  "Sage", "Sawyer", "Saylor", "Sutton", "Sparrow",
  "Tatum", "Tanner", "Tate", "Theo", "Tilly",
  "Urban", "Uriel", "Ulysses", "Umberto", "Una",
  "Vesper", "Vida", "Valentine", "Vance", "Verity",
  "Wren", "Weston", "Willow", "Wilder", "Winslow",
  "Xanthe", "Xander", "Ximena", "Xiomara", "Xena",
  "Yara", "Yasmine", "Yael", "Yvette", "Yvonne",
  "Zephyr", "Zara", "Zander", "Zeke", "Zelda", "Zain",
    "Killer", "Zoro", "Luffy", "Brook", "Nami"
]

def s_tier(amp=0):
    # Generate random integer values for each stat within the specified range for S tier
    atk_dmg = randint(45, 60)
    atk_spd = randint(6, 14)
    crit_pct = (randint(20, 50))/1000
    crit_x = randint(800, 1200)/100
    health = round(uniform(525,575),2)
    power = randint(55, 60) + int(amp)
    spawn_time = randint(10, 13)
    crit_dmg = atk_dmg*crit_x
    # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("S", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, f"S_{choice(names)}")
    else:
        return Player(f"S", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"S^{amp}_{choice(names)}")

def a_tier(amp=0):
    # Generate random integer values for each stat within the specified range for A tier
    atk_dmg = randint(45, 60)
    atk_spd = randint(7, 15)
    crit_pct = (randint(20, 45))/1000
    crit_x = randint(700, 1100)/100
    health = round(uniform(500,565),2) + round((25*amp),2)
    power = randint(50, 60)
    spawn_time = randint(10, 14)
    crit_dmg = atk_dmg * crit_x
    # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("A", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"A_{choice(names)}")
    else:
        return Player(f"A", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"A^{amp}_{choice(names)}")

def b_tier(amp=0):
    # Generate random integer values for each stat within the specified range for B tier
    atk_dmg = randint(40, 55)
    atk_spd = randint(8, 15) - int(amp/2)
    crit_pct = (randint(18,43))/1000
    crit_x = randint(500, 900)/100
    health = round(uniform(495,555),2)
    power = randint(45, 60)
    spawn_time = randint(11, 14) - int(amp/3)
    crit_dmg = atk_dmg * crit_x
    # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("B", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"B_{choice(names)}")
    else:
        return Player(f"B", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"B^{amp}_{choice(names)}")

def c_tier(amp=0):
    atk_dmg = randint(30, 52)
    atk_spd = randint(9, 16)
    crit_pct = ((randint(20, 50)) / 1000) + (amp * 0.01)
    crit_x = randint(1175, 1350)/100
    health = round(uniform(525,575),2)
    power = randint(40, 60)
    spawn_time = randint(11, 15)
    crit_dmg = atk_dmg * crit_x
            # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("C", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, f"C_{choice(names)}")
    else:
        return Player("C", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"C^{amp}_{choice(names)}")