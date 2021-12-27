import json
import numpy as np
import pickle
from word_encoding import WordEncoding

def get_onehot(dict):
    # Create a one hot encoding of all of the words
    words_array = np.array([encoding.encode(word) for word in dict.keys()])
    words_one_hot = np.zeros((words_array.shape[0], words_array.shape[1], len(alphabet)), bool)
    for i, word in enumerate(words_array):
        for j, letter in enumerate(word):
            words_one_hot[i, j, letter] = True
    return words_one_hot

if __name__ == '__main__':
    with open('words_dictionary.json') as fd:
        full_dictionary = json.load(fd)

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encoding = WordEncoding(alphabet)

    wordle_dictionary = {key: value for key, value in full_dictionary.items() if len(key) == 5}

    with open('wordle_dictionary.json', 'w') as fd:
        json.dump(wordle_dictionary, fd)
        
    words_one_hot = get_onehot(wordle_dictionary)

    with open('wordle_dictionary_array.p', 'wb') as fd:
        pickle.dump(words_one_hot, fd)

    wordle_dictionary_short = {}
    with open('short_word_list.txt', 'r') as fd:
        for line in fd:
            if len(stripped := line.strip().lower()) == 5:
                wordle_dictionary_short[stripped] = 1
    
    with open('wordle_dictionary_short.json', 'w') as fd:
        json.dump(wordle_dictionary_short, fd)

    words_one_hot_short = get_onehot(wordle_dictionary_short)

    with open('wordle_dictionary_array_short.p', 'wb') as fd:
        pickle.dump(words_one_hot_short, fd)

