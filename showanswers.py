import random
from gamerunner import NullState
from ui import Text, QuestionText, Countdown, CountdownPrompt

class ShowAnswers(NullState):
    def __init__(self, audio, nextState, currentQuestion, player, countdown_secs = 5):
        self.nextState = nextState
        self.player = player
        self.currentQuestion = currentQuestion
        self.wrongAnswers = []
        self.showWrongAnswersList = []
        self.stopButton = -1
        self.showCorrectAnswer = False
        self.countdownSecs = countdown_secs
        self.endCount = self.countdownSecs
        self.questionText = QuestionText()
        self.delayCorrectAnswerDisplay = True
        text = Text(32, (255, 255, 255))
        self.countdown = Countdown(self.countdownSecs, (80, 560), 640, 32, (128, 0, 0), (255, 0, 0), text, False)
        self.audio = audio

    def update(self, deltaTime):
        if not self.showCorrectAnswer:
            self.countdown.update(deltaTime)
            if self.countdown.finished:
                if len(self.wrongAnswers) > 0:
                    poppedAnswer = self.wrongAnswers.pop(0)
                    self.showWrongAnswersList.append(poppedAnswer)
                    self.player.outputExclusive(poppedAnswer)
                    self.audio.SoundWrong()
                    if (len(self.wrongAnswers) > 0) or self.delayCorrectAnswerDisplay == True:
                        self.countdown.reset()
                else:
                    if self.currentQuestion.selectedAnswer == self.currentQuestion.answerIndex:
                        self.player.score = self.player.score + 1
                    self.player.outputOff()
                    self.audio.SoundCorrect()
                    self.showCorrectAnswer = True

        else:
            self.endCount = self.endCount - deltaTime
            if self.endCount <= 0:
                return self.nextState

        return self

    def draw(self, surface):
        self.questionText.draw(surface, self.currentQuestion.question, self.currentQuestion.answer, self.currentQuestion.answers, True, self.currentQuestion.selectedAnswer, self.showCorrectAnswer, self.showWrongAnswersList)
        if not self.showCorrectAnswer:
            self.countdown.draw(surface)

    def onExit(self):
        self.endCount = self.countdownSecs
        self.showCorrectAnswer = False
        self.countdown.reset()
        self.player.outputOff()

    def onEnter(self):
        self.wrongAnswers = []
        self.showWrongAnswersList = []
        answerCount = 0

        for q in self.currentQuestion.answers:
            if q != self.currentQuestion.answer:
                if answerCount != self.currentQuestion.selectedAnswer:
                    self.wrongAnswers.append(answerCount)
            answerCount = answerCount + 1
        random.shuffle(self.wrongAnswers)
        
        if self.currentQuestion.selectedAnswer != self.currentQuestion.answerIndex:
            self.wrongAnswers.append(self.currentQuestion.selectedAnswer)

        self.audio.MusicPause()