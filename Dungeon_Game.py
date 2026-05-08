import random
from colors import * #for coloring the text
from enemies import * #mainly for enemy data, and to spawn random enemy in the dungeon floors

# DATA DICTIONARIES
ROLES = { 
    "Tank": {
        "hp": 150, 
        "atk": 15, 
        "def": 15,
        "skill": "Shield"
        },
    "DPS": {
        "hp": 120, 
        "atk": 25, 
        "def": 13,
        "skill": "Double Strike"
        },
    "Healer": {
        "hp": 105, 
        "atk": 12, 
        "def": 10,
        "skill": "Heal"
        }
}

SHOP_ITEMS = {
    "1": {
        "name": 
        "Health Potion", 
        "cost": 30, 
        "type": "potion"
        },
    "2": {
        "name": 
        "Iron Sword", 
        "cost": 50, 
        "type": "weapon", 
        "atk_buff": 10
     },
    "3": {
        "name": 
        "Iron Armor", 
        "cost": 50, 
        "type": "armor", 
        "def_buff": 5
        }
}

# FUNCTIONS 

#Function to display stats it loops to display all the stats 
def display_stats():
    print("\n===== PLAYER STATS =====")
    for stat, value in player.items():
     if stat == "hp":
        print(f"Hp: {player['hp']}/{player['max_hp']}")
     elif stat != "max_hp":
        print(f"{stat.capitalize()}: {value}")

#Function to choose roles loops until the player gives a valid choice
def choose_role():
    while True:
        print("\nChoose Your Class: 1. Tank | 2. DPS | 3. Healer")
        role = input("Enter choice: ")
        if role == "1": 
            return "Tank"
        if role == "2": 
            return "DPS"
        if role == "3": 
            return "Healer"
        print("Invalid choice!")

#function for shop 
def shop():
    print(f"\n--- Welcome to the Shop! (Gold: {player['gold']}) ---")
    for n, i in SHOP_ITEMS.items(): #n = is for the number (1. ----) i is placeholder for the item name and cost
        print(f"{n}. {i['name']} ({i['cost']} Gold)")
    print("4. Exit")
    
    #shopping for items it checks if you have enough gold to buy an item from the shop + it permanently adds the buffs depends on what the item you bought in the shop (Except for the healing potion)
    choice = input("Buy something? ")
    if choice in SHOP_ITEMS:
        item = SHOP_ITEMS[choice]
        if player["gold"] >= item["cost"]:
            player["gold"] -= item["cost"]
            if item["type"] == "potion":
                player["potions"] += 1
            elif item["type"] == "weapon":
                player["atk"] += item["atk_buff"]
            elif item["type"] == "armor":
                player["def"] += item["def_buff"]
            print(f"Purchased {item['name']}!")
        else:
            print("Not enough gold!")

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
            e_damage = max(1, enemy_atk - player["def"]) #the same as the one in the player side

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
    
def level_up():

    print(f"\n{GREEN}*** LEVEL UP! ***")

    player["max_hp"] += 20
    player["hp"] = player["max_hp"]

    player["atk"] += 3
    player["def"] += 2
    player["potions"] += 1


    print(f"{GREEN}Your stats increased!")
    print(f"{GREEN}+20 Max HP")
    print(f"{GREEN}+3 ATK")
    print(f"{GREEN}+2 DEF")
    print(f"{GREEN}+1 Potion")

#  START GAME
player_name = input("Enter your player name: ")
print("\033[0;35m-\033[0m" * 40)
print(f"        \033[0;35mWelcome to the Dungeon!\n             {player_name}!\033[0m")
print("\033[0;35m-\033[0m" * 40)

# call function choose_role to choose what role the player wants
player_role = choose_role()
current_floor = 1 #the dungeon starts on floor 1

# player stats
player = {
    "name": player_name,
    "role": player_role,
    "hp": ROLES[player_role]["hp"],
    "max_hp": ROLES[player_role]["hp"],
    "atk": ROLES[player_role]["atk"],
    "def": ROLES[player_role]["def"],
    "gold": 50,
    "potions": 3
}

# MAIN GAME LOOP
while current_floor <= 5:
    print(f"\n" + "="*20)
    print(f"   FLOOR {current_floor} HUB")
    print("="*20)
    
    # Check if its the final floor
    if current_floor == 5:
        print(f"{RED}!{RESET}" * 53)
        print(f"{RED}!!!   WARNING: YOU HAVE REACHED THE FINAL FLOOR   !!!{RESET}")
        print(f"{RED}!{RESET}" * 53)
        
        # Give the player a final choice: Fight or Shop (one last time)
        print("\n1. FACE THE FINAL BOSS\n2. Final Visit to Shop\n3. View Stats")
        final_choice = input("There is no turning back now. Choose: ")
        
        if final_choice == "1":
            f_name = spawn_final_boss() # Spawns the Dragon
            if battle(f_name, FINAL_BOSS_STATS): #player will battle the dragon 
                current_floor += 1
                continue 
        elif final_choice == "2":
            shop()
            continue # Returns to the Floor 5 "Warning" screen
        elif final_choice == "3":
            display_stats()
            continue

    # Menu for Floors 1-4
    print("1. Explore (Fight) | 2. Boss Altar | 3. Shop | 4. Stats | 5. Quit")
    move = input("What will you do? ")

    if move == "1":
        # 15% chance for a Boss to ambush you, 85% for a Normal enemy
        if random.random() < 0.15:
            print(f"\n{RED}!!! AMBUSH !!! A Boss was lurking in the shadows!{RESET}")
            e_name = spawn_boss_enemy()
            battle_success = battle(e_name, BOSS_STATS)
        else:
            e_name = spawn_normal_enemy()
            battle_success = battle(e_name, ENEMY_STATS)
            
        # If you won the battle (Normal or Boss)
        if battle_success:
            # 40% chance to find the stairs after any successful exploration
            if random.random() < 0.40: 
                current_floor += 1
                level_up()
                print(f"\n{BLUE}--- You found stairs! Descending to Floor {current_floor} ---{RESET}")
                
    elif move == "2":
        b_name = spawn_boss_enemy()
        if battle(b_name, BOSS_STATS):
            current_floor += 1
            level_up()
            print(f"\n--- BOSS DEFEATED! Moving to Floor {current_floor} ---")
    
    # to open shop 
    elif move == "3":
        shop()
    # display your current stats
    elif move == "4":
        display_stats()
    # exits the game (Ends the program)
    elif move == "5":
        print("Giving up so soon? Goodbye!")
        break

# Victory Message
if current_floor > 5:
    print(f"{GREEN}*{RESET}"*45)
    print(f"{GREEN}  CONGRATULATIONS! YOU HAVE CLEARED THE DUNGEON!{RESET}")
    print(f"{GREEN}*{RESET}"*45)