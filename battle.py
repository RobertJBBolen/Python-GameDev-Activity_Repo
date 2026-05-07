from Dungeon_Game import *
from colors import *
from enemies import *
from random import *

# function for both enemy and player action (Attack, Drink potion and run)
def battle(enemy_name, stats_dict):
    #variables for the enemy stats (When called it should return back with an enemy name and stats for the enemy)
    enemy_hp = stats_dict[enemy_name]["hp"]
    enemy_atk = stats_dict[enemy_name]["atk"]
    enemy_def = stats_dict[enemy_name]["def"]
    enemy_gold = stats_dict[enemy_name]["gold"]
    
    # Combat States 
    is_blocking = False
    is_dodging = False
    is_parrying = False

    print(f"\n{RED}!!! A {enemy_name} appeared !!!{RESET}")

    #it will loop aslong as the enemy and player are still alive
    while enemy_hp > 0 and player["hp"] > 0:
        print(f"\n{RED}{enemy_name}: {enemy_hp} HP{RESET} | {GREEN}{player['name']}: {player['hp']} HP{RESET}")
        
        # Display Menu depending on which Role was picked
        if player["role"] == "Healer":
            print(f"{YELLOW}1. Attack | 2. Heal (Skill) | 3. Dodge | 4. Potion{RESET}")
        elif player["role"] == "DPS":
            print(f"{YELLOW}1. Attack | 2. Parry (Skill) | 3. Dodge | 4. Potion{RESET}")
        elif player["role"] == "Tank":
            print(f"{YELLOW}1. Attack | 2. Block (Skill) | 3. Dodge | 4. Potion{RESET}")
        
        action = input("Choose action: ")

        # Reset states each turn
        is_blocking = is_dodging = is_parrying = False

        # normal attack 
        if action == "1":
            damage = max(1, player["atk"] - enemy_def) #the function max is used for comparing which is bigger in this case if ever the atk - def became a negative number it will automatically do 1 dmg since 1 > negative number
            enemy_hp -= damage
            print(f"{CYAN}You dealt {damage} damage!{RESET}")
            
        elif action == "2": # SPECIAL SKILLS for each roles
            if player["role"] == "Healer":
                heal = 25
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                print(f"{GREEN}You cast Heal! Restored {heal} HP.{RESET}")
            elif player["role"] == "DPS":
                print(f"{MAGENTA}You prepare to Parry! (High chance to reflect damage){RESET}")
                is_parrying = True
            elif player["role"] == "Tank":
                print(f"{BLUE}You hide down behind your shield! (Massive defense){RESET}")
                is_blocking = True

        elif action == "3": # DODGE (Available to everyone)
            print(f"{CYAN}You focus on dodging the next attack...{RESET}")
            is_dodging = True

        elif action == "4": # POTION
            if player["potions"] > 0:
                player["hp"] = min(player["max_hp"], player["hp"] + 40)
                player["potions"] -= 1
                print(f"{GREEN}Used Potion! HP: {player['hp']}{RESET}")
            else:
                print(f"{RED}No potions left!{RESET}")
                continue
        else:
            print("Invalid choice!")
            continue

        # ENEMY TURN
        if enemy_hp > 0:
            e_damage = max(1, enemy_atk - player["def"])

            # DODGE has Standard 50/50 Chance
            if is_dodging:
                if random.random() < 0.50:
                    print(f"{CYAN}WHOOSH! You dodged the attack!{RESET}")
                    e_damage = 0
                else:
                    print(f"{RED}Dodge failed!{RESET}")

            # BLOCK Tank Guaranteed but partial dmg can still go through
            elif is_blocking:
                e_damage = e_damage // 5
                print(f"{BLUE}CLANG! Your shield absorbed the impact.{RESET}")

            # PARRY DPS has a high atk reward but high risk and low chance to succeed
            elif is_parrying:
                # Lowered to 35% chance
                if random.random() < 0.35:
                    counter_dmg = player["atk"] # Deals full attack damage back
                    enemy_hp -= counter_dmg
                    print(f"{MAGENTA}PERFECT PARRY! You deflected the hit and countered for {counter_dmg}!{RESET}")
                    e_damage = 0
                else:
                    # Failed parry makes you take 1.2x more damage
                    e_damage = int(e_damage * 1.2)
                    print(f"{RED}PARRY FAILED! You left yourself wide open!{RESET}")

            # Apply final damage of the enemy to player
            player["hp"] -= e_damage
            if e_damage > 0:
                print(f"{RED}The {enemy_name} hits you for {e_damage} damage!{RESET}")

    # player dies 
    if player["hp"] <= 0:
        print(f"\n{RED}YOU HAVE BEEN DEFEATED.{RESET}")
        exit()
    # player wins 
    else:
        print(f"\n{GREEN}Victory! Found {enemy_gold} gold.{RESET}")
        player["gold"] += enemy_gold
        return True