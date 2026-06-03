import random
# Snake Water Gun Game 
# Snake = 1
# Water = 0
# Gun = -1
# Rules:
# Snake drinks water, so snake wins.
# Water douses gun, so water wins.
# Gun kills snake, so gun wins.
def snake_water_gun(user_choice):
    choices = {"S": 1, "W": 0, "G": -1}
    rechoices = {1: "Snake", 0: "Water", -1: "Gun"}
    computer_choice = random.choice(list(choices.keys()))
    if user_choice not in choices:
        return "Invalid choice! Please choose S, W, or G."
    if user_choice == computer_choice:
        return "It's a tie!"
    
    if (user_choice == choices["S"] and computer_choice == choices["W"]) or \
       (user_choice == choices["W"] and computer_choice == choices["G"]) or \
       (user_choice == choices["G"] and computer_choice == choices["S"]):
        return "You win!"
    else:
        return "Computer wins!"
    
user_input = input("Enter your choice (Snake: S, Water: W, Gun: G): ")
result = snake_water_gun(user_input)
print(result)

