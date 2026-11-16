import random

class Mastermind:
    def __init__(self, code_length, allow_duplicates):
        self.code_length = code_length
        self.allow_duplicates = allow_duplicates
        #red, blue, green, yellow, purple, orange
        self.colors = ["R", "B", "G", "Y", "P", "O"]
        self.max_turns = 12

        self.secret_code = self.generate_secret_code()
        self.board = []
        self.won = False
        self.game_over = False

    def turn(self, guess):
        unmatched_guess = []
        unmatched_secret = []
        pins = []

        for i in range(self.code_length):
            if guess[i] == self.secret_code[i]:
                pins.append("R")
            else:
                unmatched_guess.append(guess[i])
                unmatched_secret.append(self.secret_code[i])

        for color in unmatched_guess:
            if color in unmatched_secret:
                pins.append("W")
                unmatched_secret.remove(color)

        while len(pins) < self.code_length:
            pins.append("B")

        random.shuffle(pins)
        self.board.append({
            "Guess": guess,
            "Pins": pins
        })

        if guess == self.secret_code:
            self.won = True

        if self.won or len(self.board) == self.max_turns:
            self.game_over = True


    def valid_guess(self, guess):
        if len(guess) != self.code_length:
            return False

        for color in guess:
            if color not in self.colors:
                return False

        return True
        
    def generate_secret_code(self):
        colors = self.colors[:]
        secret_code = []

        while len(secret_code) < self.code_length:
            color = random.choice(colors)
            secret_code.append(color)

            if not self.allow_duplicates:
                colors.remove(color)

        return secret_code
