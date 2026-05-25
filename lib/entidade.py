from pplay.sprite import *
from abc import ABC


class Entidade(ABC):
    def __init__(self, caminho, janela, x=0, y=0):

        self.sprite = Sprite(caminho)

        self.sprite.x = x
        self.sprite.y = y

    def update(self, dt):
        pass

    def draw(self):
        self.sprite.draw()
