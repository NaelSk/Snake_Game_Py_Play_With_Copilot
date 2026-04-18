#Create a simple rock-paper-scissors game
#provide welcome message and instructions
#provide game instructions
#get computer's choice
#get user's choice
#compare choices and determine winner
#display result
#ask user if they want to play again
#say goodbye if user does not want to play again
#use one function for the game logic
import random

CHOICES = ['rock', 'paper', 'scissors']

def determine_winner(user_choice, computer_choice):
    """
    Determines the winner of a rock-paper-scissors game.
    
    Args:
        user_choice: User's choice ('rock', 'paper', or 'scissors')
        computer_choice: Computer's choice ('rock', 'paper', or 'scissors')
    
    Returns:
        'tie' if both chose the same
        'user' if user wins
        'computer' if computer wins
        None if invalid choice
    """
    if user_choice not in CHOICES:
        return None
    
    if user_choice == computer_choice:
        return 'tie'
    
    win_conditions = {
        ('rock', 'scissors'): 'user',
        ('paper', 'rock'): 'user',
        ('scissors', 'paper'): 'user',
    }
    
    return win_conditions.get((user_choice, computer_choice), 'computer')

def play_game():
    print("Welcome to Rock-Paper-Scissors!")
    print("Instructions: Type 'rock', 'paper', or 'scissors' to play.")
    
    computer_choice = random.choice(CHOICES)
    
    user_choice = input("Enter your choice: ").lower()
    
    result = determine_winner(user_choice, computer_choice)
    
    if result is None:
        print("Invalid choice. Please try again.")
        return
    
    print(f"Computer chose: {computer_choice}")
    
    if result == 'tie':
        print("It's a tie!")
    elif result == 'user':
        print("You win!")
    else:
        print("Computer wins!")
    
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again == 'yes':
        play_game()
    else:
        print("Thanks for playing! Goodbye!")

if __name__ == "__main__":
    play_game()


