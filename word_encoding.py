import numpy as np

class WordEncoding:
    def __init__(self, alphabet = 'abcdefghijklmnopqrstuvwxyz'):
        self.alphabet = alphabet

    def decode(self, array):
        out = ''
        for el in array:
            out += self.alphabet[el]
        return out

    def decode_onehot(self, array):
        out = ''
        for l in array:
            out += self.decode(np.nonzero(l)[0])
        return out

    def encode(self, word):
        return [self.alphabet.index(l) for l in word]
