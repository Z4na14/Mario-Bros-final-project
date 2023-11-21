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
        self.posX = 50
        self.posY = 50
        self.mY = 0
        self.mX = 0
        self.isFalling = False

    def movement(self, command):
        if command == 'up':
            if self.mY == 0 and self.isFalling == False:
                self.mY = -30

        elif command == 'left':
            if self.mX == 0:
                self.mX -= 2

        elif command == 'right':
            if self.mX == 0:
                self.mX += 2

