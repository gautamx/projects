# GUESSING GAME
import random
import math

print('Welcome.\nThis is a guessing game.\nYou will get 7 chances to guess a random number between 1 and 100 chosen by the compiler :)')
range_lowlimit = int(input("Enter range lower limit: "))
range_uplimit = int(input("Enter range upper limit: "))
chosen_num = random.randrange(range_lowlimit,range_uplimit)

# Minimum number of guessing = log2(Upper bound – lower bound + 1)
log_input = range_uplimit - range_lowlimit + 1
guess_counter = math.ceil(math.log(log_input,2))

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
