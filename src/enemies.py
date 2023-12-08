from copy import deepcopy
import pyxel


class Enemies:
    def __init__(self, enemy, collideX, collideY):
        # Same properties as mario
        self.posX = 0
        self.posY = 0
        self.collideX = collideX
        self.collideY = collideY
        self.direction = 1
        self.velY = 0
        self.mX = 1
        self.isDed, self.timeDed = False, -1
        self.isSpawning, self.timeSpawning = False, 0
        self.isFlipped = False
        self.enemy = enemy

        # Status checks
        self.isFalling = True
        self.isOver = False

        # Related to animations
        self.currentSetFrames = []
        self.currentPhaseFrame = 0
        self.currframe = []
        self.currPlat = None

    def __str__(self):
        return self.enemy

    def __eq__(self, enemy):
        return enemy == self.enemy

    def movement(self, dimX):
        # Automatic movement to the direction set
        self.posX += self.mX * self.direction

        if self.isDed and self.isFlipped:
            if self.velY > 0:
                self.posY -= self.velY
                self.velY -= 1

            elif self.velY <= 0:
                if self.velY > 0 - 8:
                    self.velY -= 1
                self.posY -= self.velY

        if self.isFlipped:
            # Animating the enemy when fallen
            self.currframe = deepcopy(self.currentSetFrames[self.currentPhaseFrame])
            self.currframe[2] = self.currframe[2] * self.direction

            if pyxel.frame_count % 3 == 0:
                if self.currentPhaseFrame == 1:
                    self.currentPhaseFrame = 0
                elif self.currentPhaseFrame != 1:
                    self.currentPhaseFrame += 1

        elif not self.isDed:
            # Check if character leaves screen
            if self.posX < 0:
                self.posX = dimX
                self.posY -= 2

            elif self.posX > dimX:
                self.posX = 0
                self.posY -= 2

            # Animating the enemies
            self.currframe = deepcopy(self.currentSetFrames[self.currentPhaseFrame])
            self.currframe[2] = self.currframe[2] * self.direction
            if pyxel.frame_count % 3 == 0:
                if self.currentPhaseFrame == 2:
                    self.currentPhaseFrame = 0
                elif self.currentPhaseFrame != 2:
                    self.currentPhaseFrame += 1

            if not self.isSpawning:
                # Make the gravity
                if self.isFalling:
                    if self.isOver:
                        self.posY = self.currPlat.positionY - self.collideY
                        self.isFalling = False

                    else:
                        if self.velY < 8:
                            self.velY += 1
                        self.posY += self.velY

                # Check if enemy is still over a platform
                elif not self.isFalling:
                    if not self.isOver:
                        self.isFalling = True
                        self.velY = 0

    def checkIsOver(self, currplatforms):
        for i in currplatforms:
            if not self.isDed:
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

    """
    TO DO: Finish mario check when hes over the flipped enemies to kill them
    """

    def kickFall(self, state, time=-1):
        if state == "turn":
            self.isFlipped = True
            self.mX = 0
            # Set state and animation
            self.currentSetFrames = self.fallenFrames
            self.currentPhaseFrame = 0

        elif state == "fall":
            # Create movement
            self.velY = 7
            self.mX = 1

            self.isDed = True
            self.timeDed = time


class Turtle(Enemies):
    def __init__(self, enemy, collideX, collideY):
        super().__init__(enemy, collideX, collideY)
        self.currentSetFrames = [[0, 24, -16, 16], [16, 24, -16, 16], [32, 24, -16, 16]]
        self.fallenFrames = [[96, 24, 16, 16], [112, 24, 16, 16]]


class Crab(Enemies):
    def __init__(self, enemy, collideX, collideY):
        super().__init__(enemy, collideX, collideY)
        self.status = "normal"

        self.movingFramesNormal = [[0, 40, 16, 16], [16, 40, 16, 16], [32, 40, 16, 16], [48, 40, 16, 16]]
        self.movingFramesAngry = [[88, 40, 16, 16], [104, 40, 16, 16], [120, 40, 16, 16], [136, 40, 16, 16]]
        self.fallenFrames = [[152, 40, 16, 16], [168, 40, 16, 16]]

        self.currentSetFrames = self.movingFramesNormal

    def changeStatus(self):
        self.status = "angry"
        self.currentSetFrames = self.movingFramesAngry
        self.mX = 2


class Fly(Enemies):
    def __init__(self, enemy, collideX, collideY):
        super().__init__(enemy, collideX, collideY)

        self.movingFrames = [[48, 56, 16, 16], [32, 56, 16, 16], [48, 56, 16, 16], [0, 56, 16, 16]]
        self.fallenFrames = [[64, 56, 16, 16], [80, 56, 16, 16]]

        self.currentSetFrames = self.movingFrames
        self.jumping = False

    def movement(self, dimX, platforms):
        if pyxel.frame_count // 7 and self.velY == 0:
            self.velY = 8
            self.jumping = True

        if self.jumping:
            self.posX += self.mX * self.direction

            # Make the gravity
            if not self.isFalling:
                if self.checkIsUnder(platforms):
                    self.isFalling = True
                    self.velY = 0

                else:
                    self.posY -= self.velY
                    self.velY -= 1

            elif self.isFalling:
                if self.isOver:
                    self.posY = self.currPlat.positionY - self.collideY
                    self.isFalling = False
                    self.jumping = False
                    self.velY = 0

                else:
                    if self.velY < 8:
                        self.velY += 1
                    self.posY += self.velY

    def checkIsUnder(self, currplatform):
        for a, i in enumerate(currplatform):
            if (i.positionY + i.height) <= self.posY <= \
                    (i.positionY + i.height + 8):
                # Then checks if it is also in the right position of the platform
                if i.positionX <= self.posX <= (i.positionX + i.width) \
                        or i.positionX <= (self.posX + self.collideX) <= \
                        (i.positionX + i.width):
                    self.posY = i.positionY + i.height
                    return True
