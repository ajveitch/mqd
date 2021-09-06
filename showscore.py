import pygame
from pygame.locals import *
from gamerunner import NullState
from ui import Text, CountdownPrompt

class ShowScore(NullState):
    def __init__(self, audio, nextState, player):
        self.nextState = nextState
        self.player = player
        self.startButton = -1
        self.counter = 5
        self.scoreText = Text(300, (255, 255, 0))
        text = Text(32, (255, 255, 255))
        self.countdownPrompt = CountdownPrompt((400, 560), text, "Press START to continue")
        self.audio = audio
        self.musicRestart = False

    def update(self, deltaTime):
        if self.startButton == 0:
            start = self.player.startButton()
            if start:
                return self.nextState
        self.startButton = self.player.startButton()

        self.counter = self.counter - deltaTime
        if self.counter <= 0:
            if self.musicRestart == False:
                self.musicRestart = True
                self.audio.MusicPre()

        return self

    def draw(self, surface):
        self.scoreText.draw(surface, str(self.player.score), (400, 150), True)
        self.countdownPrompt.draw(surface)

    def onEnter(self):
        self.audio.SoundScore()
        self.counter = 5
        self.musicRestart = False
        self.startButton = self.player.startButton()
