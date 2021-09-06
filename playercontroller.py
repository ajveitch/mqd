from gpiozero import Button, OutputDevice

class PlayerController(object):
    def __init__(self, buttonPlayer, buttonStart, buttonStop, buttonReset, outputRelays):
        self.buttons = []
        self.relays = []
        self.start = Button(buttonStart, pull_up = False)
        self.stop = Button(buttonStop, pull_up = False)
        self.reset = Button(buttonReset, pull_up = False)
        self.score = 0
        for pin in buttonPlayer:
            self.buttons.append(Button(pin, pull_up = False))
        for pin in outputRelays:
            self.relays.append(OutputDevice(pin, active_high = True, initial_value = False))

    def anyButton(self):
        for button in self.buttons:
            if button.is_pressed:
                return True
        return False

    def playerChoice(self):
        index = 0
        for button in self.buttons:
            if button.is_pressed:
                return index
            index = index + 1
        return -1

    def startButton(self):
        if self.start.is_pressed:
            return True
        return False

    def stopButton(self):
        if self.stop.is_pressed:
            return True
        return False
    
    def resetButton(self):
        if self.reset.is_pressed:
            return True
        return False

    def outputExclusive(self, index):
        for relay in self.relays:
            relay.off()
        self.relays[index].on()

    def outputOff(self):
        for relay in self.relays:
            relay.off()

