from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from invadersObjects import *
from PPlay.window import Window
from invadersClass import *
import time

def refreshbuttons(lista, coord):
    """
    Função para desenhar e alterar a imagem dos botões quando o mouse estiver em cima
    """
    for i in lista:
        i.atualiza(coord)
        i.draw()

def settela(screen, lista, mouse: Mouse, keyboard: Keyboard, window):
    """
    Função que gerencia qual as telas do jogo
    """
    if screen == 0:
        refreshbuttons(lista[0], mouse.get_position())
        if mouse.is_over_object(lista[0][0]) and mouse.is_button_pressed(1):
            return 1
        elif mouse.is_over_object(lista[0][1]) and mouse.is_button_pressed(1):
            return 2
        elif mouse.is_over_object(lista[0][2]) and mouse.is_button_pressed(1):
            return 0
        elif mouse.is_over_object(lista[0][3]) and mouse.is_button_pressed(1):
            exit()
        return 0
    
    elif screen == 1:
        game(lista, mouse, keyboard, window)
        return 0
    
    elif screen == 2:
        refreshbuttons(lista[1], mouse.get_position())
        if mouse.is_over_object(lista[1][0]) and mouse.is_button_pressed(1):
            return 0
        elif mouse.is_over_object(lista[1][1]) and mouse.is_button_pressed(1):
            return 0
        elif mouse.is_over_object(lista[1][2]) and mouse.is_button_pressed(1):
            return 0
        return 2
    
def game(lista, mouse: Mouse, keyboard: Keyboard, window: Window):
    """
    Função que roda o jogo
    """
    ship = Ship("assets/SpaceShip.png")
    background = GameImage("assets/fundo.png")
    ship.set_position(window.width/2 - ship.width/2, window.height - ship.height - 20)
    blastlist = []
    space = [0,0]
    cooldown = 0.3
    lastshot = 0
    invader = [[None]*5 for _ in range(3)]
    for i in range(3):
        for j in range(5):
            invader[i][j] = Invaders("assets/Invader.png")
            invader[i][j].set_position(100 + j*100, 100 + i*100)

    while not keyboard.key_pressed("esc"):
        start_time = time.time()
        deltatime = window.delta_time()
        background.draw()
        space[0] = space[1]
        space[1] = keyboard.key_pressed("space")
        if(keyboard.key_pressed("down") and ship.y < window.height - ship.height - 10):
            ship.move_y(ship.speed*deltatime)
        if(keyboard.key_pressed("up") and ship.y > 10):
            ship.move_y(-ship.speed*deltatime)
        if(keyboard.key_pressed("left") and ship.x > 10):
            ship.move_x(-ship.speed*deltatime)
        if(keyboard.key_pressed("right") and ship.x < window.width - ship.width - 10):
            ship.move_x(ship.speed*deltatime)
        if(space == [0,1]):
            time_now = time.time()
            if time_now - lastshot >= cooldown:
                blastlist.append(Blast(ship.x, ship.y))
                lastshot = time_now
        for blast in blastlist:
            blast.foward(deltatime)
            blast.draw()
            if blast.y < -20:
                del blastlist[0]

        for i in range(len(invader)):
            for j in range(len(invader[i])):
                if invader[i][j].alive == True:
                    invader[i][j].draw()
                    if invader[i][j].collidedblast(blastlist):
                        invader[i][j].alive = False
                        blastlist.remove(blast)
                else:
                    del invader[i][j]

# Remover listas vazias após a remoção dos invasores mortos
        invader = [row for row in invader if row]

        ship.draw()

        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time > 0:
            fps = int(1 / elapsed_time)
        else:
            fps = 0

        window.draw_text(str(fps), 0, 0, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)

        # Atualização da tela
        window.update()
