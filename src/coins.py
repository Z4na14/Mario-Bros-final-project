import time
class Coins:
    def __init__(self, collideX, collideY):
        # Basic stuff
        self.collideX = collideX
        self.collideY = collideY
        self.posX = 0
        self.posY = 0
        self.time = 0
        

        # I don´t know if I should be adding this as they're just going to be spawning on the top
        self.isFalling = True
        self.isOver = False
        self.currPlat = None

        # Animation (idk how to know which to put from the file)
        self.stillframe = [0, 0, 0, 0]
        # The phase is only used in moving animations
