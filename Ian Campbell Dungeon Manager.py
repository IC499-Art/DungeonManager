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
    
    def status(self):
        print(f"{self.name}: {self.cHealth}/{self.mHealth} health, {self.cMana}/{self.mMana} mana")
    def isAlive(self):
        if self.cHealth > 0:
            return(True)

    def strike(self, target):
        damage = self.power
        if target.block == True:
            damage /= target.shield
            round(damage)
        damage -= target.defense
        target.cHealth -= damage
        print(f"{self.name} deals {damage} damage to {target.name}!")

    def healthRegen(self, amount):
        self.cHealth += amount
        if self.cHealth > self.mHealth:
            self.cHealth = self.mHealth
    
    def manaRegen(self, amount):
        self.cMana += amount
        if self.cMana > self.mMana:
            self.cMana = self.mMana
    
    def defend(self):
        self.block = True
        self.manaRegen(1)
        print(f"{self.name} defends!")
    
    def bleed(self):
        if self.bleedStacks > 0:
            self.cHealth -= self.bleedDamage
            self.bleedStacks -= 1
            print(f"{self.name} bled for {self.bleedDamage} damage!")
            if self.bleedStacks == 0:
                self.bleedDamage = 0
                print(f"{self.name} stopped bleeding!")
    
    def turnStart(self):
        alive = self.isAlive
        if alive == True:    
            self.manaRegen(1)
            self.block = False
            self.bleed()
            self.status()
            return(True)
        else:
            print(f"{self.name} is dead!")
            return(False)
        

#Player Classes:
class Berserker(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
        self.manaCost = 3
    def rend(self, target):
        self.cMana -= self.manaCost
        damage = self.power
        if target.block == True:
            damage /= target.shield
            round(damage)
        damage -= target.defense
        target.cHealth -= damage
        print(f"{self.name} tears into {target.name} for {damage} damage!")
        target.bleedStacks += 2
        target.bleedDamage += round(damage / 2)
        print(f"{target.name} is bleeding!")    
    def action(self, target):
        print("What will you do?: ")
        choice = int(input("1: Attack \n2: Block\n3: Rend (3 Mana)\n1-3: "))
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
        print(f"{self.name}:")
        print(f"Health Points: {self.cHealth}/{self.mHealth}")
        print(f"Max Mana: {self.mMana}")
        print(f"Attack Power: {self.power}")
        print(f"Defense: {self.defense}")
        print(f"Special Attack: \n Rend: Causes the target to bleed for two turns.")

#Enemy Types:
class Goblin(Character):
    def __init__(self, name, health, attack, defense, mana):
        super().__init__(name, health, attack, defense, mana)
    def actionSelect(self):
        self.choice = random.randint(1, 8)
        if self.choice >= 5:
            print(f"{self.name} takes an aggressive stance.")
        elif self.choice >= 2:
            self.defend()
            print(f"{self.name} raises its guard!")
        else:
            print(f"{self.name} looks lost.")         
    def action(self, target):
        if self.choice >= 5:
            self.strike(target)
        else:
            print(f"{self.name} wasted the turn.") 
    
        

#Character Creation:
realjob = 0
while realjob == 0:
    realjob = 1
    job = int(input("Choose your class:\n 1. Berserker\n 1-1: "))
if job == 1:
    player = Berserker(input("Name your Character: "), 50, 10, 0, 5)
else:
    print("Please choose a number from the list.")
    realjob = 0

def combat(player):
    #Combat Initiation:
    enemyList = [Goblin("Goblin Joe", 30, 6, 1, 0)]
    enemy = random.choice(enemyList)
    print(f"{player.name} is attacked by {enemy.name}!")
    #Combat Loop:
    battleEnd = 0
    while battleEnd == 0:
        eAlive = enemy.turnStart()
        if eAlive == True:
            enemy.actionSelect()
            pAlive = player.turnStart()
            if pAlive == True:
                player.action(enemy)
                enemy.action(player)
            else: battleEnd = 2
        else: 
            battleEnd = 1
            if player.cHealth <= 0:
                player.cHealth = 1
    if battleEnd == 1: 
        print("Victory!")
        return(0)
    if battleEnd == 2:
        print("Game Over!")
        return(1)
        

   



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
        quit = combat()
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    else:
        confirm = str.lower(input("Are you sure you want to quit? y/n: "))
        if confirm == "y":
            quit = 1
