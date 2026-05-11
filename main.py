from lib.tiro import *
from lib.player import *
from lib.botao import *
from pplay.window import *
from pplay.keyboard import *
from pplay.mouse import *
from pplay.sprite import *
from time import sleep
from rich.traceback import install
install()


def space_invaders():

    # Janela
    x = 800
    y = 800
    janela = Window(x, y)
    janela.set_title("--- SPACE INVADERS ---")
    fundo = Sprite("sprites/menu/fundo.png", 1)

    # Menu
    jogar = Botao("sprites/menu/jogar.png", janela, 220, 246)
    dificuldade = Botao("sprites/menu/dificuldade.png", janela, 220, 358.5)
    rank = Botao("sprites/menu/rank.png", janela, 220, 474)
    sair = Botao("sprites/menu/sair.png", janela, 220, 597.5)

    # Dificuldade
    facil = Botao("sprites/modo/facil.png", janela, 325, 310)
    medio = Botao("sprites/modo/medio.png", janela, 325, 400)
    dificil = Botao("sprites/modo/dificil.png", janela, 325, 487)
    dif = 1

    # Player
    velocidade = 400
    player = Player("sprites/player/nave.png",
                    janela, 240, 650, velocidade/dif)

    # Tiro
    tiro = Tiro("sprites/player/tiro.png", janela, 240, 500, velocidade/dif)
    tiros = list()
    # Extras
    teclado = Keyboard()
    estado = "menu"

    while True:
        janela.set_background_color((0, 0, 0))
        fundo.draw()
        dt = janela.delta_time()

        # Menu
        if estado == "menu":
            jogar.draw()
            dificuldade.draw()
            rank.draw()
            sair.draw()
            if jogar.update(janela):
                estado = "jogo"
                player.sprite.x = 240
                player.sprite.y = 650
                tiros.clear()
                sleep(0.2)
            elif dificuldade.update(janela):
                sleep(0.2)
                estado = "dificuldade"
            elif dificuldade.update(janela):
                estado = "menu"
                sleep(0.2)
            elif sair.update(janela):
                estado = "sair"
                sleep(0.2)
        elif estado == "jogo":

            # Movimento do Player
            player.new_speed(velocidade/dif)
            player.recarga(dif)
            player.update(janela, teclado, dt)

            # Tiro
            if teclado.key_pressed("SPACE") and player.timer <= 0:
                tiros.append(
                    Tiro(
                        "sprites/player/tiro.png",
                        janela,
                        player.sprite.x + player.sprite.width // 2,
                        player.sprite.y,
                        velocidade * dif
                    )
                )
                player.timer = player.cooldown

            # Desenhando
            player.draw()
            for t in tiros:
                t.update(dt)
                t.draw()

            tiros = [t for t in tiros if not t.fora_da_tela()]
            if teclado.key_pressed("ESC"):
                estado = "menu"

        elif estado == "dificuldade":
            facil.draw()
            medio.draw()
            dificil.draw()

            if facil.update(janela):
                dif = 1
                sleep(0.2)
                estado = "menu"
            elif medio.update(janela):
                dif = 1.5
                sleep(0.2)
                estado = "menu"
            elif dificil.update(janela):
                dif = 2
                sleep(0.2)
                estado = "menu"

            if teclado.key_pressed("ESC"):
                estado = "menu"

        elif estado == "sair":
            break
        janela.update()


if __name__ == "__main__":
    space_invaders()
