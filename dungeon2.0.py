import random
import os
from colors import *
from enemies import *

# ─── ROLES ───────────────────────────────────────────────────────────────────

ROLES = {
    "Tank": {
        "hp":  150,
        "atk": 15,
        "def": 10
    },
    "DPS": {
        "hp":  100,
        "atk": 25,
        "def": 5
    },
    "Healer": {
        "hp":  85,
        "atk": 12,
        "def": 5
    }
}

# ─── FUNCTIONS ───────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def display_stats(player):
    print("\n===== PLAYER STATS =====")
    print(f"Name : {player['name']}")
    print(f"Role : {player['role']}")
    print(f"HP   : {player['hp']} / {player['max_hp']}")
    print(f"ATK  : {player['atk']}")
    print(f"DEF  : {player['def']}")
    print("=" * 25)

def choose_role():
    while True:
        print("\nChoose Your Role:")
        print("1. Tank   — HP:150  ATK:15  DEF:10")
        print("2. DPS    — HP:100  ATK:25  DEF:5")
        print("3. Healer — HP:85   ATK:12  DEF:5  (Can heal 25 HP in combat)")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            return "Tank"
        elif choice == "2":
            return "DPS"
        elif choice == "3":
            return "Healer"
        else:
            print(f"{RED}Invalid choice! Enter 1, 2, or 3.{RESET}")

def battle(player, enemy_name, stats_dict):
    enemy_hp  = stats_dict[enemy_name]["hp"]
    enemy_atk = stats_dict[enemy_name]["atk"]
    enemy_def = stats_dict[enemy_name]["def"]

    print(f"\n{RED}!!! A {enemy_name} appeared !!!{RESET}")

    while enemy_hp > 0 and player["hp"] > 0:
        print(f"\n{RED}{enemy_name}: {enemy_hp} HP{RESET} | {GREEN}{player['name']}: {player['hp']} HP{RESET}")

        # Show menu based on role
        if player["role"] == "Healer":
            print(f"{YELLOW}1. Attack | 2. Heal (+25 HP) | 3. Dodge{RESET}")
        else:
            print(f"{YELLOW}1. Attack | 2. Dodge{RESET}")

        action = input("Choose action: ").strip()
        is_dodging = False

        if action == "1":
            damage = max(1, player["atk"] - enemy_def)
            enemy_hp -= damage
            print(f"{CYAN}You dealt {damage} damage!{RESET}")

        elif action == "2" and player["role"] == "Healer":
            healed = min(25, player["max_hp"] - player["hp"])
            player["hp"] += healed
            print(f"{GREEN}You cast Heal! Restored {healed} HP.{RESET}")

        elif action == "2" and player["role"] != "Healer":
            print(f"{CYAN}You focus on dodging the next attack...{RESET}")
            is_dodging = True

        elif action == "3" and player["role"] == "Healer":
            print(f"{CYAN}You focus on dodging the next attack...{RESET}")
            is_dodging = True

        else:
            print(f"{RED}Invalid choice!{RESET}")
            continue

        # Enemy turn
        if enemy_hp > 0:
            e_damage = max(1, enemy_atk - player["def"])

            if is_dodging:
                if random.random() < 0.50:
                    print(f"{CYAN}WHOOSH! You dodged the attack!{RESET}")
                    e_damage = 0
                else:
                    print(f"{RED}Dodge failed!{RESET}")

            player["hp"] -= e_damage
            if e_damage > 0:
                print(f"{RED}The {enemy_name} hits you for {e_damage} damage!{RESET}")

    if player["hp"] <= 0:
        player["hp"] = 0
        print(f"\n{RED}YOU HAVE BEEN DEFEATED.{RESET}")
        return False
    else:
        print(f"\n{GREEN}Victory! The {enemy_name} has been slain!{RESET}")
        return True

# ─── START GAME ──────────────────────────────────────────────────────────────

player_name = input("Enter your player name: ").strip()
if not player_name:
    player_name = "Nameless One"

print("\033[0;35m-\033[0m" * 40)
print(f"        \033[0;35mWelcome to the Dungeon!\n             {player_name}!\033[0m")
print("\033[0;35m-\033[0m" * 40)

player_role = choose_role()

player = {
    "name":    player_name,
    "role":    player_role,
    "hp":      ROLES[player_role]["hp"],
    "max_hp":  ROLES[player_role]["hp"],
    "atk":     ROLES[player_role]["atk"],
    "def":     ROLES[player_role]["def"]
}

current_floor = 1

# ─── MAIN GAME LOOP ──────────────────────────────────────────────────────────

while current_floor <= 5:
    clear()

    # FLOOR 5 — FINAL FLOOR
    if current_floor == 5:
        print(f"{RED}{'!' * 53}{RESET}")
        print(f"{RED}!!!   WARNING: YOU HAVE REACHED THE FINAL FLOOR   !!!{RESET}")
        print(f"{RED}{'!' * 53}{RESET}")
        display_stats(player)

        print("\n1. Face the Final Boss")
        print("2. View Stats")
        print("3. Quit")
        final_choice = input("There is no turning back. Choose: ").strip()

        if final_choice == "1":
            f_name = spawn_final_boss()
            if battle(player, f_name, FINAL_BOSS_STATS):
                current_floor += 1
            else:
                break

        elif final_choice == "2":
            display_stats(player)
            input(f"\n{CYAN}Press Enter to continue...{RESET}")

        elif final_choice == "3":
            print("Giving up so soon? Goodbye!")
            break

        continue

    # FLOORS 1–4
    print(f"\n{'=' * 20}")
    print(f"   FLOOR {current_floor} HUB")
    print("=" * 20)
    display_stats(player)

    print("1. Explore (Fight)  |  2. Boss Altar  |  3. Stats  |  4. Quit")
    move = input("What will you do? ").strip()

    if move == "1":
        # 15% chance for a boss ambush
        if random.random() < 0.15:
            print(f"\n{RED}!!! AMBUSH !!! A Boss was lurking in the shadows!{RESET}")
            e_name = spawn_boss_enemy()
            won = battle(player, e_name, BOSS_STATS)
        else:
            e_name = spawn_normal_enemy()
            won = battle(player, e_name, ENEMY_STATS)

        if not won:
            break

        # 40% chance to find stairs after winning
        if random.random() < 0.40:
            current_floor += 1
            print(f"\n{BLUE}--- You found the stairs! Descending to Floor {current_floor} ---{RESET}")

    elif move == "2":
        b_name = spawn_boss_enemy()
        if battle(player, b_name, BOSS_STATS):
            current_floor += 1
            print(f"\n{BLUE}--- BOSS DEFEATED! Moving to Floor {current_floor} ---{RESET}")
        else:
            break

    elif move == "3":
        display_stats(player)
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

    elif move == "4":
        print("Giving up so soon? Goodbye!")
        break

    else:
        print(f"{RED}Unknown command.{RESET}")