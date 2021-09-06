import pygame
from pygame.locals import *
from pathlib import Path

class GameAudio(object):
    def __init__(self):
        AUDIO_PATH = Path(__file__).parent

        PRE_GAME = str(AUDIO_PATH / "audio/mixkit-feeling-happy-5.wav")
        QUESTION_GAME = str(AUDIO_PATH / "audio/mixkit-getting-ready-46.wav")
        TIMER_GAME = str(AUDIO_PATH / "audio/mixkit-game-level-music2-689.wav")
        COUNTDOWN_GAME = str(AUDIO_PATH / "audio/mixkit-long-game-over-notification2-276.wav")
        CORRECT_GAME = str(AUDIO_PATH / "audio/mixkit-player-boost-recharging-2040.wav")
        WRONG_GAME = str(AUDIO_PATH / "audio/mixkit-ominous-drums-227.wav")
        SCORE_GAME = str(AUDIO_PATH / "audio/mixkit-game-level-completed-2059.wav")

        self.musicPre = PRE_GAME
        self.musicQuestion = QUESTION_GAME
        self.musicTimer = TIMER_GAME
        
        self.soundCountdown = pygame.mixer.Sound(COUNTDOWN_GAME)
        self.soundCorrect = pygame.mixer.Sound(CORRECT_GAME)
        self.soundWrong = pygame.mixer.Sound(WRONG_GAME)
        self.soundScore = pygame.mixer.Sound(SCORE_GAME)

    def MusicPre(self):
        pygame.mixer.music.load(self.musicPre)
        pygame.mixer.music.play(-1)
    
    def MusicQuestion(self):
        pygame.mixer.music.load(self.musicQuestion)
        pygame.mixer.music.play(-1)

    def MusicTimer(self):
        pygame.mixer.music.load(self.musicTimer)
        pygame.mixer.music.play(-1)
    
    def MusicPause(self):
        pygame.mixer.music.pause()
    
    def MusicUnpause(self):
        pygame.mixer.music.unpause()
    
    def SoundCountdown(self):
        self.MusicPause()
        ßpygame.mixer.Sound.play(self.soundCountdown)
        #self.MusicUnpause()

    def SoundCorrect(self):
        self.MusicPause()
        pygame.mixer.Sound.play(self.soundCorrect)
        #self.MusicUnpause()

    def SoundWrong(self):
        self.MusicPause()
        pygame.mixer.Sound.play(self.soundWrong)
        #self.MusicUnpause()

    def SoundScore(self):
        self.MusicPause()
        pygame.mixer.Sound.play(self.soundScore)
        #self.MusicUnpause()




class Text(object):
    def __init__(self, size, colour):
        self.size = size
        self.colour = colour
        self.font = pygame.font.Font(None, size)

    def draw(self, surface, msg, pos, centred = False):
        x, y = pos
        tempSurface = self.font.render(msg, True, self.colour)
        if centred:
            x = x - tempSurface.get_width() / 2
            y = y + tempSurface.get_height() / 4
            pos = (x, y)
        surface.blit(tempSurface, pos)

class QuestionText(object):
    def __init__(self):
        self.questionText = Text(32, (255, 255, 0))
        self.answerText = Text(32, (255, 255, 255))
        self.disabledText = Text(32, (56, 56, 56))
        self.buttonText = Text(48, (255, 255, 255))
        self.borderColour = (0, 0, 255)
        self.answerColour = (192, 192, 0)
        self.correctColour = (0, 192, 0)
        self.wrongColour = (192, 0, 0)

    def draw(self, surface, question, answer, answers, showAnswer = False, answerButton = -1, showCorrectAnswer = False, showWrongAnswersList = []):
        y = 64
        maxWidth = 30
        lineHeight = 32
        rectHeight = 48
        borderWidth = 2
        textOffset = int(rectHeight - lineHeight) / 2

        self.questionText.draw(surface, question, (400, y), True)

        y = y + rectHeight * 2
        label = "A"

        for a in answers:
            pygame.draw.rect(surface, self.borderColour, Rect(100, y, 600, rectHeight), borderWidth)

            ordLabelIndex = ord(label) - ord("A")

            if showAnswer and (ordLabelIndex == answerButton):
                pygame.draw.rect(surface, self.answerColour, Rect(100, y + borderWidth, 600, rectHeight - borderWidth), 0)

            if len(showWrongAnswersList) > 0:
                for wa in showWrongAnswersList:
                    if ordLabelIndex == wa:
                        pygame.draw.rect(surface, self.wrongColour, Rect(100, y + borderWidth, 600, rectHeight - borderWidth), 0)

            if showCorrectAnswer and (a == answer):
                pygame.draw.rect(surface, self.correctColour, Rect(100, y + borderWidth, 600, rectHeight - borderWidth), 0)                

            pygame.draw.circle(surface, self.borderColour, (100, y + int(rectHeight / 2)), int(rectHeight / 2))

            font = self.buttonText
            font.draw(surface, "%s" % label, (100, y - borderWidth), True)
            font = self.answerText
            font.draw(surface, "%s" % a, (400, y + textOffset), True)

            labelChar = ord(label)
            labelChar = labelChar + 1
            label = chr(labelChar)

            y = y + 64

class CountdownPrompt(object):
    def __init__(self, pos, text, prompt):
        self.pos = pos
        self.text = text
        self.prompt = prompt
    
    def draw(self, surface):
        self.text.draw(surface, self.prompt, self.pos, True)


class Countdown(object) :
    def __init__(self, seconds, pos, width, height, innerColour, borderColour, text, showCount = True):
        self.maxSeconds = seconds
        self.seconds = seconds
        self.pos = pos
        self.width = width
        self.height = height
        self.finished = False
        self.text = text
        self.innerColour = innerColour
        self.borderColour = borderColour
        self.fullRect = Rect(pos, (width, height))
        self.rect = Rect(pos, (width, height))
        self.showCount = showCount

    def draw(self, surface):
        pygame.draw.rect(surface, self.innerColour, self.rect)
        pygame.draw.rect(surface, self.borderColour, self.fullRect, 2)

        if self.showCount:
            x, y = self.pos
            x = x + self.width / 2
            pos = (x, y)
            self.text.draw(surface, "%02d" % self.seconds, pos, True)

    def reset(self):
        self.finished = False
        self.seconds = self.maxSeconds

    def update(self, deltaTime):
        if self.seconds == 0:
            return
        self.seconds = self.seconds - deltaTime
        if self.seconds < 0:
            self.seconds = 0
            self.finished = True
        progressWidth = self.width * (self.seconds / self.maxSeconds)
        self.rect = Rect(self.pos, (progressWidth, self.height))
