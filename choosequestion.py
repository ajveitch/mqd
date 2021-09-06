from gamerunner import NullState

class ChooseQuestion(NullState):
    def __init__(self, nextState, endGameState, currentQuestion, questions):
        self.questions = questions
        self.nextState = nextState
        self.endGameState = endGameState
        self.current = -1
        self.currentQuestion = currentQuestion

    def update(self, deltaTime):
        self.current = self.current + 1
        if self.current == len(self.questions):
            self.currentQuestion.question = ""
            self.currentQuestion.answer = ""
            self.currentQuestion.answerIndex = -1
            self.currentQuestion.answers = []
            self.current = -1
            return self.endGameState
        else:
            question = self.questions[self.current]
            self.currentQuestion.question = question.question
            self.currentQuestion.answer = question.answer
            self.currentQuestion.answers = question.answers
            self.currentQuestion.answerIndex = question.answerIndex
        return self.nextState
