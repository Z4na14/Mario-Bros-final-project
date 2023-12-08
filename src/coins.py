import time
class Coin:
    def __init__(self, value, collideX, collideY, direction):
        self.posX = 0
        self.posY = 0
        self.collideX = collideX
        self.collideY = collideY
        self.direction = direction
        self.velY = 0
        self.value = value  # Represents the value of the coin (I thought it was simple and
                            # could add an extra layer of gameplay)
        self.isCollected = False

        # Status checks
        self.isFalling = True
        self.isOver = False

        # Related to animations
        self.currentSetFrames = []
        self.currentPhaseFrame = 0
        self.currframe = []
        self.currPlat = None

    def movement(self, dimX):
        # Automatic movement to the direction set
        if not self.isCollected:
            self.posX += self.direction

            # Check if coin leaves the screen
            if self.posX < 0:
                self.posX = dimX
                self.posY -= 2
            elif self.posX > dimX:
                self.posX = 0
                self.posY -= 2

            # Animations (same as enemies)
            self.currframe = deepcopy(self.currentSetFrames[self.currentPhaseFrame])
            self.currframe[2] = self.currframe[2] * self.direction

            if self.currentPhaseFrame == 2:
                self.currentPhaseFrame = 0
            elif self.currentPhaseFrame != 2:
                if pyxel.frame_count % 3 == 0:
                    self.currentPhaseFrame += 1

            # Make the gravity (same es enemies)
            if self.isFalling:
                if self.isOver:
                    self.posY = self.currPlat.positionY - self.collideY
                    self.isFalling = False
                    self.velY = -1

                else:
                    if self.velY < 8:
                        self.velY += 1
                    self.posY += self.velY

            # Check if coin is still over a platform
            elif not self.isFalling:
                if not self.isOver:
                    self.isFalling = True
                    self.velY = 0

    def collect(self):
        # Perform actions when the coin is collected
        self.isCollected = True
        # Additional actions, if any, when the coin is collected
