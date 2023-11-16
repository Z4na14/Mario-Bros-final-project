import pyxel


class App:
    def __init__(self, dimx, dimy, marioClass):
        self.mario = marioClass

        pyxel.init(dimx, dimy)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.mario.mY < 0:
            if pyxel.btnp(pyxel.KEY_A):
                self.mario.movement('left')

            elif pyxel.btnp(pyxel.KEY_D):
                self.mario.movement('right')

            self.mario.posY -= 3
            self.mario.mY += 3

            if self.mario.mY == 0:
                self.mario.mY = 12

        elif self.mario.mY > 0:
            self.mario.posY += 3
            self.mario.mY -= 3

        if pyxel.btnp(pyxel.KEY_W):
            self.mario.movement("up")

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.mario.posX, self.mario.posY, 5, 10, 11)


class Mario:
    def __init__(self, collideX, collideY):
        self.collideX = collideX
        self.collideY = collideY
        self.posX = 100
        self.posY = 100
        self.mY = 0

    def movement(self, command):
        if command == 'up':
            self.mY = -12

        elif command == 'left':
            self.posX -= 2

        elif command == 'right':
            self.posX += 2


App(160, 120, Mario(10, 10))
