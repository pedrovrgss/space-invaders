from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite
import pygame

pygame.init()

class Button(GameImage):
    
    def __init__(self, image_file1, image_file2):
        super().__init__(image_file1)
        self.img1 = image_file1
        self.img2 = image_file2
        self.bool = False
    
    def atualiza(self, coord):
        """
        Metodo para trocar botões quando o mouse esta por cima
        """
        if self.bool == False and coord[0] > self.x and coord[1] > self.y and coord[0] < (self.x + self.width) and coord[1] < (self.y + self.height):
            self.image = pygame.image.load(self.img2)
            self.bool = True
        if self.bool == True and (coord[0] < self.x or coord[1] < self.y or coord[0] > (self.x + self.width) or coord[1] > (self.y + self.height)):
            self.image = pygame.image.load(self.img1)
            self.bool = False
        self.draw()

class Ship(Sprite):
    def __init__(self, image_file, frames=1):
        self.speed = 150
        super().__init__(image_file, frames)


class Blast(GameImage):

    def __init__(self, x, y):
        super().__init__("assets/Tiro.png")
        self.speed = 150
        self.x = x
        self.y = y
    
    def foward(self, time):
        self.y -= time * self.speed