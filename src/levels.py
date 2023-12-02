import pyxel


class Platform:
    def __init__(self, positionX, positionY, width, height):
        self.positionX = positionX
        self.positionY = positionY
        self.width = width
        self.height = height

        self.aniBlock = [[0, 245, 23, 15], [24, 243, 23, 17], [48, 241, 23, 19]]
        self.aniPipeYellow = []
        self.aniPipeGreen = []
        self.aniTiles = []
        self.aniFrozen = []

        self.kickStatus = False
        self.kickX = 0
        self.kickY = 0
        self.currPhaseFrame = 0
        self.recover = False
        self.f
        ramesPlatform = None

    def kick(self, posX, posY, block: str):
        if not self.kickStatus:
            self.kickX = posX
            self.kickY = posY
            match block:
                case "block":
                    self.framesPlatform = self.aniBlock

                case "pipeyellow":
                    self.framesPlatform = self.aniPipeYellow

                case "pipegreen":
                    self.framesPlatform = self.aniPipeGreen

                case "tiles":
                    self.framesPlatform = self.aniTiles

                case "frozen":
                    self.framesPlatform = self.aniFrozen

            self.currPhaseFrame = 0
            self.kickStatus = True

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
