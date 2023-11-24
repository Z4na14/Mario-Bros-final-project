from copy import deepcopy

class Mario:
    def __init__(self, collideX, collideY):
        """
        :param collideX:
        :param collideY:
        I would leave the colliders, but they are going to be fixed
        to Mario
        """
        self.collideX = collideX
        self.collideY = collideY
        self.posX = 110
        self.posY = 170
        self.velY = 0
        self.mX = 0

        self.isFalling = True
        self.isOver = False
        self.currPlat = None

        self.runframes = [[16, 3, 16, 21],[32, 3, 16, 21],[48, 3, 16, 21]]
        self.stillframe = [0, 3, 15, 21]
        self.currframe = self.stillframe
        self.currPhaseFrame = 0
        self.direction = 1

    def movement(self, command, currPhase = 0):
        if command == 'up':
            if self.velY == -1 and self.isFalling == False:
                self.velY = 10

        elif command == 'left':
            if self.mX == 0:
                self.mX -= 4
                self.direction = -1

                # We invert the sprite when moving to the left
                self.currframe = deepcopy(self.runframes[self.currPhaseFrame])
                self.currframe[2] = self.currframe[2] * self.direction

                if self.currPhaseFrame == 2:
                    self.currPhaseFrame = 0
                elif self.currPhaseFrame != 2:
                    self.currPhaseFrame += 1

        elif command == 'right':
            if self.mX == 0:
                self.mX += 4
                self.direction = 1
                self.currframe = self.runframes[self.currPhaseFrame]

                if self.currPhaseFrame == 2:
                    self.currPhaseFrame = 0
                elif self.currPhaseFrame != 2:
                    self.currPhaseFrame += 1

    def checkMovement(self, dimX):
        # Check if the position of the character must be higher
        if self.velY > 0 and self.isFalling == False:
            self.posY -= self.velY
            self.velY -= 1

            # Mario falls after reaching peak
            if self.velY <= 0:
                self.isFalling = True
                self.velY = 0

        # Make the gravity
        elif self.isFalling:
            if self.isOver:
                self.posY = self.currPlat.positionY - self.collideY
                self.isFalling = False
                self.velY = -1

            else:
                if self.velY < 10:
                    self.velY += 1
                self.posY += self.velY

        # Check if Mario is still over a platform
        elif not self.isFalling:
            if not self.isOver:
                self.isFalling = True
                self.velY = 0

        # Check for horizontal movement
        if self.mX != 0:
            self.posX += self.mX
            self.mX = 0

            """
            NEEDS CHANGE, WORKS REALLY BAD
            """
            # Check if character leaves screen
            if self.posX < 0:
                self.posX = dimX
                # TEMPORAL CHANGE, WE SHOULD DO IT SEAMLESSLY
                """
                Character falls from the platform when stopping
                right in the border of the screen
                TO DO: Solve bug
                """
                self.posY -= 2

            elif self.posX > dimX:
                self.posX = 0
                # HERE TOO
                self.posY -= 2

        elif self.mX == 0:
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



class Enemies:
    def __init__(self, collideX, collideY):
        self.collideX = collideX
        self.collideY = collideY
        self.direction = 1

        self.posX = 50
        self.posY = 50
        self.velY = 0
        self.isFalling = False
        self.isOver = False
        self.currPlat = None

"""
class Turtle(Enemies):
    def __init__(self):
    def movement(self):
"""

"""
class Crab(Enemies):
    def __init__(self):
    def movement(self):
"""

