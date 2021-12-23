import pickle
import json
import numpy as np
from word_encoding import WordEncoding

class WordleGame:
    N_GUESSES = 6
    def __init__(self, seed = None):
        if not seed is None:
            np.random.seed = seed

        # Load in the dictionary
        with open('wordle_dictionary.json', 'r') as fd:
            self.dictionary = json.load(fd)
        self.word_list = list(self.dictionary.keys())

    def generate_random_word(self):
        return self.word_list[np.random.randint(0, len(self.word_list))]


    def sim(self, guesser, word = None):
        # A simulation of the game. Takes a guesser as an input, which makes successive guesses of words, and a word. If word is None (defualt), a word is automatically generated.
        
        # Generate a random word if one is not provided
        if word is None:
            word = self.generate_random_word()

        letters_not_in_word = set()
        letters_in_word = set()
        letters_in_position = [None] * 5
        
        for i in range(WordleGame.N_GUESSES):
            guess = guesser(letters_not_in_word, letters_in_word, letters_in_position)
            print(guess)
            assert guess in self.word_list

            if guess == word:
                # Return number of guesses
                return i + 1
            else:
                # Update the state information
                for i, l in enumerate(guess):
                    if not l in word:
                        letters_not_in_word.add(l)
                    else:
                        letters_in_word.add(l)
                        if word[i] == l:
                            letters_in_position[i] = l
        else:
            return None

def guesser_generator(dictionary_array, encoding):
    letter_occurance_array = np.max(dictionary_array, axis = 1)
    def guesser(letters_not_in_word, letters_in_word, letters_in_position):
        nonlocal dictionary_array, encoding, letter_occurance_array

        keep_indexes = np.ones((dictionary_array.shape[0]), bool)
        for l in encoding.encode(letters_not_in_word):
            # Take out words where the letter is in it
            keep_indexes &= np.logical_not(letter_occurance_array[:,l])
            # # Take out the letter
            # dictionary_array = np.append(dictionary_array[:,:,:l], dictionary_array[:,:,l+1:], axis = -1)

        for l in encoding.encode(letters_in_word):
            keep_indexes &= letter_occurance_array[:,l]
            # dictionary_array = np.append(dictionary_array[:,:,:l], dictionary_array[:,:,l+1:], axis = -1)


        for i, l in enumerate(letters_in_position):
            if not l is None:
                keep_indexes &= dictionary_array[:,i,encoding.encode(l)[0]]

        dictionary_array = dictionary_array[keep_indexes]
        letter_occurance_array = letter_occurance_array[keep_indexes]
        # Number of words each letter occurs in
        letter_occurance_totals = np.sum(letter_occurance_array, axis = 0)

        n_words = dictionary_array.shape[0]

        letter_in_word_scores = letter_occurance_totals ** 2 + (n_words - letter_occurance_totals) ** 2

        letter_placed_totals = np.sum(dictionary_array, axis = 0)

        letter_placed_scores = letter_placed_totals ** 2 + (n_words - letter_placed_totals) ** 2

        dictionary_scores = np.sum(letter_occurance_array * letter_in_word_scores[None, :], axis = -1)
                            # + dictionary_array * letter_placed_scores[None, :, :]

        return encoding.decode_onehot(dictionary_array[np.argmax(dictionary_scores)])
    return guesser



if __name__ == '__main__':
    with open('wordle_dictionary_array.p', 'rb') as fd:
        dictionary_array = pickle.load(fd)

    wordle_game = WordleGame(seed = 0)

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encoding = WordEncoding(alphabet)

    guesser = guesser_generator(dictionary_array, encoding)

    # guesser = lambda x, y, z: 'hello'

    print(wordle_game.sim(guesser))

