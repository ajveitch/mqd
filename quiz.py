#!/usr/bin/env python3

import os
import sys

old_so = sys.stdout
devnull = open(os.devnull, 'w')
sys.stdout = devnull
import pygame
sys.stdout = old_so

from gamerunner import GameRunner
from questions import *
from headertextscreen import HeaderTextScreen
from playercontroller import PlayerController
from currentquestion import CurrentQuestion
from choosequestion import ChooseQuestion
from showquestion import ShowQuestion
from showcountdown import ShowCountdown
from getquestionanswer import GetQuestionAnswer
from showanswers import ShowAnswers
from showscore import ShowScore
from ui import GameAudio

BUTTON_START = 23
BUTTON_STOP = 24
BUTTON_RESET = 13
BUTTON_A = 25
BUTTON_B = 5
BUTTON_C = 6
BUTTON_D = 12
INPUT_BUTTONS = [ BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_D ]

RELAY_A = 4
RELAY_B = 17
RELAY_C = 18
RELAY_D = 27
RELAY_SPARE = 22
OUTPUT_RELAYS = [ RELAY_A, RELAY_B, RELAY_C, RELAY_D ]

COUNTDOWN_SECS = 30
ANSWER_COUNTDOWN_SECS = 5

if os.geteuid() != 0:
    exit("You need to have root privileges to run this.\nPlease try again, this time using 'sudo'. Exiting.")

pygame.init()
pygame.mouse.set_visible(False)

audio = GameAudio()

player = PlayerController(INPUT_BUTTONS, BUTTON_START, BUTTON_STOP, BUTTON_RESET, OUTPUT_RELAYS)
currentQuestion = CurrentQuestion()

questions = loadQuestions("questions.json")

showScore = ShowScore(audio, None, player)
showAnswers = ShowAnswers(audio, showScore, currentQuestion, player, ANSWER_COUNTDOWN_SECS)
getQuestionAnswer = GetQuestionAnswer(showAnswers, currentQuestion, player)
showCountDown = ShowCountdown(audio, getQuestionAnswer, currentQuestion, player, COUNTDOWN_SECS)
showQuestion = ShowQuestion(audio, showCountDown, currentQuestion, player)
chooseQuestion = ChooseQuestion(showQuestion, showScore, currentQuestion, questions)

splashScreen = HeaderTextScreen(audio, chooseQuestion, player)
splashScreen.setHeader("The Million Q.U.I.D. Drop")
splashScreen.setSub("Press START to begin")

showAnswers.nextState = chooseQuestion
showScore.nextState = splashScreen

game = GameRunner((800, 600), "The Million Q.U.I.D. Drop", (0, 0, 0), splashScreen)

lastState = None
while game.state != None:
    nextState = game.update()
    if nextState != lastState:
        if game.state != None:
            game.state.onExit()
        if nextState != None:
            nextState.onEnter()
        lastState = nextState
    game.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.state = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                game.state = None
pygame.quit()
