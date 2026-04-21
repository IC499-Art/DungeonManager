import random
import time
import os


class Character:
    def __init__(self, name, health, attack, defense, mana):
        self.name = name
        self.mHealth = health
        self.cHealth = health
        self.power = attack
        self.defense = defense
        self.block = False
        self.shield = 2
        self.mMana = mana
        self.cMana = 0
        self.bleedStacks = 0
        self.bleedDamage = 0
        self.wPoison = 0
        self.poisonStacks = 0
        self.pTypes = ["Health", "Mana", "Poison"]
        self.pDesc = ["Restore a large portion of Health.", "Start next battle with full Mana.", "Poison weapon for next battle."]
        self.pQuant = [0, 0, 0]
    
    def status(self):
        print(f"{self.name}: {self.cHealth}/{self.mHealth} health, {self.cMana}/{self.mMana} mana")
    def isAlive(self):
        if self.cHealth > 0:
            return True
        else:
            print(f"{self.name} is dead!")

    def strike(self, target):
        damage = self.power
        if target.block == True:
            damage /= target.shield
            damage = round(damage)
        damage -= target.defense
        target.cHealth -= damage
        print(f"{self.name} deals {damage} damage to {target.name}!")
        if self.wPoison > 1:
            target.poisonStacks += self.wPoison
            print(f"{self.name} poisons {target.name}!")
        return damage

    def hRegen(self, amount):
        self.cHealth += amount
        self.cHealth = round(self.cHealth)
        if self.cHealth > self.mHealth:
            self.cHealth = self.mHealth
    
    def mRegen(self, amount):
        self.cMana += amount
        if self.cMana > self.mMana:
            self.cMana = self.mMana
    
    def defend(self):
        self.block = True
        self.mRegen(2)
        print(f"{self.name} defends!")
    
    def bleed(self):
        if self.bleedStacks > 0:
            self.cHealth -= self.bleedDamage
            self.bleedStacks -= 1
            print(f"{self.name} bleeds for {self.bleedDamage} damage!")
            if self.bleedStacks == 0:
                self.bleedDamage = 0
                print(f"{self.name} stops bleeding!")
    
    def poison(self):
        if self.poisonStacks > 0:
            self.cHealth -= self.poisonStacks
            print(f"{self.name} takes {self.poisonStacks} damage from poison!")
            self.poisonStacks -= 1
            if self.poisonStacks == 0:
                print(f"{self.name} is no longer poisoned!")
            

    def turnStart(self):
        alive = self.isAlive()
        if alive == True:    
            self.mRegen(1)
            self.block = False
            self.bleed()
            self.poison()
            self.status()
            return self.isAlive()
        else:
            return(False)
    def battleWon(self):
        if self.cHealth <= 0:
            self.cHealth = 1
        self.bleedStacks = 0
        self.poisonStacks = 0
        self.wPoison = 0
        

#Player Classes:
class Berserker(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.manaCost = 4
        self.level = 1
    def rend(self, target):
        self.cMana -= self.manaCost
        damage = self.strike(target)
        print(f"{self.name} tears into {target.name}!")
        target.bleedStacks += 2
        target.bleedDamage += round(damage / 2)
        print(f"{target.name} is bleeding!")    
    def action(self, target):
        print("What will you do?: ")
        choice = int(input(f"1: Attack \n2: Block\n3: Rend (Costs {self.manaCost} Mana)\n1-3: "))
        if choice == 1:
            self.strike(target)
        elif choice == 2:
            self.defend()
        elif choice == 3:
            if self.cMana >= self.manaCost:
                self.rend(target)
            else:
                print(f"{self.name} tried, but didn't have the Mana.")
        else:
            print(f"{self.name} couldn't choose, and wasted the turn.")
    def charsheet(self):
        print(f"{self.name}: Level {self.level} Berserker")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}")
        print(f"Special Attack: \n Rend: Causes the target to bleed for two turns.")

class Assassin(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.manaCost = 3
        self.level = 1
    def pDart(self, target):
        self.strike(target)
        target.poisonStacks += (self.cMana - 1)
        self.cMana = 0
        print(f"{target.name} is poisoned!")  
    def action(self, target):
        print("What will you do?: ")
        choice = int(input(f"1: Attack \n2: Block\n3: Poison Dart (Costs at least {self.manaCost} Mana)\n1-3: "))
        if choice == 1:
            self.strike(target)
        elif choice == 2:
            self.defend()
        elif choice == 3:
            if self.cMana >= self.manaCost:
                self.pDart(target)
            else:
                print(f"{self.name} tried, but didn't have the Mana.")
        else:
            print(f"{self.name} couldn't choose, and wasted the turn.")
    def charsheet(self):
        print(f"{self.name}: Level {self.level} Assaassin")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}")
        print(f"Special Attack: \n Poison Dart: Afflicts the target with poison relative to Mana spent.")

class Paladin(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.manaCostA = 2
        self.manaCostB = 7
        self.level = 1
    def smite(self, target):
        damage = self.strike(target)
        holyDamage = damage + self.cMana
        target.cHealth -= holyDamage
        print(f"Holy light scorches {target.name} for {holyDamage} damage!")
        self.cMana = 0  
    def healPrayer(self):
        misHealth = (self.mHealth - self.cHealth)
        self.hRegen(misHealth*0.7)
        self.cMana -= self.manaCostB
        self.bleedStacks = 0
        self.poisonStacks = 0
        print(f"{self.name}'s wounds close!")
    def action(self, target):
        print("What will you do?: ")
        choice = int(input(f"1: Attack \n2: Block\n3: Smite (Costs at least {self.manaCostA} Mana)\n4: Heal Prayer (Costs {self.manaCostB} Mana)\n1-3: "))
        if choice == 1:
            self.strike(target)
        elif choice == 2:
            self.defend()
        elif choice == 3:
            if self.cMana >= self.manaCostA:
                self.smite(target)
            else:
                print(f"{self.name} tried, but didn't have the Mana.")
        elif choice == 4:
            if self.cMana >= self.manaCostB:
                self.healPrayer()
            else:
                print(f"{self.name} tried, but didn't have the Mana.")  
        else:
            print(f"{self.name} couldn't choose, and wasted the turn.")
    def charsheet(self):
        print(f"{self.name}: Level {self.level} Paladin")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}")
        print(f"Special Attack: \n Smite: Scorch the target with holy light, piercing defenses.")
        print(f"Spell: \n Heal Prayer: Restores {self.name}'s health, and cures bleed and poison.")       


#Enemy Types:
class Goblin(Character):
    def __init__(self, name, health, attack, defense, mana, aggro):
        super().__init__(name, health, attack, defense, mana)
        self.aggro = aggro
        self.manaCost = 4
    def rend(self, target):
        self.cMana -= self.manaCost
        damage = self.strike(target)
        print(f"{self.name} tears into {target.name}!")
        target.bleedStacks += 2
        target.bleedDamage += round(damage / 2)
        print(f"{target.name} is bleeding!")    
    def actionSelect(self):
        self.choice = random.randint(1, self.aggro)
        if self.choice >= 5:
            print(f"{self.name} takes an aggressive stance.")
        elif self.choice >= 2:
            self.defend()
        else:
            print(f"{self.name} looks lost.")         
    def action(self, target):
        if self.choice >= 8:
            if self.cMana >= self.manaCost:
                self.rend(target)
            else:
                print(f"{self.name} tries to rend {target.name}, but doesn't have the Mana.")
        elif self.choice >= 5:
            self.strike(target)


        
#Inventory
def showInv(player):
    print("Potion Types:")
    for item in range(len(player.pTypes)):
        print(f"{player.pTypes[item]}: {player.pQuant[item]} owned.")
        print(f"-{player.pDesc[item]}")

def useItem(player):
    showInv(player)
    choice = str.capitalize(input("Which potion do you want to use? Type the name of the potion, or hit enter to skip: "))
    for item in range(len(player.pTypes)):
        if choice == player.pTypes[item]:
            if player.pQuant[item] > 0:
                player.pQuant[item] -= 1
                if choice == "Health":
                    player.hRegen(player.mHealth/2)
                    print(f"{player.name} regained Health!")
                if choice == "Mana":
                    player.mRegen(player.mMana)
                    print(f"{player.name}'s Mana was maxed out!")
                if choice == "Poison":
                    if player.wPoison == 0:
                        player.wPoison += 2
                        print(f"{player.name} poisoned their weapon!")
                    else:
                        player.wPoison += 1
                        print(f"{player.name} added more poison to their weapon.")
            else:
                print(f"{player.name} doesn't have any of those.")


def Loot(player):
    loot = random.randint(1, 7)
    if loot >= 4:
        potion = random.choice(range(len(player.pTypes)))
        player.pQuant[potion] += 1
        print(f"{player.name} found a {player.pTypes[potion]} Potion!")
    elif loot >= 3:
        player.defense += 1
        print(f"{player.name} found an armor upgrade! Defense +1!")
    else:
        player.mMana += 1
        print(f"{player.name} found a Mana enchantment! Max Mana +1!")

#Leveling

def LevelUp(player):
    player.level += 1
    print(f"{player.name} reached level {player.level}")
    valid = 0
    while valid == 0:
        valid = 1
        choice = int(input("What do you want to upgrade?\n 1: +5 Health\n 2: +1 Attack Power\n 3: +1 Mana\n 1-3: "))
        if choice == 1:
            player.mHealth += 5
            player.cHealth += 5
            print("Health upgraded.")
        elif choice == 2:
            player.power += 1
            print("Power upgraded.")
        elif choice == 3:
            player.mMana += 1
            print("Mana upgraded.")
        else:
            valid = 0
            print("Please type 1, 2, or 3 to select one of the given options.")
    

#Combat

def spawnEnemy(tier, difficulty):
    if tier == 1:
        minionList = [Goblin("Goblin", 30, 6, 1, 4, 8)]
        enemy = random.choice(minionList)    
    elif tier == 2: 
        bossList = [Goblin("Bob Goblin", 50, 6, 2, 7, 10)]
        enemy = random.choice(bossList)
    elif tier == 3:
        summon = random.randint(1, 1)
        if summon == 1:
            enemy = Goblin("Gobert the Terrible", 60, 7, 3, 9, 10)
            enemy.wPoison = 2          
    else:
        enemy = Goblin("Dead Goblin", 0, 6, 1, 0, 0)
    
    if difficulty >= 12:
        hScaling = ((difficulty - 10) * 0.1) + 1
        pScaling = (difficulty - 10)
        enemy.mHealth = round(enemy.mHealth * hScaling)
        enemy.cHealth = round(enemy.cHealth * hScaling)
        enemy.power += pScaling
    return enemy

def combat(player, tier, difficulty):
    #Combat Initiation:
    enemy = spawnEnemy(tier, difficulty)
    print(f"{player.name} is attacked by {enemy.name}!")
    time.sleep(1)
    #Combat Loop:
    battleEnd = 0
    while battleEnd == 0:
        eAlive = enemy.turnStart()
        if eAlive == True:
            enemy.actionSelect()
            time.sleep(2)
            pAlive = player.turnStart()
            if pAlive == True:
                player.action(enemy)
                time.sleep(1)
                enemy.action(player)
            else: battleEnd = 2
        else: 
            battleEnd = 1
    time.sleep(2)
    if battleEnd == 1: 
        print("Victory!")
        time.sleep(2)
        player.battleWon()
        for count in range(tier):
            Loot(player)
        for count in range(tier):
            LevelUp(player)
        player.cMana = 0
        return(0)
    if battleEnd == 2:
        print("Game Over!")
        return(1)
        

#Character Creation:
realjob = 0
while realjob == 0:
    realjob = 1
    job = int(input("Choose your class:\n 1. Berserker\n 2. Assassin\n 3. Paladin\n 1-3: "))
if job == 1:
    player = Berserker(input("Name your Character: "), 50, 8, 0, 7)
elif job == 2:
    player = Assassin(input("Name your Character: "), 40, 10, 0, 6)
elif job == 3:
    player = Paladin(input("Name your Character: "), 50, 7, 2, 7)
else:
    print("Please choose a number from the list.")
    realjob = 0

#Main Menu:
quit = 0
while quit == 0:
    print("Options: \n " +
          "1. View Character \n " +
          "2. Explore Dungeon \n " + 
          "3. View Inventory \n " +
          "4. Save Game \n " + 
          "5. Load Game \n " +
          "6. Exit")
    choice = int(input("What will you do? 1-6: "))
    if choice == 1:
        player.charsheet()
    elif choice == 2:
        difficulty = 6 + player.level
        event = random.randint(1, difficulty)
        if event >= 15:
            quit = combat(player, 3, difficulty)
        elif event >= 10:
            quit = combat(player, 2, difficulty)
        elif event >= 6:
            print(f"{player.name} discovered a treasure chest! ")
            Loot(player)
        else:    
            quit = combat(player, 1, difficulty)
    elif choice == 3:
        useItem(player)
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    else:
        confirm = str.lower(input("Are you sure you want to quit? y/n: "))
        if confirm == "y":
            quit = 1
