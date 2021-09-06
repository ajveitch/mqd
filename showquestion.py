from gamerunner import NullState
from ui import Text, QuestionText, CountdownPrompt

class ShowQuestion(NullState):
    def __init__(self, audio, nextState, currentQuestion, player):
        self.nextState = nextState
        self.player = player
        self.startButton = -1
        self.currentQuestion = currentQuestion
        self.showAnswer = False
        self.questionText = QuestionText()
        text = Text(32, (255, 255, 255))
        self.countdownPrompt = CountdownPrompt((400, 560), text, "Press START to continue")
        self.audio = audio

    def update(self, deltaTime):
        if self.startButton == 0:
            start = self.player.startButton()
            if start:
                return self.nextState
        self.startButton = self.player.startButton()
        return self

    def draw(self, surface):
        self.questionText.draw(surface, self.currentQuestion.question, self.currentQuestion.answer, self.currentQuestion.answers)
        self.countdownPrompt.draw(surface)

    def onEnter(self):
        self.audio.MusicQuestion()
        self.startButton = self.player.startButton()
