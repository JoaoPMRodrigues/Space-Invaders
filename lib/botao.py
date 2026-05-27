from pplay.sprite import *
from lib.entidade import *


class Botao(Entidade):
    was_pressed = False

    def __init__(self, imagem, window, x, y):
        super().__init__(imagem, window, x, y)

    def clicked(self, window):
        mouse = window.mouse
        hovering = mouse.is_over_object(self.sprite)
        pressed = mouse.button_pressed(1)

        if hovering and pressed and not Botao.was_pressed:
            Botao.was_pressed = True
            return True

        if not pressed:
            Botao.was_pressed = False

        return False

    def update(self, window):
        return self.clicked(window)
