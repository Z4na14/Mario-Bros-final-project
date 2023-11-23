import pyxel
import characters
import levels
import os


class App:
    def __init__(self, dimx, dimy, mario: object, screens: list, dir):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param mario: Class of the main character
        TO DO: Add collider check creating simple blocks (Use another
        class for every object)
        """

        self.dimX = dimx
        self.dimY = dimy
        pyxel.init(dimx, dimy)

        self.mario = mario
        self.screens = screens

        self.currlv = 0
        self.currplatforms = self.screens[self.currlv].platforms
        self.currpipes = self.screens[self.currlv].pipes

        pyxel.load(f"{dir}/resources/texture.pyxres", True, False, False, False)
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
        pyxel.blt(self.mario.posX, self.mario.posY, 0, self.mario.currframe[0],
                  self.mario.currframe[1], self.mario.currframe[2], self.mario.currframe[3])

        for i in range(len(self.currplatforms)):
            pyxel.rect(self.currplatforms[i].positionX, self.currplatforms[i].positionY,
                       self.currplatforms[i].width, self.currplatforms[i].height, 3)
        for i in range(len(self.currpipes)):
            pyxel.rect(self.currpipes[i][0], self.currpipes[i][1], 10, 10, 1)

"""
screen1 = levels.Screen(1)
"""

screen2 = levels.Screen(2, [levels.Platform(0, 35, 44, 3),
                            levels.Platform(116, 35, 44, 3),
                            levels.Platform(0, 85, 44, 3),
                            levels.Platform(116, 85, 44, 3),
                            levels.Platform(58, 60, 44, 3),
                            levels.Platform(0, 35, 44, 3),
                            levels.Platform(0, 117, 160, 3)],
                        [[0, 10], [150, 10]])
"""
screen2 = levels.Screen(3)
screen2 = levels.Screen(4)
"""

App(160, 120, characters.Mario(16, 21), [screen2], os.getcwd())