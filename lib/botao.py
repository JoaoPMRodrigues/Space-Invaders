from pplay.sprite import *
from pplay.mouse import *


class Botao:
    def __init__(self, caminho, janela, distancia):
        self.sprite = Sprite(caminho)
        self.sprite.x = janela.width // 2 - self.sprite.width // 2
        self.sprite.y = janela.height // 2 + (distancia*self.sprite.height)

    def draw(self):
        self.sprite.draw()

    def clicado(self, janela):
        mouse = janela.mouse
        return mouse.is_over_object(self.sprite) and mouse.button_pressed(1)

    def update(self, janela):
        if self.clicado(janela):
            return True
        return False
