from sys import stdin, stderr, exit
from os.path import exists
from glob import glob
from time import sleep
import os
import pickle
import random

CHANCE_OF_OCCURENCE = 40 # chance in percent that a zombie appears
Z_MIN_HEALTH = 20 # minimum health status that zombie can have
Z_MAX_HEALTH = 60 # maximum health status that zombie can have
DAMAGE_VARIANCE = 0.2 # (+-) variance of weapon damage
CHANCE_OF_ESCAPE = 20 # chance of successfully escaping from a fight
HEALTH_MEDICINE = 25 # energy that medicine provides
HEALTH_FOOD = 10 # energy that food provides
HEALTH_WATER = 5 # energy that water provides
HEALTH_WILDBERRIES = 20 # energy that wild berries provide
FIGHT_DELAY = 1 # delay in fight sequence

# dic of possible health packs
healthDict = {'Medicine': HEALTH_MEDICINE, 'Food': HEALTH_FOOD, 'Water': HEALTH_WATER, 'WildBerries': HEALTH_WILDBERRIES}

# list of possible weapons
weaponList = list()
weaponList.append({'name': 'Bat', 'strength': 5, 'accuracy': 80})
weaponList.append({'name': 'Crossbow', 'strength': 50, 'accuracy': 40, 'ammo': 3})
weaponList.append({'name': 'Shotgun', 'strength': 40, 'accuracy': 60, 'ammo': 0})
weaponList.append({'name': 'Revolver', 'strength': 10, 'accuracy': 80, 'ammo': 0})
weaponList.append({'name': 'SniperRifle', 'strength': 50, 'accuracy': 90, 'ammo': 0})
weaponList.append({'name': 'Knife', 'strength': 20, 'accuracy': 90})
weaponList.append({'name': 'Nothing', 'strength':0, 'accuracy': 0})
weaponList.append({'name': 'Flea', 'strength': 0, 'accuracy': 25})
weaponList.append({'name': 'Bite', 'strength': 10, 'accuracy': 80})

# zombie weapon
zWeapon = [weapon for weapon in weaponList if weapon['name']=='Bite'][0]

def getAction():
    found = False
    action = raw_input("\n> ").lower().split()
    for word in action:
        if word in ActionsDic:
            ActionsDic.get(word, None)()
            found = True
    if not found:
        stderr.write('Your action was not recognized\n')
    return

def startGame():
    readTitle()

    global zombiesBool
    if raw_input('\nPress ENTER> ').lower() == 'no zombies':
        zombiesBool = False
        print '\nAll zombies have starved to re-death!'
        sleep(1)
    else:
        zombiesBool = True
    while (True):
        print "\nMain menu"
        print "---------\n"
        print "(N)ew game"
        print "(L)oad game"
        print "(Q)uit"
        choice = raw_input("\n> ")
        if (choice.lower() == "n"):
            initialize()
            break
        if (choice.lower() == "l"):
            loadGame()
            break
        if (choice.lower() == "q"):
            print "Have a nice day."
            exit(0)
        return

def initialize():
    global health, inventory, pWeapons, currentRoom, previousRoom, pickUpList
    health = 100
    inventory = dict()
    pWeapons = list()
    pWeapons.append([weapon for weapon in weaponList if weapon['name']=="Crossbow"][0])
    pWeapons.append([weapon for weapon in weaponList if weapon['name']=="Knife"][0])
    pWeapons.append([weapon for weapon in weaponList if weapon['name']=="Nothing"][0])
    pWeapons.append([weapon for weapon in weaponList if weapon['name']=="Flea"][0])
    previousRoom = "none"
    currentRoom = os.path.realpath(__file__).split('/') # Get current file location
    currentRoom.pop() # gets directory
    currentRoom.append('Rooms') # Navigate into the Rooms subcurrentRoom
    currentRoom.append('IntroStory') # Navigate to first room
    pickUpList = list()
    printDescription()
    return

def quitGame():
    print '\nWould you like to save your game?'
    answer = raw_input("\n> ").lower()
    if 'y' in answer:
        saveGame()
        print 'See you soon'
        exit(0)
    elif 'n' in answer:
        print 'You committed suicide'
        exit(0)
    else:
        stderr.write('Invalid input\n')
    return

def saveGame():
    global health, inventory, pWeapons, currentRoom, previousRoom, pickUpList
    print "Please enter a file name for your savegame."
    while (True):
        saveDir = (raw_input("\n> ")).strip('.sg') + '.sg'
        if (exists(saveDir)):
            print "Savegame already exists. Do you want to overwrite it?"
            if ('y' in raw_input("\n> ").lower()):
                break
            else:
                print "Choose another name."
        else:
            break
    with open(saveDir, 'w') as outFile:
        pickle.dump(health, outFile)
        pickle.dump(inventory, outFile)
        pickle.dump(currentRoom, outFile)
        pickle.dump(previousRoom, outFile)
        pickle.dump(pWeapons, outFile)
        pickle.dump(pickUpList, outFile)
    print 'Game saved!'
    return

def loadGame():
    global health, inventory, pWeapons, currentRoom, previousRoom, pickUpList
    fileList = glob('*.sg')
    fileList.sort()
    if (len(fileList) > 0):
        print "\nList of avaiable savegames:"
        print "---------------------------"
        i=1
        for fileName in fileList:
            print "(%d) %s" % (i, fileName)
            i += 1
        success = False
        while (success == False):
            print "\nPlease choose a savegame."

            invalidInt = True
            while(invalidInt):
                try:
                    invalidInt = False
                    saveNumber = int(raw_input("\n#> "))
                    savegame = fileList[saveNumber-1]
                except ValueError:
                    invalidInt = True
                    print "\nInput needs to be integer."

            if (exists(savegame)):
                with open(savegame) as inFile:
                    health = pickle.load(inFile)
                    inventory = pickle.load(inFile)
                    currentRoom = pickle.load(inFile)
                    previousRoom = pickle.load(inFile)
                    pWeapons = pickle.load(inFile)
                    pickUpList = pickle.load(inFile)
                success = True
            else:
                print "No such file."
        printDescription()
    else:
        print "Couldn't find any savegames. Starting a new game."
        initialize()
    return

def changeRoom():
    global previousRoom
    if (exists('/'.join(currentRoom) + '/Go')):
        with open (('/'.join(currentRoom) + '/Go'), 'r') as f:
            # print accessable rooms
            i = 1
            for line in f:
                print "(%d) %s" % (i, line.strip())
                i += 1
            roomNotFound = True
            # wait for player to enter valid room
            while (roomNotFound):
                f.seek(0)
                try:
                    choice = int(raw_input("\n#> "))
                    roomNotFound = not(choice in range(1,i))
                except ValueError:
                    print "Input needs to be integer."
                    continue
                if (roomNotFound):
                    print "No such room."
            i = 1
            f.seek(0)
            for line in f:
                if (i == choice):
                    nextRoom = line.strip()
                    break
                i += 1
            if zombiesBool:
                fight()
            previousRoom = currentRoom.pop() # remember previous room
            if (health <= 0):
                currentRoom.append('UserDied')
            else:
                currentRoom.append(nextRoom) # set new room
            printDescription() # print next description
    else:
        print "You can go nowhere from here."
    return

def goBack():
    global previousRoom
    if (previousRoom != "none"): # check for existence of previous room
        temppreviousRoom = currentRoom.pop() # remember previous room
        currentRoom.append(previousRoom) # set current room to last room
        previousRoom = temppreviousRoom # set new room
        printDescription() # print next description
    else:
        print "Sorry, you can not go back from here."
    return

def printDescription():
    print '\n---------------------------------------------'
    # Read room description
    with open(('/'.join(currentRoom) + '/Description'), 'r') as f:
        for line in f:
            print line.strip()

def lookAround():
    global status
    if (exists('/'.join(currentRoom) + '/Look')):
        with open(('/'.join(currentRoom) + '/Look'), 'r') as f:
            for line in f:
                # Change Items dictionary value for specified key
                item = line.strip()
                if (not (currentRoom[-1] + '_' + item in pickUpList)):
                    if (item.startswith('ammo')):
                        ammoString = item.split(':')
                        weaponName = ammoString[1]
                        amount = ammoString[2]
                        weaponFound = False
                        for weapon in pWeapons:
                            if (weaponName in weapon.values()):
                                pickUpList.append(currentRoom[-1] + '_' + item)
                                weapon['ammo'] += int(amount)
                                print "\nYou just found and picked up %d bullets for %s." % (int(amount), weaponName)
                                weaponFound = True
                                break
                        if (weaponFound == False):
                            print "You found bullets for %s, but you don't have this weapon so you just drop the bullets." % weaponName
                    elif (item.startswith('health')):
                        pickUpList.append(currentRoom[-1] + '_' + item)
                        healthString = item.split(':')
                        healthName = healthString[1]
                        if (healthName in inventory.keys()):
                            inventory[healthName] += 1
                        else:
                            inventory[healthName] = 1
                        print "\nYou just found %s." % (healthName)
                    elif (item.startswith('weapon')):
                        pickUpList.append(currentRoom[-1] + '_' + item)
                        weaponString = item.split(':')
                        weaponName = weaponString[1]
                        pWeapons.append([weapon for weapon in weaponList if weapon['name']==weaponName][0])
                        print "\nYou just found %s." % (weaponName)

    else:
        print "There's nothing to see here."
    return

def checkInventory():
    if (len(inventory) == 0):
        print "\nNo items in inventory."
    else:
        for item in inventory:
            print "%-20s: %s" % (item, inventory[item])
    return

def useHealthPack():
    global health, inventory
    if (len(inventory) == 0):
        print "\nNo items in inventory."
    else:
        print "\nWhich item would you like to use? (q to cancel)"
        for item in inventory:
            print "%-20s: %s" % (item, inventory[item])
        notFound = True
        while (notFound):
            choice = raw_input("\n> ")
            if (choice in inventory.keys()):
                if (inventory[choice] > 0):
                    notFound = False
                    inventory[choice] -= 1
                    health += healthDict[choice]
                    if (inventory[choice] == 0):
                        del inventory[choice]
            elif (choice.lower() == 'q'):
                break
            if (notFound):
                print "No such item."
    return

def helpMessage():
    print "\nYou can use the following commands:\n"
    print "room     : show and access available rooms"
    print "back     : go to last room"
    print "look     : look for items"
    print "save     : save game"
    print "quit     : quit (and save) game"
    print "inventory: show inventory items"
    print "use      : use inventory item"
    print "status   : show health status"
    print "help     : show this message"
    return

def readTitle():
    tempDir = os.path.realpath(__file__).split('/') # Get current file location
    tempDir.pop() # Removes program name from the list to get directory location
    with open('/'.join(tempDir) + '/Title', 'r') as f:
        for line in f:
            print line.strip()
    return

def showStatus():
    print "\nYour health status: %d" % health

def fight():
    global health, pWeapons, zWeapon
    occurence = (random.randint(1,100) <= CHANCE_OF_OCCURENCE)
    won = True
    if occurence:
        print("Oh my god! A bloodthirsty zombie!\n")
        zHealth = random.randint(Z_MIN_HEALTH, Z_MAX_HEALTH)
        turn = "Player";
        while (not ((zHealth <= 0) or (health <=0))):
            sleep(FIGHT_DELAY)
            print "\nplayer health: %d, zombie health: %d" % (health, zHealth)
            sleep(FIGHT_DELAY)
            if (turn == "Player"):
                weapon = chooseWeapon();
            else:
                weapon = zWeapon
            if (weapon['name'] == 'Flea'):
                print "\nYou're trying to flea"
                sleep(FIGHT_DELAY)
                if (random.randint(1,100) <= weapon['accuracy']):
                    print "... and got away safely."
                    break
                else:
                    print "... and couldn't escape."
                    damage = 0
            else:
                if ('ammo' in weapon.keys()):
                    weapon['ammo'] -= 1
                hit = (random.randint(1,100) <= weapon['accuracy'])
                if (hit):
                    variance = random.uniform(-DAMAGE_VARIANCE, DAMAGE_VARIANCE)
                    damage = weapon['strength'] + round(variance * weapon['strength'])
                    if (turn == "Player"):
                        print "\nYou're trying to attack with a %s" % weapon['name']
                        sleep(FIGHT_DELAY)
                        print "... and hit the zombie. Damage: %d" % (damage)
                    else:
                        print "\nThe zombie is trying to bite you."
                        sleep(FIGHT_DELAY)
                        print "and hit you. Damage: %d" % (damage)
                else:
                    if (turn == "Player"):
                        print "\nYou're trying to attack with a %s" % weapon['name']
                        sleep(FIGHT_DELAY)
                        print  "... and missed the zombie."
                    else:
                        print "\nThe zombie is trying to bite you."
                        sleep(FIGHT_DELAY)
                        print "... and missed you."
                    damage = 0
            if (turn == "Player"):
                zHealth = zHealth - damage
                turn = "Zombie"
            else:
                health = health - damage
                turn = "Player"
        # end of fight
        if (zHealth <= 0):
           print("You killed the zombie.")
           won = True
        elif (health <= 0):
           print("The zombie killed you.")
           won = False
    return

def chooseWeapon():
    global health, pWeapons, zWeapon
    validWeapon = False
    print("\n\nChoose your weapon to attack:")
    while(not validWeapon):
        print("You have the following weapons:\n")
        for weapon in pWeapons:
            if ('ammo' in weapon.keys()):
                print "%s (strength: %s, accuracy: %s, ammo: %s)" % (weapon['name'], weapon['strength'], weapon['accuracy'], weapon['ammo'])
            else:
                print "%s (strength: %s, accuracy: %s)" % (weapon['name'], weapon['strength'], weapon['accuracy'])
        choice = raw_input("\n> ")
        weapon = [weapon for weapon in pWeapons if weapon['name'].lower()==choice.lower()]
        if (len(weapon) == 1):
            weapon = weapon[0]
            if ('ammo' in weapon.keys()):
                if (weapon['ammo'] == 0):
                    print "No ammo!"
                else:
                    validWeapon = True
            else:
                validWeapon = True
        else:
            print "You don't have such weapon!"
    return weapon


ActionsDic = {'room': changeRoom, 'back': goBack, 'look': lookAround,
            'save': saveGame, 'quit': quitGame, 'inventory': checkInventory,
            'use': useHealthPack, 'help': helpMessage, 'status': showStatus}



