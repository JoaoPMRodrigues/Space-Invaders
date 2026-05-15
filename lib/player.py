from lib.entidade import *


class Player(Entidade):
    def __init__(self, caminho, janela, x, y, velocidade):

        super().__init__(caminho, janela, x, y)

        self.velocidade = velocidade

        self.base = 0.3
        self.cooldown = self.base

        self.timer = 0

    def new_speed(self, velocidade):
        self.velocidade = velocidade

    def recarga(self, dificuldade):
        self.cooldown = self.base * dificuldade

    def update(self, janela, teclado, dt):

        if self.timer > 0:
            self.timer -= dt

        if teclado.key_pressed("LEFT"):
            self.sprite.x -= self.velocidade * dt

        if teclado.key_pressed("RIGHT"):
            self.sprite.x += self.velocidade * dt

        # Colisão com parede
        if self.sprite.x < 0:
            self.sprite.x = 0

        if self.sprite.x + self.sprite.width > janela.width:
            self.sprite.x = (
                janela.width - self.sprite.width
            )
