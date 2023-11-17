class Platform:
    def __init__(self, positionX, positionY, width, height):
        self.positionX = positionX
        self.positionY = positionY
        self.width = width
        self.height = height
"""
    def kick(self):
"""

class Screen:
    def __init__(self, lv: int, platforms : list, pipes : list):
        self.lv = lv
        self.platforms = platforms
        self.pipes = pipes