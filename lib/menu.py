from pplay.sprite import *
from pplay.mouse import *


class Botao:
    def __init__(self, imagem, x, y):
        self.sprite = Sprite(imagem)
        self.sprite.x = x
        self.sprite.y = y

    def draw(self):
        self.sprite.draw()

    def clicado(self, mouse):
        return mouse.is_over_object(self.sprite) and mouse.button_pressed(1)


def criar_botao(caminho, janela, distancia):
    botao = Sprite(caminho)
    botao.x = janela.width // 2 - botao.width // 2
    botao.y = janela.height // 2 + (distancia*botao.height)
    return botao


def verificar_clique(janela, jogar, dificuldade, rank, sair, estado):
    if janela.mouse.is_over_object(jogar):
        if janela.mouse.button_down(1):
            estado = "jogo"
    elif janela.mouse.is_over_object(dificuldade):
        if janela.mouse.button_down(1):
            estado = "dificuldade"
    elif janela.mouse.is_over_object(rank):
        if janela.mouse.button_down(1):
            estado = "menu"
    elif janela.mouse.is_over_object(sair):
        if janela.mouse.button_down(1):
            estado = "sair"

    return estado
