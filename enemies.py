from random import choice

# Normal Enemies Stats
ENEMY_STATS = {
    "Goblin": {
        "hp": 30,
        "atk": 5,
        "def": 3,
        "skill": "Club Smack",
        "gold": 10,
        "loot": "Health Potion"
    },
     "Slime": {
        "hp": 40,
        "atk": 8,
        "def": 2,
        "skill": "Slimy Bite",
        "gold": 20,
        "loot": "Health Potion"
    },
     "Orc": {
        "hp": 50,
        "atk": 15,
        "def": 10,
        "skill": "Heavy Chop",
        "gold": 40,
        "loot": "Health Potion"
    },
     "Wolf": {
        "hp": 40,
        "atk": 10,
        "def": 2,
        "skill": "Bite",
        "gold": 30,
        "loot": "Health Potion"
    },
     "Ogre": {
        "hp": 60,
        "atk": 15,
        "def": 10,
        "skill": "Head Smash",
        "gold": 50,
        "loot": "Health Potion"
    }
}

# Boss Enemies Stats
BOSS_STATS = {
    "King Goblin": {
        "hp": 100,
        "atk": 25,
        "def": 10,
        "skill": "Iron Cleave",
        "gold": 100,
        "loot": "Iron Sword"
    },
    "Uruk-hai": {
        "hp": 150,
        "atk": 25,
        "def": 15,
        "skill": "Bone Crusher",
        "gold": 200,
        "loot": "Health Potion"
    },
    "Alpha Wolf": {
        "hp": 150,
        "atk": 25,
        "def": 15,
        "skill": "Alpha Bite",
        "gold": 200,
        "loot": "Iron Armor"
    },
}
# Final boss (Floor 5 only)
FINAL_BOSS_STATS = {
    "The Shadow Dragon": {
        "hp": 200,
        "atk": 28,
        "def": 17,
        "skill": "Shadow Breath",
        "gold": 1000,
        "loot": "Dragon Egg"

    }
}

def spawn_final_boss():
    return "The Shadow Dragon"

def spawn_normal_enemy():
    N_enemy = choice(list(ENEMY_STATS.keys()))
    return N_enemy

def spawn_boss_enemy():
    B_enemy = choice(list(BOSS_STATS.keys()))
    return B_enemy



