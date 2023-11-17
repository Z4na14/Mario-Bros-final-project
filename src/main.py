import pyxel
import characters
import levels


class App:
    def __init__(self, dimx, dimy, mario: object, screens: list):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param marioClass: Class of the main character
        TO DO: Add collider check creating simple blocks (Use another
        class for every object)
        """

        self.dimX = dimx
        self.dimY = dimy

        self.mario = mario
        self.screens = screens

        self.currlv = 0
        self.currplatforms = self.screens[self.currlv].platforms
        print(self.currplatforms[0].positionX, self.currplatforms[0].positionY,
              self.currplatforms[0].width, self.currplatforms[0].height)
        print(pyxel.colors.to_list())

        pyxel.init(dimx, dimy)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Check if the position of the character must be higher
        if self.mario.mY < 0:
            self.mario.posY -= 4
            self.mario.mY += 4

            # Mario falls after reaching peak
            if self.mario.mY == 0:
                self.mario.mY = 24

        elif self.mario.mY > 0:
            self.mario.posY += 4
            self.mario.mY -= 4

        # Check for horizontal movement
        if self.mario.mX != 0:
            self.mario.posX += self.mario.mX
            self.mario.mX = 0

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
                            levels.Platform(90, 60, 30, 5)],
                        [[0, 10], [150, 10]])

App(160, 120, characters.Mario(10, 10), [screen1])
