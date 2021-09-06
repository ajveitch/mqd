from gamerunner import NullState
from ui import Text, QuestionText, Countdown

class ShowCountdown(NullState):
    def __init__(self, audio, nextState, currentQuestion, player, countdown_secs = 60):
        self.nextState = nextState
        self.player = player
        self.stopButton = -1
        self.currentQuestion = currentQuestion
        self.getAnswer = False
        self.endCount = 0
        self.questionText = QuestionText()
        text = Text(32, (255, 255, 255))
        self.countdown = Countdown(countdown_secs, (80, 560), 640, 32, (128, 0, 0), (255, 0, 0), text)
        self.audio = audio

    def update(self, deltaTime):
        if self.stopButton == 0:
            stop = self.player.stopButton()
            if stop:
                self.getAnswer = True
        self.stopButton = self.player.stopButton()
        if not self.getAnswer:
            self.countdown.update(deltaTime)
            if self.countdown.finished:
                self.getAnswer = True
        else:
            self.endCount = self.endCount - deltaTime
            if self.endCount <= 0:
                return self.nextState
        return self

    def draw(self, surface):
        self.questionText.draw(surface, self.currentQuestion.question, self.currentQuestion.answer, self.currentQuestion.answers)
        if not self.getAnswer:
            self.countdown.draw(surface)

    def onExit(self):
        self.endCount = 0
        self.getAnswer = False
        self.countdown.reset()

    def onEnter(self):
        self.audio.MusicTimer()
        self.stopButton = self.player.stopButton()

