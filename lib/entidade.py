from pplay.sprite import *


class Entidade:
    def __init__(self, caminho, janela, x=None, y=None):
        self.sprite = Sprite(caminho)
        self.sprite.x = x
        self.sprite.y = y
        if x == None:
            self.sprite.x = janela.width/2+self.sprite.width/2
        if y == None:
            self.sprite.y = janela.height/2+self.sprite.height/2

    def draw(self):
        self.sprite.draw()
