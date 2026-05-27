from pplay.sprite import *
from lib.entidade import *


class Tiro(Entidade):
    def __init__(self, caminho, janela, x, y, velocidade):

        super().__init__(caminho, janela, x, y)

        self.velocidade = velocidade

    def update(self, dt):
        self.sprite.y -= self.velocidade * dt

    def fora_da_tela(self):
        return self.sprite.y < 0


class TiroInimigo(Tiro):

    def update(self, dt):
        self.sprite.y += self.velocidade * dt

    def fora_da_tela(self):
        return self.sprite.y > 1100
