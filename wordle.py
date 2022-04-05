import random
import requests

_VALID_GUESS = 1
_NOT_5_LETTERS = 2
_NOT_IN_DICTIONARY = 3

_MAX_ATTEMPTS = 6

available_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                     'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

with open('words.txt', 'r') as f:
    words = []
    for line in f:
        line = line.replace('\n', '')
        words.append(line)

    
def get_word(word_list):
    list_size = len(word_list)
    return word_list[random.randrange(list_size - 1)]


def is_in_dictionary(key_guess):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(key_guess)
    jsondata = requests.get(url).json()
    try:
        correct = jsondata[0]['word']
    except:
        correct = False
    if correct:
        return True
    else:
        return False
    

def user_guess(letter_set):
    key_guess = input("5 letter guess: ").lower()
    key_guess_size = len(key_guess)
    key_guess_list = set(list(key_guess))
    if key_guess_size != 5:
        return (key_guess, _NOT_5_LETTERS, letter_set)
    elif not is_in_dictionary(key_guess):
        return (key_guess, _NOT_IN_DICTIONARY, letter_set)
    else:
        for letter in key_guess_list:
            letter_set.discard(letter)
        return (key_guess, _VALID_GUESS, letter_set)


def analysis(guess_str, word_str):
    string = ""
    for index in range(5):
        if guess_str[index] == word_str[index]:
            string = string + ' *{}* '.format(guess_str[index])
        elif word_str.find(guess_str[index]) > -1:
            string = string + " -{}- ".format(guess_str[index])
        else:
            string = string + " --- "
    return string
    

word = get_word(words)
#word="stuck"
attempts = _MAX_ATTEMPTS

print('Welcome to pyWordle!')
print('You have {} attempts to guess the 5 letter word\n'.format(_MAX_ATTEMPTS))
print('*x* right letter in the right position')
print('-x- right letter in the wrong position')
print('--- letter is not in the word\n')

while True:
    
    guess_word, return_code, letters = user_guess(available_letters)
    remaining_string = "".join(letters)
    if return_code == _VALID_GUESS:
        print('{}  Remaining letters: {}'.format(analysis(guess_word, word), remaining_string))
        attempts = attempts - 1
    elif return_code == _NOT_IN_DICTIONARY:
        print('Word not in dictionary - Remaining letters: {}'.format(remaining_string))
    elif return_code == _NOT_5_LETTERS:
        guess_word = None
        print('Word must contain 5 letters - Remaining letters: {}'.format(remaining_string))

    if guess_word == word:
        print("You won! Using {} guesses!".format(_MAX_ATTEMPTS - attempts))
        break
    
    if attempts < 1:
        print('Too many attempts!')
        print('The word was {}'.format(word))
        break
    available_letters = letters