import pyxel
import characters
import levels


class App:
    def __init__(self, dimx, dimy, mario: object, screens: list):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param mario: Class of the main character
        TO DO: Add collider check creating simple blocks (Use another
        class for every object)
        """

        self.dimX = dimx
        self.dimY = dimy

        self.mario = mario
        self.screens = screens

        self.currlv = 0
        self.currplatforms = self.screens[self.currlv].platforms

        pyxel.init(dimx, dimy)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Loop that checks whether the character is over a platform or not
        for i in range(len(self.currplatforms)):
            if ((self.currplatforms[i].positionY - 10) <= (self.mario.posY + 10) \
                    <= self.currplatforms[i].positionY):

                if self.currplatforms[i].positionX <= self.mario.posX <= \
                        (self.currplatforms[i].positionX + self.currplatforms[i].width):
                    self.mario.isOver = True
                    self.mario.currPlat = self.currplatforms[i]

                else:
                    self.mario.isOver = False
                    self.mario.currPlat = []

        # Check if the position of the character must be higher
        if self.mario.velY > 0 and self.mario.isFalling == False:
            self.mario.posY -= self.mario.velY
            self.mario.velY -= 1

            # Mario falls after reaching peak
            if self.mario.velY <= 0:
                self.mario.isFalling = True
                self.mario.velY = 0

        elif self.mario.isFalling:
            if self.mario.isOver:
                self.mario.posY = self.mario.currPlat.positionY - 10
                self.mario.isFalling = False
                self.mario.velY = -1

            else:
                if self.mario.velY < 9:
                    self.mario.velY += 1

                self.mario.posY += self.mario.velY

        elif not self.mario.isFalling:
            if not self.mario.isOver:
                self.mario.isFalling = True
                self.mario.velY = 0

        # Check for horizontal movement
        if self.mario.mX != 0:
            self.mario.posX += self.mario.mX
            self.mario.mX = 0

            # Check if character leaves screen
            if self.mario.posX < -10:
                self.mario.posX = self.dimX + 5

            elif self.mario.posX > self.dimX + 10:
                self.mario.posX = -5

        # Exec the functions for the movement
        if pyxel.btnp(pyxel.KEY_W):
            self.mario.movement('up')

        elif pyxel.btn(pyxel.KEY_A):
            self.mario.movement('left')

        elif pyxel.btn(pyxel.KEY_D):
            self.mario.movement('right')

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.mario.posX, self.mario.posY, 5, 10, 2)
        for i in range(len(self.currplatforms)):
            pyxel.rect(self.currplatforms[i].positionX, self.currplatforms[i].positionY,
                       self.currplatforms[i].width, self.currplatforms[i].height, 3)


screen1 = levels.Screen(1, [levels.Platform(0, 20, 30, 5),
                            levels.Platform(30, 40, 30, 5),
                            levels.Platform(90, 60, 30, 5),
                            levels.Platform(0, 115, 160, 5)],
                        [[0, 10], [150, 10]])

App(160, 120, characters.Mario(10, 10), [screen1])
