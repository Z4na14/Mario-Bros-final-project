from copy import deepcopy
import pyxel


class Mario:
    def __init__(self, collideX, collideY):
        """
        :param collideX: Collision width of mario
        :param collideY: Collision height of mario
        """
        # Basic properties of the character
        self.collideX = collideX
        self.collideY = collideY
        self.posX = 110
        self.posY = 170
        # Used for vertical movement
        self.velY = 0
        # Used for horizontal movement
        self.mX = 0

        # Status checks
        self.isFalling = True
        self.isOver = False
        self.currPlat = None

        # Related to animations (All frames are taken from the pyxres file)
        self.runframes = [[16, 3, 16, 21], [32, 3, 16, 21], [48, 3, 16, 21]]
        self.stillframe = [192, 3, 16, 21]
        self.jumpframe = [64, 1, 16, 23]
        self.currframe = self.stillframe
        # The phase is only used in moving animations
        self.currPhaseFrame = 0
        self.direction = 1

    def movement(self, command):
        """
        :param command: Execute the following keyboard press
        """
        if command == 'up':
            if self.velY == -1 and not self.isFalling:
                self.velY = 10

        elif command == 'left':
            if self.mX == 0:
                self.mX -= 4
                self.direction = -1

                if self.isOver:
                    # We invert the sprite when moving to the left
                    self.currframe = deepcopy(self.runframes[self.currPhaseFrame])
                    self.currframe[2] = self.currframe[2] * self.direction

                    # Change the frame of the animation only on even global frames
                    if self.currPhaseFrame == 2:
                        self.currPhaseFrame = 0
                    elif self.currPhaseFrame != 2:
                        if pyxel.frame_count % 2 == 0:
                            self.currPhaseFrame += 1

        elif command == 'right':
            if self.mX == 0:
                self.mX += 4
                self.direction = 1

                if self.isOver:
                    self.currframe = self.runframes[self.currPhaseFrame]

                    if self.currPhaseFrame == 2:
                        self.currPhaseFrame = 0
                    elif self.currPhaseFrame != 2:
                        if pyxel.frame_count % 2 == 0:
                            self.currPhaseFrame += 1

    def checkMovement(self, dimX, currplatforms):
        # Check if the position of the character must be higher
        if self.velY > 0 and not self.isFalling:
            self.posY -= self.velY
            self.velY -= 1

            # Set the frame of the jump
            self.currframe = deepcopy(self.jumpframe)
            self.currframe[2] = self.currframe[2] * self.direction

            # Mario falls after reaching peak
            if self.velY <= 0 or self.checkIsUnder(currplatforms):
                self.isFalling = True
                self.velY = 0

        # Make the gravity
        elif self.isFalling:
            if self.isOver:
                """
                If it is over a platform, we set the Y position to be
                over the platform and change the respective status and mario frame.
                """
                self.posY = self.currPlat.positionY - self.collideY
                self.isFalling = False
                self.velY = -1
                self.currframe = self.stillframe

            else:
                """
                If not over platform, keep falling until a certain velocity
                and set mario frames
                """
                if self.velY < 10:
                    self.velY += 1
                self.posY += self.velY
                self.currframe = deepcopy(self.jumpframe)
                self.currframe[2] = self.currframe[2] * self.direction

        # Check if Mario is still over a platform and make him fall
        elif not self.isFalling:
            if not self.isOver:
                self.isFalling = True
                self.velY = 0

        # Check for horizontal movement
        if self.mX != 0:
            if not self.checkIsParallel(currplatforms):
                self.posX += self.mX
                self.mX = 0

                """
                TO DO: Mario falls when standing right
                in the corner.
                """
                # Check if character leaves screen
                if self.posX < 0:
                    self.posX = dimX
                    self.posY -= 2

                elif self.posX > dimX:
                    self.posX = 0
                    self.posY -= 2

        # Set the still frame when mario is not moving
        elif self.mX == 0 and self.isOver:
            self.currframe = deepcopy(self.stillframe)
            self.currframe[2] = self.currframe[2] * self.direction

    def checkIsOver(self, currplatforms):
        # Loop that checks whether the character is over a platform or not
        # First looks if the character is parallel to a platform
        for i in range(len(currplatforms)):
            if (currplatforms[i].positionY - 8) <= (self.posY + self.collideY) <= currplatforms[i].positionY:
                # Then checks if it is also in the right position of the platform
                if currplatforms[i].positionX <= (self.posX + (self.collideX // 2)) <= (
                        currplatforms[i].positionX + currplatforms[i].width):
                    # Then we add a bool to pass to the rest of the program that is over
                    # a platform and the characteristics of that platform
                    self.isOver = True
                    self.currPlat = currplatforms[i]
                    return  # Exit the loop since we found the platform

        # If no platform is found, set isOver to False
        self.isOver = False
        self.currPlat = None

    def checkIsUnder(self, currplatforms):
        # Same as before but checking if it is under the platform
        for i in range(len(currplatforms)):
            if (currplatforms[i].positionY + currplatforms[i].height) <= self.posY + 2 <= \
                    (currplatforms[i].positionY + currplatforms[i].height):
                # Then checks if it is also in the right position of the platform
                if currplatforms[i].positionX <= (self.posX + (self.collideX // 2)) <= (
                        currplatforms[i].positionX + currplatforms[i].width):
                    self.posY = currplatforms[i].positionY + currplatforms[i].height
                    return True

        return False

    """
    NOT WORKING
    TO DO: Repair the frontal collision
    """

    def checkIsParallel(self, currplatforms):
        for i in range(len(currplatforms)):
            if (currplatforms[i].positionX + currplatforms[i].width) <= self.posX <= \
                    (currplatforms[i].positionX + currplatforms[i].width + 4) or \
                    currplatforms[i].positionX >= (self.posX + self.collideX) >= (currplatforms[i].positionX - 4):
                if (self.posY - 1) >= currplatforms[i].positionY >= (self.posY + self.collideY + 1):
                    return True

        return False


class Enemies:
    def __init__(self, enemy, collideX, collideY, direction):
        # Same properties as mario
        self.posX = 0
        self.posY = 0
        self.collideX = collideX
        self.collideY = collideY
        self.direction = direction
        self.velY = 0
        self.mX = 2
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

    def __repr__(self):
        return self.__str__()

    def movement(self):
        # Automatic movement to the direction set
        self.posX += self.mX * self.direction

        # Animating the enemies
        self.currframe = deepcopy(self.currentSetFrames[self.currentPhaseFrame])
        self.currframe[2] = self.currframe[2] * self.direction

        if self.currentPhaseFrame == 2:
            self.currentPhaseFrame = 0
        elif self.currentPhaseFrame != 2:
            if pyxel.frame_count % 3 == 0:
                self.currentPhaseFrame += 1

        # Make the gravity
        if self.isFalling:
            if self.isOver:
                self.posY = self.currPlat.positionY - self.collideY
                self.isFalling = False
                self.velY = -1

            else:
                if self.velY < 10:
                    self.velY += 1
                self.posY += self.velY

        # Check if enemy is still over a platform
        elif not self.isFalling:
            if not self.isOver:
                self.isFalling = True
                self.velY = 0

    def checkIsOver(self, currplatforms):
        for i in range(len(currplatforms)):
            if (currplatforms[i].positionY - 8) <= (self.posY + self.collideY) <= currplatforms[i].positionY:
                # Then checks if it is also in the right position of the platform
                if currplatforms[i].positionX <= (self.posX + (self.collideX // 2)) <= (
                        currplatforms[i].positionX + currplatforms[i].width):
                    # Then we add a bool to pass to the rest of the program that is over
                    # a platform and the characteristics of that platform
                    self.isOver = True
                    self.currPlat = currplatforms[i]
                    return  # Exit the loop since we found the platform

        # If no platform is found, set isOver to False
        self.isOver = False
        self.currPlat = None


class Turtle(Enemies):
    def __init__(self, enemy, collideX, collideY, direction):
        super().__init__(enemy, collideX, collideY, direction)
        self.posX = 0
        self.posY = 10

        self.currentSetFrames = [[0, 24, -16, 16], [16, 24, -16, 16], [32, 24, -16, 16]]


class Crab(Enemies):
    def __init__(self, enemy, collideX, collideY, direction):
        super().__init__(enemy, collideX, collideY, direction)
        self.posX = 200
        self.posY = 10
        self.status = "normal"

        self.movingFramesNormal = [[0, 40, 16, 16], [16, 40, 16, 16], [32, 40, 16, 16], [48, 40, 16, 16]]
        self.movingFramesAngry = [[88, 40, 16, 16], [104, 40, 16, 16], [120, 40, 16, 16], [136, 40, 16, 16]]

        self.currentSetFrames = self.movingFramesNormal

    def changeStatus(self):
        self.status = "angry"
        self.currentSetFrames = self.movingFramesAngry
        self.mX = 3
