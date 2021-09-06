import pygame
from pygame.locals import *

class NullState(object):
    def update(self, deltaTime):
        return None
    def draw(self, surface):
        pass
    def onEnter(self):
        pass
    def onExit(self):
        pass

class GameRunner(object):
    def __init__(self, dimensions, title, backColour, initialState):
        self.state = initialState
        self.clock = pygame.time.Clock()
        self.backColour = backColour
        self.surface = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(title)

    def update(self):
        deltaTime = self.clock.tick(30) / 1000.0
        if self.state != None:
            self.state = self.state.update(deltaTime)
        return self.state

    def draw(self):
        self.surface.fill(self.backColour)
        if self.state != None:
            self.state.draw(self.surface)
        pygame.display.update()
