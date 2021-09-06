from ui import *
from playercontroller import *
from gamerunner import NullState

class HeaderTextScreen(NullState):
    def __init__(self, audio, nextState, player, waitTime = 0):
        self.nextState = nextState
        self.startButton = -1
        self.player = player
        self.big = Text(96, (255, 192, 0))
        self.small = Text(36, (255, 255, 255))
        self.waitTime = waitTime
        self.currentTime = 0
        self.header = ""
        self.subHeader = ""
        self.audio = audio

    def setHeader(self, header):
        self.header = header

    def setSub(self, subHeader):
        self.subHeader = subHeader

    def setNextState(self, nextState):
        self.nextState = nextState

    def update(self, deltaTime):
        if self.waitTime > 0:
            self.currentTime = self.currentTime + deltaTime
            if self.currentTime >= self.waitTime:
                return self.nextState
        elif self.startButton == 0:
            start = self.player.startButton()
            if start:
                return self.nextState
        self.startButton = self.player.startButton()
        return self

    def draw(self, surface):
        self.big.draw(surface, self.header, (400, 200), True)
        self.small.draw(surface, self.subHeader, (400, 300), True)

    def onEnter(self):
        self.audio.MusicPre()
        self.startButton = self.player.startButton()

