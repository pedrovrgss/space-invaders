from PPlay.sprite import *
from PPlay.gameimage import *

class Invaders(Sprite):
    def __init__(self, image_file = "assets/Invader", frames = 1, alive = True):
        super().__init__(image_file, frames)
        self.image_file = image_file
        self.frames = frames
        self.alive = alive

    def collidedblast(self, blastlist):
        for blast in blastlist:
            if self.collided(blast):
                    return True
        return False

