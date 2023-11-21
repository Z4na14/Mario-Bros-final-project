class Mario:
    def __init__(self, collideX, collideY):
        """
        :param collideX:
        :param collideY:
        I would leave the colliders, but they are going to be fixed
        to Mario
        """
        self.collideX = collideX
        self.collideY = collideY
        self.posX = 50
        self.posY = 50
        self.velY = 0
        self.mX = 0
        self.isFalling = False
        self.isOver = False
        self.currPlat = None

    def movement(self, command):
        if command == 'up':
            if self.velY == -1 and self.isFalling == False:
                self.velY = 10

        elif command == 'left':
            if self.mX == 0:
                self.mX -= 2

        elif command == 'right':
            if self.mX == 0:
                self.mX += 2

