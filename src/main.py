import pyxel
import levels
import characters


class App:
    def __init__(self, dimx, dimy, mario):
        """
        :param dimx: Dimensions of the window (x)
        :param dimy: Dimensions of the window (y)
        :param marioClass: Class of the main character
        TO DO: Add collider check creating simple blocks (Use another
        class for every object)
        """

        self.dimX = dimx
        self.dimY = dimy

        self.mario = mario

        pyxel.init(dimx, dimy)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Quit game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Check if the position of the character must be higher
        if self.mario.mY < 0:
            self.mario.posY -= 4
            self.mario.mY += 4

            # Mario falls after reaching peak
            if self.mario.mY == 0:
                self.mario.mY = 24

        elif self.mario.mY > 0:
            self.mario.posY += 4
            self.mario.mY -= 4

        # Check for horizontal movement
        if self.mario.mX != 0:
            self.mario.posX += self.mario.mX
            self.mario.mX = 0

            if self.mario.posX < -10:
                self.mario.posX = self.dimX + 5

            elif self.mario.posX > self.dimX + 10:
                self.mario.posX = -5

        # Exec the functions for the movement
        if pyxel.btnp(pyxel.KEY_W):
            self.mario.movement("up")

        elif pyxel.btn(pyxel.KEY_A):
            self.mario.movement('left')

        elif pyxel.btn(pyxel.KEY_D):
            self.mario.movement('right')

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.mario.posX, self.mario.posY, 5, 10, 11)


App(160, 120, characters.Mario(10, 10))
