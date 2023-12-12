import pyxel


class Coin:
    def __init__(self, value):
        self.posX = 10
        self.posY = 24
        self.collideX = 7
        self.collideY = 11
        self.direction = 1
        self.velY = 0
        self.mX = 2

        self.value = value  # Value of the coin
        self.isCollected = False

        # Status checks
        self.isFalling = True
        self.isOver = False

        # Related to animations
        self.movingFrames = [[0, 212, 7, 11], [8, 212, 7, 11], [16, 212, 7, 11], [24, 212, 7, 11], [32, 212, 7, 11]]
        self.pickedFrames = [[40, 216, 7, 7], [40, 208, 7, 7], [48, 208, 7, 7], [58, 210, 10, 10], [73, 211, 7, 10]]

        self.currentSetFrames = self.movingFrames
        self.currentPhaseFrame = 0
        self.currframe = []
        self.currPlat = None

    def movement(self, dimX):
        # Automatic movement to the direction set
        if not self.isCollected:
            self.posX += self.mX * self.direction

            # Animating the coin
            self.currframe = self.currentSetFrames[self.currentPhaseFrame]

            if pyxel.frame_count % 2 == 0:
                if self.currentPhaseFrame == 4:
                    self.currentPhaseFrame = 0
                elif self.currentPhaseFrame != 4:
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

            if self.posX <= 3 or self.posX >= (dimX - 6):
                if self.posY < 144:
                    self.isFalling = False
                    self.isOver = True

                    if self.posX >= (dimX + 20):
                        self.posX = 0-20
                    elif self.posX <= 0-20:
                        self.posX = dimX + 20

        elif self.isCollected:
            if pyxel.frame_count % 3 == 0:
                if self.currentPhaseFrame != 5:
                    self.currframe = self.currentSetFrames[self.currentPhaseFrame]
                    self.currentPhaseFrame += 1

                elif self.currentPhaseFrame == 5:
                    self.currentPhaseFrame += 1

    def checkIsOver(self, currplatforms):
        # We check for every platform if the enemy is on top or not
        for i in currplatforms:
            if (i.positionY - 8) <= (self.posY + self.collideY) <= i.positionY:
                # Then checks if it is also in the right position of the platform
                if i.positionX <= (self.posX + (self.collideX // 2)) <= (
                        i.positionX + i.width):
                    # Then we add a bool to pass to the rest of the program that is over
                    # a platform and the characteristics of that platform
                    self.isOver = True
                    self.currPlat = i
                    return  # Exit the loop since we found the platform

            # If no platform is found, set isOver to False
            self.isOver = False
            self.currPlat = None
