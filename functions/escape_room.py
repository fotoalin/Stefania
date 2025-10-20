"""
Simple Escape Room Game

Description:
You wake up in a locked room with no memory of how you got there. 
Your goal is to explore the room, find hidden items, solve puzzles, 
and ultimately discover the code to unlock the door and escape.

Game Features:
- Explore different areas of the room (desk, bookshelf, painting, door)
- Collect and use items to solve puzzles
- Find clues to determine the 4-digit door code
- Simple text-based interface with command inputs

Commands:
- look [object]: Examine objects in the room
- use [item]: Use an item from your inventory
- inventory: Check what items you have
- help: Show available commands
- quit: Exit the game

Puzzle Flow:
1. Find a flashlight on the desk
2. Use flashlight to see behind the painting
3. Discover a key behind the painting
4. Use key to unlock desk drawer
5. Find a note with the door code
6. Enter code to escape
"""


class EscapeRoom:
    def __init__(self):
        self.inventory = []
        self.door_code = "4729"
        self.door_locked = True
        self.drawer_locked = True
        self.found_code = False
        
    def start_game(self):
        print("\n=== ESCAPE ROOM ===")
        print("You wake up in a dimly lit room. The door is locked.")
        print("You need to find a way to escape!")
        print("\nType 'help' for commands.\n")
        
        while self.door_locked:
            command = input("> ").lower().split()
            if not command:
                continue
                
            action = command[0]
            
            if action == "help":
                self.show_help()
            elif action == "quit":
                print("Thanks for playing!")
                break
            elif action == "inventory":
                self.show_inventory()
            elif action == "look":
                if len(command) > 1:
                    self.look_at(command[1])
                else:
                    self.look_around()
            elif action == "use":
                if len(command) > 1:
                    self.use_item(command[1])
                else:
                    print("Use what?")
            elif action == "enter":
                if len(command) > 1:
                    self.enter_code(command[1])
                else:
                    print("Enter what?")
            else:
                print("Unknown command. Type 'help' for commands.")
    
    def show_help(self):
        print("\nCommands:")
        print("- look [object]: Examine the room or specific objects")
        print("- use [item]: Use an item from your inventory")
        print("- inventory: Check your items")
        print("- enter [code]: Enter a code on the door keypad")
        print("- quit: Exit the game\n")
    
    def look_around(self):
        print("\nYou see:")
        print("- A wooden DESK with a drawer")
        print("- A BOOKSHELF filled with old books")
        print("- A PAINTING on the wall")
        print("- A DOOR with a digital keypad\n")
    
    def look_at(self, object):
        if object == "desk":
            print("\nA sturdy wooden desk. There's a FLASHLIGHT on top.")
            if self.drawer_locked:
                print("The drawer is locked.")
            else:
                print("The drawer is open. Inside is a NOTE.")
        elif object == "bookshelf":
            print("\nDusty old books. Nothing particularly interesting.")
        elif object == "painting":
            if "flashlight" in self.inventory:
                print("\nUsing your flashlight, you see a KEY hidden behind the painting!")
                if "key" not in self.inventory:
                    self.inventory.append("key")
                    print("You take the KEY.")
            else:
                print("\nA dark painting. It's too dark to see details.")
        elif object == "door":
            print("\nA heavy door with a 4-digit keypad. It's locked.")
        elif object == "flashlight":
            if "flashlight" not in self.inventory:
                print("\nA working flashlight.")
                self.inventory.append("flashlight")
                print("You take the FLASHLIGHT.")
            else:
                print("\nYou already have the flashlight.")
        elif object == "note":
            if not self.drawer_locked and not self.found_code:
                print(f"\nThe note reads: 'The escape code is {self.door_code}'")
                self.found_code = True
            else:
                print("\nYou can't see that.")
        else:
            print(f"\nYou don't see a {object} here.")
    
    def use_item(self, item):
        if item not in self.inventory:
            print(f"\nYou don't have a {item}.")
        elif item == "flashlight":
            print("\nThe flashlight illuminates dark areas. Try looking at things again!")
        elif item == "key":
            if self.drawer_locked:
                print("\nYou unlock the desk drawer with the key.")
                self.drawer_locked = False
            else:
                print("\nThe drawer is already unlocked.")
        else:
            print(f"\nYou can't use the {item} right now.")
    
    def show_inventory(self):
        if self.inventory:
            print("\nYou have:", ", ".join(self.inventory))
        else:
            print("\nYour inventory is empty.")
    
    def enter_code(self, code):
        if code == self.door_code:
            print("\n*** CLICK! ***")
            print("The door unlocks! You've escaped!")
            print("\nCongratulations! You've won the game!")
            self.door_locked = False
        else:
            print("\nWrong code. The door remains locked.")


if __name__ == "__main__":
    game = EscapeRoom()
    game.start_game()
