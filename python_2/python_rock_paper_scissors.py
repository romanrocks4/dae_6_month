import random
import time
program = True
def winner():
    if choice == com_choice:
        print("You tied")
    elif (choice == 1 and com_choice == 3) or (choice == 2 and com_choice == 1) or (choice == 3 and com_choice == 2):
        print("You won!!")
    else:
        print("You lost...")

print ("********************************************* \n      Welcome to rock paper scissors!")

while program == True: 
    
    print ("\n 1. Rock \n 2. Paper \n 3. Scissors")

    choice = int(input("Enter your choice: "))
    if choice > 3 or choice < 1:
        choice = int(input("Enter a valid choice:"))

    if choice == 1:
        choice_name = ("Rock")
    elif choice == 2:
        choice_name = ("Paper")
    else:
        choice_name = ("Scissors")

    print ("Your choice is",choice_name)
    time.sleep(1)
    print ("Its now the Computer's turn")
    time.sleep(1)
    print ("The Computer is thinking...")
    time.sleep(0.5)
    print (".")
    time.sleep(0.5)
    print (".")
    time.sleep(0.5)
    print (".")
    com_choice = random.randint(1, 3)

    if com_choice == 1:
        com_choice_name = "Rock"

    elif com_choice == 2:
        com_choice_name = "Paper"

    else:
        com_choice_name = "Scissors"
    
    print("The Computer's choice is", com_choice_name)
    print(choice_name, "vs", com_choice_name)

    winner()
    time.sleep(2)

    play = input("\nWould you like to play again?\n:")

    if play in[ "Yes", "yes", "y", "Y"]:
        program = True

    elif play in["No", "no", "n", "N"]:
        print("Goodbye!")
        program = False
    else:
        print("Error")