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
from time import time, sleep
from re import search


class App:
    def __init__(self, dimx, dimy, mario: object, screens: list, enemies: list, directory):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param mario: Class of the main character
        """

        self.dimX = dimx
        self.dimY = dimy
        # We need the initial time, the count time, and a temporal time to check changes
        # The program executes too fast and on time event, it executes them too fast
        self.initime, self.currtime, self.temptime, self.parsedtime = time(), 0, 0, 0
        self.ingame = False
        pyxel.init(dimx, dimy, fps=30)
        pyxel.load(f"{directory}/resources/texture.pyxres")

        self.mario = mario
        self.screens = screens
        self.enemies = enemies

        # We set in memory the currently used objects
        self.currlv = 0
        self.currplatforms = self.screens[self.currlv].platforms
        self.currenemies = self.enemies[self.currlv]
        self.currpipes = self.screens[self.currlv].pipes
        # And initialize the first enemy
        self.activenemies = [self.currenemies[0]]

        # Finally we run the program
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.ingame:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.ingame = True
                self.enemiesCheck(self.activenemies[0])

        elif self.ingame:
            if len(self.currenemies) == 0 and len(self.activenemies) == 0:
                self.changeLv()

            self.parseTime()

            self.mario.checkIsOver(self.currplatforms)
            self.mario.checkMovement(self.dimX, self.currplatforms)

            for a, i in enumerate(self.activenemies):
                if self.enemiesCheck(i):
                    self.activenemies.pop(a)

            for i in self.currplatforms:
                if i.kickStatus:
                    if i.aniKick():
                        self.mario.kickPos = [0, 0, None]

            # Quit game
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

            # Exec the functions for the movement
            if pyxel.btnp(pyxel.KEY_W):
                self.mario.movement('up')

            elif pyxel.btn(pyxel.KEY_A):
                self.mario.movement('left')

            elif pyxel.btn(pyxel.KEY_D):
                self.mario.movement('right')

    def draw(self):
        pyxel.cls(0)

        if self.ingame:
            pyxel.blt(self.mario.posX, self.mario.posY, 0, self.mario.currframe[0],
                      self.mario.currframe[1], self.mario.currframe[2], self.mario.currframe[3], colkey=0)

            for i in self.activenemies:
                if i == "Turtle":
                    pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3], colkey=8)
                elif i == "Crab":
                    pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3], colkey=11)

            pyxel.bltm(0, 0, self.currlv, 0, 0, 240, 200, colkey=8)

            for i in self.currplatforms:
                if i.kickStatus:
                    pyxel.blt(i.kickX, i.kickY, 0, i.framesPlatform[i.currPhaseFrame][0],
                              i.framesPlatform[i.currPhaseFrame][1], i.framesPlatform[i.currPhaseFrame][2],
                              i.framesPlatform[i.currPhaseFrame][3], colkey=8)
            """
            for i in self.currplatforms:
                pyxel.rect(i.positionX, i.positionY,
                           i.width, i.height, 3)
            """
            """
            for i in range(len(self.currpipes)):
                pyxel.rect(self.currpipes[i][0], self.currpipes[i][1], 10, 10, 1)
            """
        elif not self.ingame:
            pyxel.bltm(0, 0, 3, 0, 0, 240, 200, colkey=8)
            pyxel.text(80, 115, "Press SPACE to begin", 9)

    # From here are just functions to make more clear the update one
    def parseTime(self):
        self.parsedtime = search(r'(.*)\.', str(time() - self.initime)).group(0)[:-1]
        if int(self.parsedtime):  # Is a check for the first frame
            if self.parsedtime != self.temptime:
                self.temptime = self.parsedtime
                if int(self.parsedtime) % 3 == 0 and len(self.currenemies) != 0:
                    self.activenemies.append(self.currenemies.pop())

    def enemiesCheck(self, i):
        if i.isDed:
            if (int(self.parsedtime) - int(i.timeDed)) > 3:
                return True

        elif not i.isDed:
            i.checkIsOver(self.currplatforms)
            i.movement(self.dimX)

            if self.mario.kickPos != [0, 0, None]:
                if (self.mario.kickPos[1] - 13) <= i.posY <= (self.mario.kickPos[1] - 5):
                    if self.mario.kickPos[0] - 5 <= (i.posX + i.collideX // 2) <= \
                            (self.mario.kickPos[0] + 16):
                        i.kickFall("turn")

                self.currplatforms[self.mario.kickPos[2]].kick(self.mario.kickPos[0],
                                                               self.mario.kickPos[1],
                                                               "block")

            if self.mario.checkEnemy(i.posX, i.posY, i.collideX, i.collideY):
                if not i.isFlipped:
                    self.mario.dead(self.parsedtime)

                elif i.isFlipped:
                    i.kickFall("fall", self.parsedtime)

            return False

    def changeLv(self):
        self.currlv += 1
        self.currplatforms = self.screens[self.currlv].platforms
        self.currenemies = self.enemies[self.currlv]
        self.currpipes = self.screens[self.currlv].pipes

        sleep(2)

        try:
            for i, a in enumerate(self.currenemies):
                if i % 2 == 0:
                    a.posX = self.currpipes[0][0]
                elif i % 2 != 0:
                    a.posX = self.currpipes[1][0]
                a.posY = self.currpipes[0][1]
        except IndexError:
            for a in self.currenemies:
                a.posX = self.currpipes[0][0]
                a.posY = self.currpipes[0][1]

        self.activenemies = [self.currenemies[0]]


screen1 = levels.Screen(1, [levels.Platform(0, 48, 72, 8),
                            levels.Platform(168, 48, 72, 8),
                            levels.Platform(48, 96, 144, 8),
                            levels.Platform(0, 144, 72, 8),
                            levels.Platform(168, 144, 72, 8),
                            levels.Platform(0, 192, 240, 8)],
                        [[0, 20], [220, 20]])

screen2 = levels.Screen(2, [levels.Platform(0, 48, 136, 8),
                            levels.Platform(192, 48, 48, 8),
                            levels.Platform(0, 96, 88, 8),
                            levels.Platform(152, 96, 88, 8),
                            levels.Platform(0, 144, 48, 8),
                            levels.Platform(104, 144, 136, 8),
                            levels.Platform(0, 192, 240, 8)],
                        [[0, 20], [220, 20]])

enemies1 = [characters.Turtle("Turtle", 16, 16, 1),
            characters.Turtle("Turtle", 16, 16, 0 - 1),
            characters.Turtle("Turtle", 16, 16, 1),
            characters.Crab("Crab", 16, 16, 0 - 1),
            characters.Crab("Crab", 16, 16, 0 - 1),
            characters.Crab("Crab", 16, 16, 0 - 1)]

enemies2 = [characters.Turtle("Turtle", 16, 16, 1),
            characters.Turtle("Turtle", 16, 16, 0 - 1),
            characters.Turtle("Turtle", 16, 16, 1),
            characters.Crab("Crab", 16, 16, 0 - 1),
            characters.Crab("Crab", 16, 16, 0 - 1),
            characters.Crab("Crab", 16, 16, 0 - 1)]

App(240, 200, characters.Mario(16, 21), [screen1, screen2], [enemies1, enemies2], getcwd())
