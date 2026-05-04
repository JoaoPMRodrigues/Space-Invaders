from pplay.keyboard import *
from pplay.mouse import *
from pplay.sprite import *
from pplay.keyboard import *
from lib.botao import *
from rich.traceback import install
install()


def space_invaders():

    x = 600
    y = 800
    janela = Window(x, y)

    # Menu
    jogar = Botao("sprites/menu/jogar.png", janela, -2)
    dificuldade = Botao("sprites/menu/dificuldade.png", janela, -0.5)
    rank = Botao("sprites/menu/rank.png", janela, 1)
    sair = Botao("sprites/menu/sair.png", janela, 2.5)

    # Dificuldade
    facil = Botao("sprites/modo/facil.png", janela, -1.5)
    medio = Botao("sprites/modo/medio.png", janela, 0)
    dificil = Botao("sprites/modo/dificil.png", janela, 1.5)

    teclado = Keyboard()
    estado = "menu"

    while True:
        janela.set_background_color((0, 0, 0))

        # Menu
        if estado == "menu":
            if estado == "menu":
                jogar.draw()
                dificuldade.draw()
                rank.draw()
                sair.draw()
            if jogar.update(janela):
                estado = "jogo"
            elif dificuldade.update(janela):
                estado = "dificuldade"
            elif dificuldade.update(janela):
                estado = "menu"
            elif sair.update(janela):
                estado = "sair"

        elif estado == "jogo":
            if teclado.key_pressed("ESC"):
                estado = "menu"

        elif estado == "dificuldade":
            facil.draw()
            medio.draw()
            dificil.draw()

            if teclado.key_pressed("ESC"):
                estado = "menu"

        elif estado == "sair":
            break
        janela.update()


if __name__ == "__main__":
    space_invaders()
