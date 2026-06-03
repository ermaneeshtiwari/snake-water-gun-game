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
    user_choice = user_choice.strip().upper()
    choices = {"S": 1, "W": 0, "G": -1}
    choice_names = {"S": "Snake", "W": "Water", "G": "Gun"}
    computer_choice = random.choice(list(choices.keys()))

    if user_choice not in choices:
        return "Invalid choice! Please choose S, W, or G."

    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (
        (user_choice == "S" and computer_choice == "W")
        or (user_choice == "W" and computer_choice == "G")
        or (user_choice == "G" and computer_choice == "S")
    ):
        result = "You win!"
    else:
        result = "Computer wins!"

    return (
        f"You chose {choice_names[user_choice]}. "
        f"Computer chose {choice_names[computer_choice]}. "
        f"{result}"
    )


if __name__ == "__main__":
    user_input = input("Enter your choice (Snake: S, Water: W, Gun: G): ")
    print(snake_water_gun(user_input))

