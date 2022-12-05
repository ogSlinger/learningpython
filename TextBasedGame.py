class Room:
    roomNumber = 1
    roomItems = []

    def __init__(self, roomNumber):
        if not (0 <= roomNumber <= 8):
            raise Exception("Needs to be a valid room")
        self.roomItems = []
        self.roomNumber = roomNumber
        self.populate_items(roomNumber)

    def populate_items(self, currentRoom):
        if currentRoom == 0:
            self.roomItems.append("knife")
        if currentRoom == 2:
            self.roomItems.append("armor")
        if currentRoom == 5:
            self.roomItems.append("sword")
        if currentRoom == 6:
            self.roomItems.append("green orb")

    def list_items(self): #Returns a string of the items in a room with proper concatenation
        string = ''
        vowels = ["a", "e", "i", "o", "u"]
        if len(self.roomItems) >= 1:
            for i in range(len(self.roomItems)):
                if (i == len(self.roomItems) - 1) and (i != 0):
                    string += "and "
                if self.roomItems[i][0] in vowels:
                    string += "an "
                else:
                    string += "a "
                string += "".join(self.roomItems[i])
                if self.roomItems[i] == "armor":
                    string += " on a rack"
                if i != len(self.roomItems) - 1:
                    string += ", "
        else:
            string = "no items"
        return string

#######################################################################################################################

class Game:
    currentRoom = 0
    roomList = []
    doorList = []
    playerItems = ["torch"]
    torchState = False
    bossdoor = [""] * 3

    pedestalStates = {
        0: False,
        1: "yellow orb",
        2: False,
        3: "black orb",
        4: False,
        5: "blue orb",
        6: False,
        7: False
    }

    doorStates = {
        0: True,
        1: False,
        2: True,
        3: True,
        4: True,
        5: False,
        6: False
    }

    doorlocations = { #List cheat sheet: room #: direction:[Door exists?, Room it goes to, Door ID, obstructions?]
        0: {
            "N": False,
            "E": [True, 1, 0, ""],
            "S": False,
            "W": False
        },
        1: {
            "N": [True, 2, 1],
            "E": [True, 5, 4],
            "S": [True, 4, 3],
            "W": [True, 0, 0]
        },
        2: {
            "N": False,
            "E": [True, 3, 2, ""],
            "S": [True, 1, 1],
            "W": False
        },
        3: {
            "N": False,
            "E": False,
            "S": False,
            "W": [True, 2, 2],
        },
        4: {
            "N": [True, 1, 3],
            "E": [True, 7, 6],
            "S": False,
            "W": False
        },
        5: {
            "N": [True, 6, 5],
            "E": False,
            "S": False,
            "W": [True, 1, 4]
        },
        6: {
            "N": False,
            "E": False,
            "S": [True, 5, 4],
            "W": False
        },
        7: {
            "N": False,
            "E": False,
            "S": False,
            "W": [True, 4, 6]
        }
    }

    for i in range(8):
        roomList.append(Room(i))

    def __int__(self):
        self.currentRoom = 0

    def run(self):
        exitCode = 0
        while exitCode == 0:
            exitCode = self.display_menu()

    def display_menu(self):
        print("---------------------------")
        if self.torchState and self.currentRoom != 7:
            self.describe_room(self.currentRoom)
            self.describe_items()
            self.describe_pedestals()
            if self.currentRoom == 4:
                self.describe_boss_door()
        elif self.currentRoom != 7:
            print("It's too dark to see anything...")
        if self.currentRoom != 7:
            print("Choose One: [1]Pickup")
            print("            [2]Inventory")
            print("            [3]Move")
            print("            [4]Exit Game")
        else:
            return self.boss_encounter()
        actionNumber = 0
        while not (0 < int(actionNumber) < 5):
            actionNumber = int(input())
            if 0 < actionNumber < 5:
                return self.perform_action(actionNumber, self.playerItems)
            else:
                print("Input a real input: ")

    def perform_action(self, actionNumber, playerItems):
        if actionNumber == 2:  # Inventory
            self.check_inventory(playerItems)
            input("Press Enter to continue...")
            return 0
        elif actionNumber == 4:     #Exit
            if self.exit_game() == 1:
                print("exiting...")
                return 1
        if self.torchState == False:
            print("It's too dark to do anything...")
            return 0
        else:
            if actionNumber == 1:       #Pickup
                self.pickup()
                input("Press Enter to continue...")
                return 0
            elif actionNumber == 3:     #Move
                self.move()
                input("Press Enter to continue...")
                return 0

    def pickup(self):
        itemToPickup = input("What item would you like to pickup? ")
        if itemToPickup in self.roomList[self.currentRoom].roomItems:
            for index, itemToPickup in enumerate(self.roomList[self.currentRoom].roomItems):
                self.playerItems.append(itemToPickup)
                self.roomList[self.currentRoom].roomItems.pop(index)
                print("You picked up a", itemToPickup)
        elif self.pedestalStates[self.currentRoom]:
            if itemToPickup in self.pedestalStates[self.currentRoom]:
                print("You picked up a", itemToPickup)
                self.playerItems.append(itemToPickup)
                self.pedestalStates[self.currentRoom] = ""
                self.actuate_pedestal(itemToPickup)
        elif self.currentRoom == 4:
            self.remove_orb_boss_door(itemToPickup)
        if itemToPickup == "armor":
            self.actuate_door(2)
            self.actuate_door(3)
            print("You hear multiple doors moving.")

    def check_inventory(self, items):
        string = ''
        for i in range(len(self.playerItems)):
            if (i == len(self.playerItems) - 1) and (i != 0):
                string += "and "
            string += "a " + "".join(self.playerItems[i])
            if i != len(self.playerItems) - 1:
                string += ", "
        print("You have:", string)
        item = input("Which item do you want to use? ")
        while item not in self.playerItems:
            item = input("Enter a valid item: ")
        self.item_actions(item)

    def move(self):
        directions = ['N', 'E', 'S', 'W']
        moveDirection = str(input("In which direction? (Type N E S or W): ")).capitalize()
        while moveDirection not in directions:
            print('Enter a valid direction:')
            moveDirection = input()
        if self.door_checker(moveDirection):
            self.currentRoom = self.move_through_door(moveDirection)

    def exit_game(self):
        print("Are you sure? (Type 'Yes' or 'No'): ")
        sure = input()
        if sure.capitalize() == "YES":
            return 1

    def describe_room(self, currentRoom):
        if currentRoom == 0:
            print("There is a door to the east.")
        elif currentRoom == 1:
            print("There is a door to the north, east, south, and west. There is a pedestal in the room.")
        elif currentRoom == 2:
            print("There is a door to the east.")
        elif currentRoom == 3:
            print("There is a door to the west. There is a pedestal in the room.")
        elif currentRoom == 4:
            print("There is a giant door with a yellow, blue, and green sockets on it to the east.")
            print("There is a door to the north.")
        elif currentRoom == 5:
            print("There is a door to the north and west. There is a pedestal with black markings on it.")
        elif currentRoom == 6:
            print("There is a door to the south.")
        elif currentRoom == 7:
            print("BOSS ROOM")

    def describe_items(self):
        print(f"You see {self.roomList[self.currentRoom].list_items()} in the room.")

    def describe_pedestals(self):
        if self.pedestalStates[self.currentRoom]:
            print("There is ", end="")
            if self.pedestalStates[self.currentRoom] == "":
                print("nothing", end=" ")
            else:
                print(self.pedestalStates[self.currentRoom], end=" ")
            if self.currentRoom != 5:
                print("on a pedestal.")
            else:
                print("on a pedestal marked with black glyphs.")

    def door_checker(self, moveDirection):
        if self.doorlocations[self.currentRoom][str(moveDirection)]:
            if len(self.doorlocations[self.currentRoom][str(moveDirection)]) == 4:
                print("The door is obstructed with vines.")
            elif not self.doorStates[self.doorlocations[self.currentRoom][moveDirection][2]]:
                print("The door is closed")
            else:
                return True
        else:
            print("There is nothing there...")
            return False

    def move_through_door(self, moveDirection):
        print("You move through the doorway.")
        return self.doorlocations[self.currentRoom][moveDirection][1]

    def actuate_door(self, doorID):
        self.doorStates[doorID] = not self.doorStates[doorID]

    def actuate_pedestal(self, item):
        if self.currentRoom == 1:
            self.actuate_door(1)
            self.actuate_door(3)
            print("You hear something moving...")
        elif self.currentRoom == 3:
            self.actuate_door(2)
            print("You hear something moving...")
        elif self.currentRoom == 5:
            if item == "black orb":
                self.actuate_door(5)
                print("You hear something moving...")

    def item_actions(self, itemToUse):
        if itemToUse == "knife":
            if self.currentRoom == 0 and len(self.doorlocations[0]["E"]) == 4:
                print("You cut the vines obstructing the doorway.")
                self.doorlocations[0]["E"].pop(3)
            if self.currentRoom == 2 and len(self.doorlocations[2]["E"]) == 4:
                print("You cut the vines obstructing the doorway.")
                self.doorlocations[2]["E"].pop(3)
        elif itemToUse == "torch":
            self.torchState = not self.torchState
            print("You turn on the torch.")
        elif itemToUse == "yellow orb":
            self.place_orb_pedestal(itemToUse)
            self.place_orb_boss_door(itemToUse)
        elif itemToUse == "black orb":
            self.place_orb_pedestal(itemToUse)
            self.place_orb_boss_door(itemToUse)
        elif itemToUse == "blue orb":
            self.place_orb_pedestal(itemToUse)
            self.place_orb_boss_door(itemToUse)
        elif itemToUse == "green orb":
            self.place_orb_pedestal(itemToUse)
            self.place_orb_boss_door(itemToUse)
        elif itemToUse == "armor":
            if self.currentRoom == 2:
                for index, temp in enumerate(self.playerItems):
                    if temp == "armor":
                        self.playerItems.pop(index)
                        self.roomList[self.currentRoom].roomItems.append("armor")
                        print("You place the armor on the rack.")
                        self.actuate_door(2)
                        self.actuate_door(3)
                        print("You hear multiple doors moving.")
            else:
                print("You are already wearing the armor.")
        elif itemToUse == "sword":
            print("You swing your sword around. You look silly.")

    def place_orb_pedestal(self, itemToUse):
        if self.pedestalStates[self.currentRoom] != False:
            if self.pedestalStates[self.currentRoom] == "":
                for index, temp in enumerate(self.playerItems):
                    if temp == itemToUse:
                        self.playerItems.pop(index)
                self.pedestalStates[self.currentRoom] = itemToUse
                print(f"You place the {itemToUse} on the pedestal.")
                self.actuate_pedestal(itemToUse)
            else:
                print("The pedestal has something on it already.")

    def place_orb_boss_door(self, orb):
        validOrbs = ["yellow orb", "blue orb", "green orb"]
        placed = False
        if orb in validOrbs and self.currentRoom == 4:
            for index, temp in enumerate(self.bossdoor):
                if temp == "" and not placed:
                    self.bossdoor[index] = orb
                    placed = True
                    for indextwo, temptwo in enumerate(self.playerItems):
                        if temptwo == orb:
                            self.playerItems.pop(indextwo)
                            print(f"You place the {orb}.")
                            break
                elif index == 2 and self.bossdoor[index]:
                    print("All the sockets are full.")
        if "yellow orb" in self.bossdoor:
            if "blue orb" in self.bossdoor:
                if "green orb" in self.bossdoor:
                    self.actuate_door(6)
                    print("The door opens.")

    def remove_orb_boss_door(self, orb):
        if orb in self.bossdoor:
            for index, temp in enumerate(self.bossdoor):
                if temp == orb:
                    self.bossdoor[index] = ""
                    self.playerItems.append(orb)
                    print(f"You removed {orb}")
            if self.doorStates[6]:
                print("The door closes.")
                self.actuate_door(6)

    def describe_boss_door(self):
        string = ""
        tempList = []
        if self.currentRoom == 4:
            print("There is a giant door with three sockets along it's frame.")
            print("Each socket has a yellow, blue, and green glyphs.")
            print("There is currently ", end="")
            for index, temp in enumerate(self.bossdoor):
                if self.bossdoor[index] != "":
                    tempList.append(self.bossdoor[index])
            for indextwo, temp in enumerate(tempList):
                if len(tempList) > 0:
                    if indextwo > 0:
                        string += ", "
                    if (indextwo == len(tempList) - 1) and len(tempList) > 1:
                        string += "and a "
                    else:
                        string += "a "
                string += temp
            if self.bossdoor[0] == "":
                if self.bossdoor[1] == "":
                    if self.bossdoor[2] == "":
                        string = "nothing"
            print(string, end=" ")
            print("in the sockets.")

    def boss_encounter(self):
        print("You walk into the room and encounter a lich. An undead mage set to guard the treasure")
        print("of the labrynth. You attempt to charge it. It notices you and casts a fireball.")
        if "armor" in self.playerItems:
            print("The fireball deflects off your armor.")
            if "sword" in self.playerItems:
                print("You attack the lich with your sword, defeating it. CONGRATULATIONS!")
                print("YOU WIN!!!")
                input("Press Enter to finish the game.")
            else:
                print("You attempt to punch the lich, it wasn't very effective.")
                print("If only you had a sword...")
                print("The lich blasts you in the face with another fireball.")
                print("Game over...")
                input("Press Enter to finish the game.")
        else:
            print("The fireball punches a hole through your chest. If only you had armor!")
            print("Game over...")
            input("Press Enter to finish the game.")
        return 1


if __name__ == "__main__":
    game = Game()
    game.run()