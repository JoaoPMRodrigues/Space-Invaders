from pplay.sprite import *
from pplay.mouse import *
from lib.entidade import *


class Botao(Entidade):
    def __init__(self, imagem, janela, x, y):
        super().__init__(imagem, janela, x, y)

    def clicado(self, janela):
        mouse = janela.mouse
        return mouse.is_over_object(self.sprite) and mouse.button_pressed(1)

    def update(self, janela):
        if self.clicado(janela):
            return True
        return False
