from lib.entidade import *
from pplay import *


class Player(Entidade):
    def __init__(self, caminho, janela, x, y, velocidade):

        super().__init__(caminho, janela, x, y)
        self.janela = Window(caminho)
        self.velocidade = velocidade
        self.base = 0.3
        self.cooldown = self.base

        self.timer = 0

        self.vidas = 3
        self.invencivel = False
        self.timer_invencivel = 0

    def new_speed(self, velocidade):
        self.velocidade = velocidade

    def recarga(self, dificuldade):
        self.cooldown = self.base * dificuldade

    def update(self, janela, teclado, dt):

        if self.timer > 0:
            self.timer -= dt

        if teclado.key_pressed("LEFT") or teclado.key_pressed("A"):
            self.sprite.x -= self.velocidade * dt

        if teclado.key_pressed("RIGHT") or teclado.key_pressed("D"):
            self.sprite.x += self.velocidade * dt

        if self.sprite.x < 0:
            self.sprite.x = 0

        if self.sprite.x + self.sprite.width > janela.width:
            self.sprite.x = (
                janela.width - self.sprite.width
            )
        if self.invencivel:

            self.timer_invencivel -= dt

        if self.timer_invencivel <= 0:

            self.invencivel = False

    def respawn(self):

        self.sprite.x = (
            self.janela.width // 2
            - self.sprite.width // 2
        )

        self.sprite.y = 650

        self.invencivel = True
        self.timer_invencivel = 2

    def draw(self):
        if self.invencivel:
            if int(self.timer_invencivel * 10) % 2 == 0:
                return

        self.sprite.draw()
