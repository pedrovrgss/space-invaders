from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from invadersObjects import *
from PPlay.window import Window
from invadersClass import *
import time
import random

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
            return 3
        elif mouse.is_over_object(lista[0][3]) and mouse.is_button_pressed(1):
            exit()
        return 0
    
    elif screen == 1:
        game(lista, mouse, keyboard, window, 1)
        return 0
    
    elif screen == 2:
        refreshbuttons(lista[1], mouse.get_position())
        if mouse.is_over_object(lista[1][0]) and mouse.is_button_pressed(1):
            game(lista, mouse, keyboard, window, 1)
            return 0
        elif mouse.is_over_object(lista[1][1]) and mouse.is_button_pressed(1):
            game(lista, mouse, keyboard, window, 1.5)
            return 0
        elif mouse.is_over_object(lista[1][2]) and mouse.is_button_pressed(1):
            game(lista, mouse, keyboard, window, 2)
            return 0
        return 2
    
    elif screen == 3:
        with open("ranking.txt", "r") as f:
            ranking = f.readlines()

        # Filtra as linhas que têm pelo menos dois elementos após a divisão
        ranking = [linha.strip().split() for linha in ranking if len(linha.strip().split()) >= 2]

        # Ordena os jogadores por pontuação em ordem decrescente
        ranking = sorted(ranking, key=lambda x: int(x[1]), reverse=True)

        # Mantém apenas os top 5 jogadores
        top5 = ranking[:5]

        while True:
            window.background_color = (0, 0, 0)
            window.draw_text("Ranking", window.width/2 - 50, 50, size=30, color=(255, 255, 255))

            # Exibe os top 5 jogadores
            for i, jogador in enumerate(top5):
                nome, pontos = jogador  # Ajuste aqui, pois jogador é uma lista
                window.draw_text("{}. {} - {}".format(i+1, nome, pontos), window.width/2 - 50, 100 + i*30, size=30, color=(255, 255, 255))

            window.update()

            if keyboard.key_pressed("esc"):
                return 0
            if keyboard.key_pressed("enter"):
                return 0


    
def game(lista, mouse: Mouse, keyboard: Keyboard, window: Window, dificuldade):
    """
    Função que roda o jogo
    """
    ship = Ship("assets/SpaceShip.png")
    background = GameImage("assets/fundo.png")

    ship.set_position(window.width/2 - ship.width/2, window.height - ship.height - 20)
    blastlist = []
    space = [0,0]
    cooldown = 0.3 * dificuldade
    lastshot = 0
    invader = [[None]*5 for _ in range(3)]
    invaderblastlist = []
    last_invader_shot = 0

    if dificuldade == 1:
        invaderscooldown = 3.0
    elif dificuldade == 1.5:
        invaderscooldown = 2.0
    elif dificuldade == 2:
        invaderscooldown = 1.0

    
    for i in range(3):
        for j in range(5):
            if dificuldade == 1:
                invader[i][j] = Invaders("assets/Invader.png", 200, 1, True)
                invader[i][j].set_position(100 + j*100, 100 + i*100)
            elif dificuldade == 1.5:
                invader[i][j] = Invaders("assets/Invader.png", 250, 1, True)
                invader[i][j].set_position(100 + j*100, 100 + i*100)
            elif dificuldade == 2:
                invader[i][j] = Invaders("assets/Invader.png", 300, 1, True)
                invader[i][j].set_position(100 + j*100, 100 + i*100)

    direction = 1  # 1 para a direita, -1 para a esquerda
    move_down_distance = 10

    if dificuldade == 1:
        lifes = 3
    elif dificuldade == 1.5:
        lifes = 2
    elif dificuldade == 2:
        lifes = 1

    score = 0   

    total_time = 0
    frames_in_second = 0
    fps = 0
    frames = 0

    nome_player = ""


    while (not keyboard.key_pressed("esc")):
        deltatime = window.delta_time()
        background.draw()
        space[0] = space[1]
        space[1] = keyboard.key_pressed("space")
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
                if invader[i][j].alive:
                    invader[i][j].draw()
                    if invader[i][j].collidedblast(blastlist):
                        invader[i][j].alive = False
                        score += 1* int(dificuldade*10)
                        blast_to_remove = None
                        for blast in blastlist:
                            if invader[i][j].collided(blast):
                                blast_to_remove = blast
                                break
                        if blast_to_remove:
                            blastlist.remove(blast_to_remove)

        # Movimentação lateral dos invaders
        for i in range(len(invader)):
            for j in range(len(invader[i])):
                if invader[i][j].alive:
                    invader[i][j].x += direction * invader[i][j].speed * deltatime
                    invader[i][j].draw()
        # Verifica se algum invader atingiu a parede
        for i in range(len(invader)):
            for j in range(len(invader[i])):
                if invader[i][j].alive:
                    if invader[i][j].x <= 10 or invader[i][j].x + invader[i][j].width >= window.width - 10:
                        for i in range(len(invader)):
                            for j in range(len(invader[i])):
                                if invader[i][j].alive:
                                    invader[i][j].x -= 10 * direction
                                    invader[i][j].y += move_down_distance
                        direction *= -1  # Inverte a direção ao atingir a parede
                        break

        current_time = time.time()
        if current_time - last_invader_shot >= invaderscooldown:
            randomi = random.randint(0, len(invader) - 1)
            randomj = random.randint(0, len(invader[randomi]) - 1)
            if invader[randomi][randomj].alive:
                new_invaderblast = Blast(invader[randomi][randomj].x + invader[randomi][randomj].width/2, invader[randomi][randomj].y + invader[randomi][randomj].height, "assets/InvaderBlast.png")
                invaderblastlist.append(new_invaderblast)
                last_invader_shot = current_time

        for blast in invaderblastlist:
            blast.y += (150 * deltatime)
            blast.draw()
            if blast.y > window.height:
                invaderblastlist.remove(blast)
            if blast.collided(ship):
                lifes -= 1
                invaderblastlist.remove(blast)



        # Verifica se algum invader chegou na altura da nave
        for i in range(len(invader)):
            for j in range(len(invader[i])):
                if invader[i][j].alive:
                    if invader[i][j].y + invader[i][j].height >= window.height - ship.height - 20:
                        lifes = 0
                        break

        
        current_time = time.time()
        total_time += deltatime
        frames_in_second += 1

        if total_time >= 1:
            fps = frames_in_second
            total_time = 0
            frames_in_second = 0


# Remover listas vazias após a remoção dos invasores mortos

        ship.draw()

        window.draw_text(str(fps), 0, 0, size=30, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)

        window.draw_text("Pontuação: {}".format(score), window.width - 150, 10, size=20, color=(255, 255, 255))
        window.draw_text("Vidas: {}".format(lifes), window.width - 150, 30, size=20, color=(255, 255, 255))
        # Atualização da tela
        window.update()
        frames += 1

        # Após o loop de verificação de colisões com os tiros
        invaders_vivos = any(invader[i][j].alive for i in range(len(invader)) for j in range(len(invader[i])))

        if not invaders_vivos:
            for i in range(3):
                for j in range(5):
                    if dificuldade == 1:
                        invader[i][j].alive = True
                        invader[i][j].speed += 35
                        invader[i][j].set_position(100 + j * 100, 100 + i * 100)
                    elif dificuldade == 1.5:
                        invader[i][j].alive = True
                        invader[i][j].speed += 35
                        invader[i][j].set_position(100 + j * 100, 100 + i * 100)
                    elif dificuldade == 2:
                        invader[i][j].alive = True
                        invader[i][j].speed += 35
                        invader[i][j].set_position(100 + j * 100, 100 + i * 100)
        
        
        if lifes <= 0:
            while True:
                
                background.draw()
                window.draw_text("Você perdeu! Digite seu nome no terminal.", window.width/2 - 300, window.height/2, size=30, color=(255, 255, 255))
                window.update()
                if nome_player == "":
                    nome_player = input("Digite seu nome: ")
                    with open ("ranking.txt", "a") as f:
                        f.write("{} {}\n".format(nome_player, score))
                else:
                    break
            break
        
            
            

    
