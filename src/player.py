from copy import deepcopy
import pyxel

"""
Hhhmmmm, spaguetti and lots of variables :D
"""


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
        self.kickPos = [0, 0, None]

        # Status checks
        self.isFalling = True
        self.isOver = False
        self.currPlat = None
        self.isDed, self.timeDed = False, -1

        # Related to animations (All frames are taken from the pyxres file)
        self.runframes = [[16, 3, 16, 21], [32, 3, 16, 21], [48, 3, 16, 21]]
        self.stillframe = [192, 3, 16, 21]
        self.jumpframe = [64, 1, 16, 23]
        self.deadframe = [112, 1, 16, 20]
        self.currframe = self.stillframe
        # The phase is only used in moving animations
        self.currPhaseFrame = 0
        self.direction = 1

    def movement(self, command):
        """
        :param command: Execute the following keyboard press
        """
        if command == 'up':
            if self.velY == 0 and not self.isFalling and not self.isDed:
                self.velY = 10

        elif command == 'left':
            if self.mX == 0 and not self.isDed:
                self.mX -= 4
                self.direction = -1

                if self.isOver:
                    # We invert the sprite when moving to the left
                    self.currframe = deepcopy(self.runframes[self.currPhaseFrame])
                    self.currframe[2] = self.currframe[2] * self.direction

                    # Change the frame of the animation only on even global frames
                    if pyxel.frame_count % 2 == 0:
                        if self.currPhaseFrame == 2:
                            self.currPhaseFrame = 0
                        elif self.currPhaseFrame != 2:
                            self.currPhaseFrame += 1

        elif command == 'right':
            if self.mX == 0 and not self.isDed:
                self.mX += 4
                self.direction = 1

                if self.isOver:
                    self.currframe = self.runframes[self.currPhaseFrame]

                    if pyxel.frame_count % 2 == 0:
                        if self.currPhaseFrame == 2:
                            self.currPhaseFrame = 0
                        elif self.currPhaseFrame != 2:
                            self.currPhaseFrame += 1

    def checkMovement(self, dimX, currplatforms, time):
        # Check if mario is dead and make him fall
        if self.isDed:
            if float(time) - float(self.timeDed) >= 3:
                self.isDed = False
                self.posX = 110
                self.posY = 170

            else:

                if self.velY > 0 and not self.isFalling:
                    self.posY -= self.velY
                    self.velY -= 1

                    if self.velY <= 0:
                        self.isFalling = True
                        self.velY = 0

                elif self.isFalling:
                    if self.velY < 15:
                        self.velY += 1
                    self.posY += self.velY

        elif not self.isDed:
            """
            TO DO: Mario falls when standing right
            in the corner.
            """
            # Check if character leaves screen
            if self.posX <= 3 or self.posX >= (dimX - 3):
                self.isFalling = False
                self.isOver = True

                if self.posX >= (dimX + 20):
                    self.posX = 0-20
                elif self.posX <= 0-20:
                    self.posX = dimX + 20

            elif 3 < self.posX < (dimX - 3):
                # Check if the position of the character must be higher
                if self.velY > 0 and not self.isFalling:
                    self.posY -= self.velY
                    self.velY -= 1

                    # Set the frame of the jump
                    self.currframe = deepcopy(self.jumpframe)
                    self.currframe[2] = self.currframe[2] * self.direction
                    self.kickPos = self.checkIsUnder(currplatforms)

                    # Mario falls after reaching peak
                    if self.velY <= 0 or self.kickPos != [0, 0, None]:
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
                        self.velY = 0
                        self.currframe = self.stillframe

                    else:
                        """
                        If not over platform, keep falling until a certain velocity
                        and set mario frames
                        """
                        if self.velY < 7:
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

            # Set the still frame when mario is not moving
            elif self.mX == 0 and self.isOver:
                self.currframe = deepcopy(self.stillframe)
                self.currframe[2] = self.currframe[2] * self.direction

    def checkIsOver(self, currplatforms):
        # Loop that checks whether the character is over a platform or not
        # First looks if the character is parallel to a platform
        for i in currplatforms:
            # Set to check under the platforms, so it sticks more smoothly
            if (i.positionY - 5) <= (self.posY + self.collideY) <= (i.positionY + 2):
                # Then checks if it is also in the right position of the platform
                if i.positionX <= self.posX <= (i.positionX + i.width) \
                        or i.positionX <= (self.posX + self.collideX) <= \
                        (i.positionX + i.width):
                    # Then we add a bool to pass to the rest of the program that is over
                    # a platform and the characteristics of that platform
                    self.isOver = True
                    self.currPlat = i
                    return  # Exit the loop since we found the platform

        # If no platform is found, set isOver to False
        self.isOver = False
        self.currPlat = None

    def checkIsUnder(self, currplatforms):
        # Same as before but checking if it is under the platform
        for a, i in enumerate(currplatforms):
            if (i.positionY + i.height) <= self.posY <= \
                    (i.positionY + i.height + 8):
                # Then checks if it is also in the right position of the platform
                if i.positionX <= self.posX <= (i.positionX + i.width) \
                        or i.positionX <= (self.posX + self.collideX) <= \
                        (i.positionX + i.width):
                    self.posY = i.positionY + i.height
                    return [self.posX, self.posY - i.height - 3, a]

        return [0, 0, None]

    def checkIsParallel(self, currplatforms):
        for i in currplatforms:
            if self.posY < i.positionY < (self.posY + self.collideY) or \
                    self.posY < (i.positionY + i.height) < \
                    (self.posY + self.collideY):
                if (i.positionX + i.width - 2) <= self.posX <= \
                        (i.positionX + i.width + 2) or \
                        (i.positionX + 2) >= (self.posX + self.collideX) >= (i.positionX - 2):
                    return True

        return False

    # Used to check whether Mario is in the range of the enemy
    def checkEnemy(self, posXenemy, posYenemy, collideXenemy, collideYenemy):
        if posYenemy <= self.posY + self.collideY <= (posYenemy + collideYenemy):
            if posXenemy <= self.posX <= (posXenemy + collideXenemy) or posXenemy <= \
                    (self.posX + self.collideX) <= (posXenemy + collideXenemy):
                return True

    # Function to execute when Mario die
    def dead(self, time, lifes):
        if not self.isDed:
            self.isDed = True
            self.timeDed = time
            self.isFalling = False
            self.velY = 10
            self.currframe = self.deadframe

            if lifes < 0:
                return True
