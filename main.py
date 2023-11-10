from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from invadersObjects import *
from gameFunctions import settela
import time


        
#definindo tela, definindo tela inicial como tela de menu e definindo background
j1 = Window(1000,600)
screen = 0
background = GameImage("assets/fundo.png")


#definindo botões da tela de menu ou tela 1
d = Button("assets/Dificuldade.png", "assets/DificuldadePressed.png")
d.set_position(j1.width/2 - d.width/2, 25 + j1.height*0.25)
j = Button("assets/Jogar.png", "assets/JogarPressed.png")
j.set_position(j1.width/2 - j.width/2, 25)
r = Button("assets/Ranking.png", "assets/RankingPressed.png")
r.set_position(j1.width/2 - r.width/2, 25 + j1.height*0.5)
s = Button("assets/Sair.png", "assets/SairPressed.png")
s.set_position(j1.width/2 - s.width/2, 25 + j1.height*0.75)

#definindo botões da tela de dificuldade ou tela 2
facil = Button("assets/Facil.png", "assets/FacilPressed.png")
medio = Button("assets/Medio.png", "assets/MedioPressed.png")
dificil = Button("assets/Dificil.png", "assets/DificilPressed.png")
facil.set_position(j1.width/8 , 0.6*j1.height)
medio.set_position(j1.width/2 - medio.width/2, 0.6*j1.height)
dificil.set_position(7*j1.width/8 - dificil.width, 0.6*j1.height)

#definindo mouse, teclado e lista de botões 
mouse = Mouse()
keyboard = Keyboard()
buttonlist = [[j,d,r,s],[facil,medio,dificil]]


import time

# ...

while True:  # game loop
    start_time = time.time()

    background.draw()
    screen = settela(screen, buttonlist, mouse, keyboard, j1)
    j1.update()

    # Outras lógicas do jogo e desenho

    end_time = time.time()
    elapsed_time = end_time - start_time
    fps = int(1 / elapsed_time)

    j1.draw_text(str(fps), 0, 0, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)

    # Atualização da tela
    j1.update()

    # Limite de frames por segundo
    j1.delay(16)  # Isso equivale a aproximadamente 60 FPS
