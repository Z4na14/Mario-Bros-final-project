"""
Final project for a university class, all the progress is uploaded
in https://github.com/Z4na14/Mario-Bros-final-project
Authors:
    Jorge Adrian Saghin Dudulea (zanajorgesaghin@gmail.com)
    Antonio Nicolas Lemus Yeguas
"""

import pyxel
import characters
import levels
from os import getcwd


class App:
    def __init__(self, dimx, dimy, mario: object, screens: list, enemies: list, directory):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param mario: Class of the main character
        """

        self.dimX = dimx
        self.dimY = dimy
        pyxel.init(dimx, dimy, fps=30)

        self.mario = mario
        self.screens = screens
        self.enemies = enemies

        self.currlv = 0
        self.currplatforms = self.screens[self.currlv].platforms
        self.currenemies = self.enemies[self.currlv]
        self.currpipes = self.screens[self.currlv].pipes

        # Set the spawn point for all the enemies at the pipes
        for i, a in enumerate(self.currenemies):
            if i % 2 == 0:
                a.posX = self.currpipes[0][0]
            elif i % 2 != 0:
                a.posX = self.currpipes[1][0]
            a.posY = self.currpipes[0][1]

        pyxel.load(f"{directory}/resources/texture.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.mario.checkIsOver(self.currplatforms)
        self.mario.checkMovement(self.dimX, self.currplatforms)

        for i in self.currenemies:
            i.checkIsOver(self.currplatforms)
            i.movement(self.dimX)

            if self.mario.kickPos != [0, 0, None]:
                if (self.mario.kickPos[1]-13) <= i.posY <= (self.mario.kickPos[1] - 5):
                    if self.mario.kickPos[0]-5 <= (i.posX + i.collideX // 2) <= \
                            (self.mario.kickPos[0] + 16):
                        i.kickFall("turn")

                self.currplatforms[self.mario.kickPos[2]].kick(self.mario.kickPos[0],
                                                               self.mario.kickPos[1],
                                                               "block")

        for i in self.currplatforms:
            if i.kickStatus:
                tempKick = i.aniKick()
                if tempKick:
                    self.mario.kickPos = [0, 0, None]

        # Exec the functions for the movement
        if pyxel.btnp(pyxel.KEY_W):
            self.mario.movement('up')

        elif pyxel.btn(pyxel.KEY_A):
            self.mario.movement('left')

        elif pyxel.btn(pyxel.KEY_D):
            self.mario.movement('right')

        # TEMPORAL: Change status of crab (Debug)
        elif pyxel.btnp(pyxel.KEY_P):
            self.currenemies[1].changeStatus()

        elif pyxel.btnp(pyxel.KEY_O):
            self.currplatforms[0].kick(20, 45, "block")

    def draw(self):
        pyxel.cls(0)

        pyxel.blt(self.mario.posX, self.mario.posY, 0, self.mario.currframe[0],
                  self.mario.currframe[1], self.mario.currframe[2], self.mario.currframe[3], colkey=0)

        for i in self.currenemies:
            if i == "Turtle":
                pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3], colkey=8)
            elif i == "Crab":
                pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3], colkey=11)

        pyxel.bltm(0, 0, 0, 0, 0, 240, 200, colkey=8)

        for i in self.currplatforms:
            if i.kickStatus:
                pyxel.blt(i.kickX, i.kickY, 0, i.framesPlatform[i.currPhaseFrame][0],
                          i.framesPlatform[i.currPhaseFrame][1], i.framesPlatform[i.currPhaseFrame][2],
                          i.framesPlatform[i.currPhaseFrame][3], colkey=8)
        """
        for i in range(len(self.currplatforms)):
            pyxel.rect(i.positionX, i.positionY,
                       i.width, i.height, 3)
        
        for i in range(len(self.currpipes)):
            pyxel.rect(self.currpipes[i][0], self.currpipes[i][1], 10, 10, 1)
        """


# On top of the measures of the platforms, we need to add the lenght of mario (function)
screen1 = levels.Screen(2, [levels.Platform(0, 48, 72, 8),
                            levels.Platform(168, 48, 72, 8),
                            levels.Platform(48, 96, 144, 8),
                            levels.Platform(0, 144, 72, 8),
                            levels.Platform(168, 144, 72, 8),
                            levels.Platform(0, 192, 240, 8)],
                        [[0, 30], [230, 30]])

enemies1 = [characters.Turtle("Turtle", 16, 16, 1), characters.Crab("Crab", 16, 16, 0 - 1)]

App(240, 200, characters.Mario(16, 21), [screen1], [enemies1], getcwd())
