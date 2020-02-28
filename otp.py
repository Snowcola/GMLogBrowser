import string
from collections import deque


class VignereCipher:
    def __init__(self, alphabet=string.ascii_lowercase, x_fill=0, y_fill=0):
        self.alphabet = deque(alphabet)
        self.vignere = []
        for x in range(len(alphabet)):
            self.vignere.append(list(self.alphabet))
            self.alphabet.rotate(-1)
        
    def encrypt(self):
        pass

    def encrypt(self):
        pass