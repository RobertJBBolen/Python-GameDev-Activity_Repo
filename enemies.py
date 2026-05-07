from random import choice

# Normal Enemies Stats
ENEMY_STATS = {
    "Goblin": {
        "hp": 30,
        "atk": 5,
        "def": 3,
        "gold": 10
    },
     "Slime": {
        "hp": 40,
        "atk": 8,
        "def": 2,
        "gold": 20
    },
     "Orc": {
        "hp": 50,
        "atk": 15,
        "def": 10,
        "gold": 40
    },
     "Wolf": {
        "hp": 40,
        "atk": 10,
        "def": 2,
        "gold": 30
    },
     "Ogre": {
        "hp": 60,
        "atk": 15,
        "def": 10,
        "gold": 50
    }
}

# Boss Enemies Stats
BOSS_STATS = {
    "King Goblin": {
        "hp": 100,
        "atk": 25,
        "def": 10,
        "gold": 100
    },
    "Uruk-hai": {
        "hp": 150,
        "atk": 25,
        "def": 15,
        "gold": 200
    },
    "Alpha Wolf": {
        "hp": 150,
        "atk": 25,
        "def": 15,
        "gold": 200
    },
}
# Final boss (Floor 5 only)
FINAL_BOSS_STATS = {
    "The Shadow Dragon": {
        "hp": 300,
        "atk": 40,
        "def": 20,
        "gold": 1000
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



