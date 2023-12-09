import pyxel


class Lifes:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

        self.count = 3

    def draw(self):
        for i in range(self.count):
            pyxel.blt(self.posX + (i*16), self.posY, 0, 208, 0, 11, 10)
