import random

print('Welcome.\nThis is a guessing game.\nYou will get 7 chances to guess a random number between 1 and 100 chosen by the compiler :)')

chosen_num = random.randrange(1,100)
# print(chosen_num)
guess_counter = 7

while (guess_counter > 0):
    print(f'You have {guess_counter} guesses left.')
    guess_counter -= 1
    guessed_num = int(input("Enter your guess: "))
    
    if (guessed_num == chosen_num):
        print(f'Hurray! You got it right. The number is {chosen_num}.')
        break

    elif (guess_counter == 0 and guessed_num != chosen_num):
        print(f'Better luck next time. The number is {chosen_num}.')

    elif (guessed_num > chosen_num):
        print('You guessed too high.')

    elif (guessed_num < chosen_num):
        print('You guessed too low.')
