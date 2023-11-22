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
        self.currpipes = self.screens[self.currlv].pipes

        pyxel.init(dimx, dimy)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.mario.checkIsOver(self.currplatforms)
        self.mario.checkMovement(self.dimX)

        # Exec the functions for the movement
        if pyxel.btnp(pyxel.KEY_W):
            self.mario.movement('up')

        elif pyxel.btn(pyxel.KEY_A):
            self.mario.movement('left')

        elif pyxel.btn(pyxel.KEY_D):
            self.mario.movement('right')

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.mario.posX, self.mario.posY, self.mario.collideX, self.mario.collideY, 2)
        for i in range(len(self.currplatforms)):
            pyxel.rect(self.currplatforms[i].positionX, self.currplatforms[i].positionY,
                       self.currplatforms[i].width, self.currplatforms[i].height, 3)
        for i in range(len(self.currpipes)):
            pyxel.rect(self.currpipes[i][0], self.currpipes[i][1], 10, 10, 1)

"""
screen1 = levels.Screen(1)
"""

screen2 = levels.Screen(2, [levels.Platform(0, 36, 42, 1),
                            levels.Platform(118, 36, 42, 1),
                            levels.Platform(59, 70, 42, 1),
                            levels.Platform(0, 90, 42, 1),
                            levels.Platform(59, 90, 42, 1),
                            levels.Platform(0, 116, 160, 1)],
                        [[0, 10], [150, 10]])
"""
screen2 = levels.Screen(3)
screen2 = levels.Screen(4)
"""

App(160, 120, characters.Mario(10, 10), [screen2])