from gamerunner import NullState
from ui import Text, QuestionText, CountdownPrompt

class GetQuestionAnswer(NullState):
    def __init__(self, nextState, currentQuestion, player):
        self.nextState = nextState
        self.player = player
        self.currentQuestion = currentQuestion
        self.showAnswer = False
        self.endCount = 0
        self.questionText = QuestionText()
        text = Text(32, (255, 255, 255))
        self.countdownPrompt = CountdownPrompt((400, 560), text, "Select your answer")

    def update(self, deltaTime):
        if self.answerButton == -1:
            answer = self.player.playerChoice()
            if answer >= 0 and answer < len(self.currentQuestion.answers):
                self.currentQuestion.selectedAnswer = answer
                self.showAnswer = True
        if self.showAnswer:
            self.endCount = self.endCount - deltaTime
            if self.endCount <= 0:
                return self.nextState
        return self

    def draw(self, surface):
        self.questionText.draw(surface, self.currentQuestion.question, self.currentQuestion.answer, self.currentQuestion.answers, self.showAnswer, self.currentQuestion.selectedAnswer)
        if not self.showAnswer:
            self.countdownPrompt.draw(surface)


    def onExit(self):
        self.endCount = 0
        self.showAnswer = False

    def onEnter(self):
        self.answerButton = self.player.playerChoice()

