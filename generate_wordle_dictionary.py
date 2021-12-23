import json
import numpy as np
import pickle
from word_encoding import WordEncoding


if __name__ == '__main__':
    with open('words_dictionary.json') as fd:
        full_dictionary = json.load(fd)

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encoding = WordEncoding(alphabet)

    wordle_dictionary = {key: value for key, value in full_dictionary.items() if len(key) == 5}

    with open('wordle_dictionary.json', 'w') as fd:
        json.dump(wordle_dictionary, fd)
    
    # Create a one hot encoding of all of the words
    words_array = np.array([encoding.encode(word) for word in wordle_dictionary.keys()])
    words_one_hot = np.zeros((words_array.shape[0], words_array.shape[1], len(alphabet)), bool)
    for i, word in enumerate(words_array):
        for j, letter in enumerate(word):
            words_one_hot[i, j, letter] = True

    with open('wordle_dictionary_array.p', 'wb') as fd:
        pickle.dump(words_one_hot, fd)