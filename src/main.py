import pyxel


class App:
    def __init__(self, dimx, dimy, marioClass):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param marioClass: Class of the main character
        """
        self.mario = marioClass
        pyxel.init(dimx, dimy)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Check if the position of the character must be higher
        if self.mario.mY < 0:
            self.mario.posY -= 3
            self.mario.mY += 3

            if self.mario.mX != 0:
                self.mario.posX += self.mario.mX
                self.mario.mX = 0

            if self.mario.mY == 0:
                self.mario.mY = 12

        elif self.mario.mY > 0:
            self.mario.posY += 3
            self.mario.mY -= 3

        if self.mario.mX != 0:
            self.mario.posX += self.mario.mX
            self.mario.mX = 0

        if pyxel.btn(pyxel.KEY_W):
            self.mario.movement("up")

        elif pyxel.btn(pyxel.KEY_A):
            self.mario.movement('left')

        elif pyxel.btn(pyxel.KEY_D):
            self.mario.movement('right')

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.mario.posX, self.mario.posY, 5, 10, 11)


class Mario:
    def __init__(self, collideX, collideY):
        """
        :param collideX:
        :param collideY:
        I would leave the colliders, but they are going to be fixed
        to Mario
        TO DO: remove colliders and make them a constant and place
        class in another file.
        """
        self.collideX = collideX
        self.collideY = collideY
        self.posX = 100
        self.posY = 100
        self.mY = 0
        self.mX = 0

    def movement(self, command):
        if command == 'up':
            if self.mY == 0:
                self.mY = -12

        elif command == 'left':
            if self.mX == 0:
                self.mX -= 2

        elif command == 'right':
            if self.mX == 0:
                self.mX += 2


App(160, 120, Mario(10, 10))