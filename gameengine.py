from wordgenerator import *

class GameEngine:

    def __init__(self, wordgenerator):
        self.wordgenerator = wordgenerator
        self.lives = None
        self.word = None
        self.letterSet = None
        self.letterDict = None

    def getLives(self):
        return self.lives

    def getWord(self):
        return self.word

    def getWordLength(self):
        return len(self.word)

    def reload(self):
        self.lives = 5
        self.word = self.wordgenerator.getRandomWord()
        print(self.word)
        self.letterSet = set(self.word)

        letters = list(self.word)
        self.letterDict = dict()
        for letter in letters:
            self.letterDict[letter] = list()

        for letter in list(self.letterDict.keys()):
            for i in range(len(letters)):
                if letters[i] == letter:
                    self.letterDict[letter].append(i)


    def containsLetter(self, letter):
        if letter in self.letterSet:
            return True
        else:
            self.lives -= 1
            return False

    def letterPositions(self, letter):
        if not self.containsLetter(letter):
            return None
        else:
            return self.letterDict[letter]
