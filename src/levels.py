import pyxel
from copy import deepcopy


class Platform:
    def __init__(self, positionX, positionY, width, height):
        self.positionX = positionX
        self.positionY = positionY
        self.width = width
        self.height = height

        self.aniBlock = [[0, 245, 23, 12], [24, 243, 23, 14], [48, 241, 23, 16]]
        self.aniPipeYellow = [[72, 245, 23, 12], [96, 243, 23, 14], [120, 241, 23, 16]]
        self.aniPipeGreen = [[144, 245, 23, 12], [168, 243, 23, 14], [192, 241, 23, 16]]
        self.aniTiles = [[32, 230, 23, 12], [56, 227, 23, 14], [80, 225, 23, 16]]

        self.kickX = 0
        self.kickY = 0
        self.currPhaseFrame = 0
        self.numPlat = 0

        self.kickStatus = False
        self.recover = False
        self.framesPlatform = None

    def kick(self, kickPos, block: str):
        if not self.kickStatus:
            self.kickX = kickPos[0]
            self.kickY = kickPos[1]
            self.numPlat = kickPos[2]

            match block:
                case "block":
                    self.framesPlatform = deepcopy(self.aniBlock)

                case "tiles":
                    self.framesPlatform = deepcopy(self.aniTiles)

            if self.kickX > (self.positionX + (self.width // 2)):
                if (self.kickX + 20) > (self.positionX + self.width):
                    for i in self.framesPlatform:
                        i[2] -= ((self.kickX + 22) - (self.positionX + self.width))

            elif self.kickX < (self.positionX + (self.width // 2)):
                if (self.kickX - 10) < self.positionX:
                    offset = self.positionX - self.kickX
                    for i in self.framesPlatform:
                        i[0] += offset
                        i[2] -= offset
                    self.kickX -= offset


            """
            From the left it bugs out lol
            """

            self.kickStatus = True
            self.currPhaseFrame = 0
            return [self.kickX, self.kickY, self.numPlat]

    def aniKick(self):
        if not self.recover:
            if self.currPhaseFrame == 2:
                self.recover = True

            elif self.currPhaseFrame != 2:
                if pyxel.frame_count % 2 == 0:
                    self.currPhaseFrame += 1
                    self.kickY -= 2

        elif self.recover:
            if self.currPhaseFrame == 0:
                self.recover = False
                self.kickStatus = False
                self.currPhaseFrame = -1
                return True

            elif self.currPhaseFrame != 0:
                if pyxel.frame_count % 2 == 0:
                    self.currPhaseFrame -= 1
                    self.kickY += 2


class Screen:
    def __init__(self, lv: int, platforms: list, pipes: list):
        self.lv = lv
        self.platforms = platforms
        self.pipes = pipes
