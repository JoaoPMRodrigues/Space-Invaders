from pplay.keyboard import *
from pplay.mouse import *
from pplay.sprite import *
from pplay.keyboard import *
from lib.menu import *
from rich.traceback import install
install()


def space_invaders():

    x = 600
    y = 800
    janela = Window(x, y)

    distancia = -2
    jogar = criar_botao("sprites/menu/jogar.png", janela, distancia)

    distancia = -0.5
    dificuldade = criar_botao(
        "sprites/menu/dificuldade.png", janela, distancia)

    distancia = 1
    rank = criar_botao("sprites/menu/rank.png", janela, distancia)

    distancia = 2.5
    sair = criar_botao("sprites/menu/sair.png", janela, distancia)

    distancia = -1
    facil = criar_botao("sprites/modo/facil.png", janela, distancia)

    distancia = 0
    medio = criar_botao("sprites/modo/medio.png", janela, distancia)

    distancia = 1
    dificil = criar_botao("sprites/modo/dificil.png", janela, distancia)

    teclado = Keyboard()

    estado = "menu"
    while True:
        if estado == "menu":
            janela.set_background_color((0, 0, 0))
            if estado == "menu":
                jogar.draw()
                dificuldade.draw()
                rank.draw()
                sair.draw()

            estado = verificar_clique(
                janela, jogar, dificuldade, rank, sair, estado)

        if estado == "jogo":
            if teclado.key_pressed("ESC"):
                estado = "menu"

        if estado == "dificuldade":
            facil.draw()
            medio.draw()
            dificil.draw()

            if teclado.key_pressed("ESC"):
                estado = "menu"

        if estado == "sair":
            break
        janela.update()


if __name__ == "__main__":
    space_invaders()
