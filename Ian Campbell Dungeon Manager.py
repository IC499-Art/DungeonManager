



class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.maxHealth = health
        self.curHealth = health
        self.attack = attack
        self.defense = defense
    def basicAttack(self, target):
        damage = self.attack
        if target.block == True:
            damage /= 2
        damage -= target.defense
        target.curHealth -= damage
        print(f"{self.name} deals {damage} damage to {target.name}!")

class Berserker(Character):
    def __init__(self, name, health, attack, defense):
        super().__init__(name, health, attack, defense)
    def rend(self, target):
        damage = self.attack
        if target.block == True:
            damage /= 2
        damage -= target.defense

#Character Creation


#Main Menu
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
        pass
    elif choice == 2:
        pass
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
