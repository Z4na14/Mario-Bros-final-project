"""
Final project for a university class, all the progress is uploaded
in https://github.com/Z4na14/Mario-Bros-final-project
Authors:
    Jorge Adrian Saghin Dudulea (zanajorgesaghin@gmail.com)
    Antonio Nicolas Lemus Yeguas
"""

from os import getcwd
from re import search
from time import time, sleep

import levels
import player
import pyxel
import enemies
import scoreboard
import json


class App:
    def __init__(self, dimx, dimy, mario: object, lifes: object, screens: list, enemies: list, directory, topScore):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param mario: Class of the main character
        """

        self.dimX = dimx
        self.dimY = dimy

        # We need the initial time, the count time, and a temporal time to check changes
        # The program executes too fast and on time event, it executes them too fast
        self.initime, self.temptime, self.parsedtime = time(), 0, 0
        self.ingame, self.endgame = False, False

        pyxel.init(dimx, dimy, fps=30)
        pyxel.load(f"{directory}/resources/texture.pyxres")

        self.mario = mario
        self.screens = screens
        self.enemies = enemies
        self.lifes = lifes

        # We set in memory the currently used objects in the level
        self.currlv, self.lvType = 0, "block"
        self.currplatforms = self.screens[self.currlv].platforms
        self.currenemies = self.enemies[self.currlv]
        self.currpipes = self.screens[self.currlv].pipes

        self.locationTopScore = f"{directory}/{topScore}"
        with open(self.locationTopScore, "r+") as file:
            self.score, self.topScore = 0, json.load(file)

        # We change the spawn of every enemy inside the pipes
        try:
            for i, a in enumerate(self.currenemies):
                # If the index is even, we spawn him in the left
                if i % 2 == 0:
                    a.posX = self.currpipes[0][0]
                    a.direction = 1

                # But if its odd, we put him in the right
                elif i % 2 != 0:
                    a.posX = self.currpipes[1][0]
                    a.direction = 0 - 1

                # And change the height for all of them
                a.posY = self.currpipes[0][1]

        # If there are not 2 pipes in the level, we put everyone to spawn at the only one
        except IndexError:
            for a in self.currenemies:
                a.posX = self.currpipes[0][0]
                a.posY = self.currpipes[0][1]

        # And initialize the first enemy
        self.activenemies = []
        self.activenemies.append(self.currenemies.pop())
        self.activenemies[0].isSpawning = True

        # Finally we run the program
        pyxel.run(self.update, self.draw)

    def update(self):
        try:
            if self.mario is not None:
                # First we check if we are still at the splash screen
                if not self.ingame:
                    if pyxel.btnp(pyxel.KEY_SPACE):
                        self.ingame = True
                        # This needed to be implemented to make the first check on the first enemy
                        self.enemiesCheck(self.activenemies[0])

                elif self.ingame:
                    # If there are no more enemies, we change the level to the next one
                    if len(self.currenemies) == 0 and len(self.activenemies) == 0:
                        self.changeLv()

                    # Function used to keep track of the time
                    self.parseTime()

                    # Call for the routine of mario
                    self.mario.checkIsOver(self.currplatforms)
                    self.mario.checkMovement(self.dimX, self.currplatforms, self.parsedtime)

                    # Call for the routine of the enemies
                    for a, i in enumerate(self.activenemies):
                        if self.enemiesCheck(i):
                            # Check if the enemy has been dead for 3 seconds then disappear
                            self.activenemies.pop(a)
                            self.score += 100

                    # Check state of each platform
                    for i in self.currplatforms:
                        if i.kickStatus:
                            # if aniKick returns false, there is no more animation
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

        except AttributeError:
            pass

    def draw(self):
        pyxel.cls(0)

        if self.ingame:
            self.lifes.draw()

            # Enemies animation
            for i in self.activenemies:
                if i == "Turtle":
                    pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3],
                              colkey=8)
                elif i == "Crab":
                    pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3],
                              colkey=11)
                elif i == "Fly":
                    pyxel.blt(i.posX, i.posY, 0, i.currframe[0], i.currframe[1], i.currframe[2], i.currframe[3],
                              colkey=0)

            if self.currlv <= 1:
                pyxel.bltm(0, 0, 0, 0, 0, 240, 200, colkey=8)
            elif self.currlv > 1:
                pyxel.bltm(0, 0, 1, 0, 0, 240, 200, colkey=8)

            pyxel.text(80, 4, str(self.score), 7)

            # This was created for the animation of the kick
            for i in self.currplatforms:
                if i.kickStatus:
                    pyxel.blt(i.kickX, i.kickY, 0, i.framesPlatform[i.currPhaseFrame][0],
                              i.framesPlatform[i.currPhaseFrame][1], i.framesPlatform[i.currPhaseFrame][2],
                              i.framesPlatform[i.currPhaseFrame][3], colkey=8)

            # Mario's animation
            try:
                pyxel.blt(self.mario.posX, self.mario.posY, 0, self.mario.currframe[0],
                          self.mario.currframe[1], self.mario.currframe[2], self.mario.currframe[3], colkey=0)

            except AttributeError:
                if self.currlv == 3:
                    pyxel.text(94, 50, "YOU WON :)", 9)

                elif self.mario is None:
                    pyxel.text(94, 50, "YOU DIED LOL", 9)

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
        self.parsedtime = search(r'(.*)\.\d{2}', str(time() - self.initime)).group(0)[:-1]
        print(float(self.parsedtime))
        if float(self.parsedtime):  # Is a check for the first frame
            if self.parsedtime != self.temptime:
                self.temptime = self.parsedtime
                if float(self.parsedtime) % 4 == 0 and len(self.currenemies) != 0:
                    self.activenemies.append(self.currenemies.pop())
                    self.activenemies[-1].isSpawning = True
                    self.activenemies[-1].timeSpawning = self.temptime

                for a in self.activenemies:
                    if a.isSpawning and (float(self.temptime) - float(a.timeSpawning)) >= 0.7:
                        a.isSpawning = False

    def enemiesCheck(self, i):
        if i.isDed:
            if (float(self.parsedtime) - float(i.timeDed)) > 3:
                return True

        elif not i.isDed:
            i.checkIsOver(self.currplatforms)

            if i != "Fly":
                i.movement(self.dimX)

            elif i == "Fly":
                # i.movement(self.dimX, self.currplatforms)
                i.movement(self.dimX)

            if self.mario is not None and self.mario.kickPos != [0, 0, None]:
                self.currplatforms[self.mario.kickPos[2]].kick(self.mario.kickPos,
                                                               self.lvType)

                if (self.mario.kickPos[1] - 13) <= i.posY <= (self.mario.kickPos[1] - 5):
                    if self.mario.kickPos[0] - 5 <= (i.posX + i.collideX // 2) <= \
                            (self.mario.kickPos[0] + 16):
                        i.kickFall("turn")

            if self.mario is not None and self.mario.checkEnemy(i.posX, i.posY, i.collideX, i.collideY):
                if not i.isFlipped and not self.mario.isDed:
                    self.lifes.count -= 1

                    if self.mario.dead(self.parsedtime, self.lifes.count):
                        self.mario = None

                        json_object = json.dumps({"topscore": self.topScore}, indent=4)
                        with open(self.locationTopScore, "r+") as file:
                            file.write(json_object)

                elif i.isFlipped:
                    i.kickFall("fall", self.parsedtime)

            return False

    def changeLv(self):
        self.currlv += 1

        if self.currlv != 4:
            self.currenemies = self.enemies[self.currlv]

            if self.currlv > 1:
                self.currpipes = self.screens[1].pipes
                self.currplatforms = self.screens[1].platforms
                self.lvType = "tiles"

            try:
                for i, a in enumerate(self.currenemies):
                    if i % 2 == 0:
                        a.posX = self.currpipes[0][0]
                        a.direction = 1
                    elif i % 2 != 0:
                        a.posX = self.currpipes[1][0]
                        a.direction = 0 - 1
                    a.posY = self.currpipes[0][1]
            except IndexError:
                for a in self.currenemies:
                    a.posX = self.currpipes[0][0]
                    a.posY = self.currpipes[0][1]

            """
            The idea was to add different levels with different layouts, but, due
            to lack of time we are obliged to reduce to two levels with various sets
            of enemies
            """

            sleep(2)

            self.activenemies = [self.currenemies[0]]
            self.activenemies[0].isSpawning = True

        elif self.currlv == 4:
            self.mario = None


screen1 = levels.Screen(1, [levels.Platform(2, 48, 68, 8),
                            levels.Platform(170, 48, 68, 8),
                            levels.Platform(50, 96, 140, 8),
                            levels.Platform(2, 144, 68, 8),
                            levels.Platform(170, 144, 68, 8),
                            levels.Platform(0, 192, 240, 8)],
                        [[10, 24], [220, 24], [0, 180], [240, 180]])

screen2 = levels.Screen(2, [levels.Platform(2, 48, 140, 8),
                            levels.Platform(178, 48, 60, 8),
                            levels.Platform(2, 96, 100, 8),
                            levels.Platform(138, 96, 100, 8),
                            levels.Platform(2, 144, 60, 8),
                            levels.Platform(98, 144, 140, 8),
                            levels.Platform(0, 192, 240, 8)],
                        [[10, 24], [220, 24], [0, 180], [240, 180]])

# enemies1 = [enemies.Fly("Fly", 16, 16)]
enemies1 = [enemies.Turtle("Turtle", 16, 16),
            enemies.Turtle("Turtle", 16, 16),
            enemies.Turtle("Turtle", 16, 16),
            enemies.Crab("Crab", 16, 16),
            enemies.Crab("Crab", 16, 16),
            enemies.Crab("Crab", 16, 16)]

# enemies2 = [enemies.Fly("Fly", 16, 16)]
enemies2 = [enemies.Turtle("Turtle", 16, 16, ),
            enemies.Turtle("Turtle", 16, 16, ),
            enemies.Turtle("Turtle", 16, 16, ),
            enemies.Crab("Crab", 16, 16, ),
            enemies.Crab("Crab", 16, 16, ),
            enemies.Crab("Crab", 16, 16, )]

enemies3 = [enemies.Turtle("Turtle", 16, 16),
            enemies.Turtle("Turtle", 16, 16),
            enemies.Turtle("Turtle", 16, 16),
            enemies.Crab("Crab", 16, 16),
            enemies.Crab("Crab", 16, 16),
            enemies.Crab("Crab", 16, 16)]

# enemies2 = [enemies.Fly("Fly", 16, 16)]
enemies4 = [enemies.Turtle("Turtle", 16, 16, ),
            enemies.Turtle("Turtle", 16, 16, ),
            enemies.Turtle("Turtle", 16, 16, ),
            enemies.Crab("Crab", 16, 16, ),
            enemies.Crab("Crab", 16, 16, ),
            enemies.Crab("Crab", 16, 16, )]

App(240, 200, player.Mario(16, 21), scoreboard.Lifes(10, 2), [screen1, screen2],
    [enemies1, enemies2, enemies3, enemies4], getcwd(), "topScore.json")
