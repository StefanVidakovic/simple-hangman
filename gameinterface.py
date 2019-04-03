import sys
import pygame
from gameengine import *
from wordgenerator import *
from alphabetletter import *

class GameInterface:
    def __init__(self):
        pygame.init()
        self.displaySize = width, height = 800, 600
        self.displayColor = 242, 230, 217
        self.color = 203, 151, 103
        self.hoverColor = 216, 177, 141
        self.inactiveColor = 248, 242, 236
        self.screen = pygame.display.set_mode(self.displaySize)

        self.screen.fill(self.displayColor)
        pygame.display.flip()

        self.wordgenerator = WordGenerator('wordbank','words')
        self.engine = GameEngine(self.wordgenerator)

        self.alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.alphabetButtons = list()
        self.initAlphaBet()

        self.arialSmall = pygame.font.SysFont("Times New Roman, Arial", 20)

        self.wordStartX = 50
        self.wordStartY = 200
        self.prevMouseState = False

        self.heartContainer = pygame.image.load('heartcontainerresized.png')
        self.heartX = self.wordStartX
        self.heartY = self.wordStartY + 125

        self.linkStanding = pygame.image.load('linkStanding.png')
        self.linkDead = pygame.image.load('linkDead.png')
        self.linkWins = pygame.image.load('linkWINS.png')

        self.state = "playing"
        self.uncoveredLetters = 0


    def initAlphaBet(self):
        x = 500
        y = 100
        width = 40
        height = 40
        marginX = 10
        marginY = 10

        for letter in self.alphabet:
            self.alphabetButtons.append(AlphabetLetter(letter, x, y, width, height, self.color, self.hoverColor, self.inactiveColor, self.screen))
            if x == 700:
                x = 500
                y += marginY + height
            else:
                x += width + marginX

    def drawUnderscores(self, wordLength):
        text = self.arialSmall.render("_",True, (0, 0, 0))
        x = self.wordStartX
        y = self.wordStartY
        width = 20
        height = 20
        marginX = 5
        pygame.draw.rect(self.screen, self.displayColor, (x, y, 450, height))
        for i in range(wordLength):
            self.screen.blit(text,(x,y))
            x += width + marginX
        pygame.display.update(pygame.Rect(self.wordStartX, self.wordStartY, 450, height))

    def showWord(self):
        word = self.engine.getWord()
        chars = list(word)
        x = self.wordStartX
        y = self.wordStartY
        width = 20
        height = 20
        marginX = 5
        pygame.draw.rect(self.screen, self.displayColor, (x, y, 450, height))
        for char in chars:
            text = self.arialSmall.render(char,True, (0, 0, 0))
            self.screen.blit(text,(x,y))
            x += width + marginX
        pygame.display.update(pygame.Rect(self.wordStartX, self.wordStartY, 450, height))


    def reload(self):
        self.engine.reload()
        wordLength = self.engine.getWordLength()
        self.drawUnderscores(wordLength)

        for alpha in self.alphabetButtons:
            if alpha.guessed:
                alpha.guessed = False

        self.updateHearts()
        self.state = "playing"
        self.uncoveredLetters = 0
        pygame.draw.rect(self.screen, self.displayColor, (self.heartX, self.heartY, 25, 100))
        self.screen.blit(self.linkStanding, (self.heartX, self.heartY+50))
        pygame.display.update(pygame.Rect(self.heartX, self.heartY+50, 25, 46))

    def updateHearts(self):
        numLives = self.engine.getLives()
        pygame.draw.rect(self.screen, self.displayColor, (self.heartX, self.heartY, 450, 25))
        heartX = self.heartX
        heartY = self.heartY
        for i in range(numLives):
            self.screen.blit(self.heartContainer, (heartX, heartY))
            heartX += 35
        pygame.display.update(pygame.Rect(self.heartX, self.heartY, 450, 25))

    def uncoverLetter(self, letter, positions):
        text = self.arialSmall.render(letter,True, (0, 0, 0))
        y = self.wordStartY
        letterWidth = 25
        height = 20
        width = 20
        for position in positions:
            x = self.wordStartX + position*letterWidth
            self.screen.blit(text,(x,y))
            pygame.display.update(pygame.Rect(x, y, width, height))

    def button(self, msg, x, y, width, height, color, hoverColor, action=None):
        #Similar code is repeated for alphabet buttons, redundancy could be
        #reduced by creating general button object and then extending it as needed
        #or by implementing something similar to addOnClickListener from JS, not sure
        #if this is possible with pygame though
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x+width and y < mouse[1] < y+height:
            pygame.draw.rect(self.screen, hoverColor,(x ,y ,width, height))

            if click[0] == 1 and action != None and not self.prevMouseState:
                self.prevMouseState = True
                action()
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
            self.prevMouseState = False
        self.screen.blit(msg, (x+20, y+15))
        pygame.display.update(pygame.Rect(x, y, width, height))

    def run(self):
        self.reload()
        reloadMsg = self.arialSmall.render("Next Puzzle", True, (0,0,0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.button(reloadMsg, 500, 500, 140, 50, self.color, self.hoverColor, self.reload)

            if self.engine.getLives() <= 0:
                #notify user of loss
                self.showWord()
                if self.state != "lost":
                    pygame.draw.rect(self.screen, self.displayColor, (self.heartX, self.heartY+50, 25, 46))
                    self.screen.blit(self.linkDead, (self.heartX, self.heartY+50))
                    pygame.display.update(pygame.Rect(self.heartX, self.heartY+50, 25, 46))
                self.state = "lost"

            if self.uncoveredLetters == self.engine.getWordLength():
                #user won
                if self.state == "playing":
                    pygame.draw.rect(self.screen, self.displayColor, (self.heartX, self.heartY+50, 25, 46))
                    self.screen.blit(self.linkWins, (self.heartX, self.heartY+50))
                    pygame.display.update(pygame.Rect(self.heartX, self.heartY+50, 25, 46))
                self.state = "won"

            for alpha in self.alphabetButtons:
                if alpha.button():
                    letter = alpha.letter.lower()
                    if self.engine.containsLetter(letter):
                        #uncover letter in all places
                        self.uncoveredLetters += 1
                        letterPositions = self.engine.letterPositions(letter)
                        self.uncoverLetter(letter, letterPositions)
                    else:
                        #remove heart container
                        self.updateHearts()

if __name__ == "__main__":
    game = GameInterface()
    game.run()
