import pygame

class AlphabetLetter:
    def __init__(self, letter, x, y, width, height, color, hoverColor, inactiveColor, gameDisplay):
        self.letter = letter
        self.guessed = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hoverColor = hoverColor
        self.inactiveColor = inactiveColor
        self.gameDisplay = gameDisplay
        self.arialSmall = pygame.font.SysFont("Times New Roman, Arial", 30)
        self.text = self.arialSmall.render(self.letter,True, (0, 0, 0))

        pygame.draw.rect(self.gameDisplay, self.color,(self.x, self.y, self.width, self.height))
        self.gameDisplay.blit(self.text,(self.x+8,self.y+5))
        pygame.display.update(pygame.Rect(self.x, self.y, self.width, self.height))

        self.prevState = "normal"

    def button(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        state = None
        clicked = False

        if self.guessed:
            pygame.draw.rect(self.gameDisplay, self.inactiveColor,(self.x, self.y, self.width, self.height))
            state = "guessed"

        elif self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(self.gameDisplay, self.hoverColor,(self.x, self.y, self.width, self.height))
            state = "hover"
            if click[0] == 1:
                self.guessed = True
                pygame.draw.rect(self.gameDisplay, self.inactiveColor,(self.x, self.y, self.width, self.height))
                clicked = True
        else:
            pygame.draw.rect(self.gameDisplay, self.color,(self.x, self.y, self.width, self.height))
            state = "normal"

        if state != self.prevState:
            self.prevState = state
            self.gameDisplay.blit(self.text,(self.x+8,self.y+5))
            pygame.display.update(pygame.Rect(self.x, self.y, self.width, self.height))

        return clicked
