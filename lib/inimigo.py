from lib.entidade import *
from random import randint


class Inimigo(Entidade):
    def __init__(self, caminho, janela, x, y):

        super().__init__(caminho, janela, x, y)


class Enxame:
    def __init__(self, caminho, janela, linhas=3, colunas=5, velocidade=30):

        self.janela = janela
        self.linhas = linhas
        self.colunas = colunas

        self.velocidade = velocidade/2
        self.direcao = 1
        fim = (linhas-1) * (colunas-1)
        self.boss = randint(0, fim)
        self.inimigos = []

        base = Sprite(caminho)
        largura = base.width
        altura = base.height

        self.espacamento_x = largura // 4
        self.espacamento_y = altura // 4

        offset_x = 20
        offset_y = 20
        c = 0
        for linha in range(self.linhas):
            for coluna in range(self.colunas):

                x = (offset_x + coluna * (largura + self.espacamento_x))
                y = (offset_y + linha * (altura + self.espacamento_y))

                if c != self.boss:
                    inimigo = Inimigo(caminho, janela, x, y)
                else:
                    inimigo = Inimigo("sprites/player/boss.png", janela, x, y)
                self.inimigos.append(inimigo)

                c += 1

    def update(self, dt):

        self.movimentar(dt)

    def draw(self):

        for inimigo in self.inimigos:
            inimigo.draw()

    def movimentar(self, dt):

        inverter = False

        for inimigo in self.inimigos:

            if inimigo.sprite.x <= 0:
                inverter = True
                break

            if (
                inimigo.sprite.x
                + inimigo.sprite.width
                >= self.janela.width
            ):
                inverter = True
                break

        if inverter:

            self.direcao *= -1

            for inimigo in self.inimigos:
                inimigo.sprite.y += 30
                inimigo.sprite.x += self.direcao * self.velocidade * dt

        for inimigo in self.inimigos:

            inimigo.sprite.x += (
                self.velocidade
                * self.direcao
                * dt
            )

    def chegou_no_player(self, player):

        for inimigo in self.inimigos:

            colisao_vertical = (
                inimigo.sprite.y + inimigo.sprite.height
                >= player.sprite.y
            )

            if colisao_vertical:
                return True

        return False

    def atualizar_limites(self):

        self.menor_x = min(
            inimigo.sprite.x
            for inimigo in self.inimigos
        )

        self.maior_x = max(
            inimigo.sprite.x + inimigo.sprite.width
            for inimigo in self.inimigos
        )

        self.menor_y = min(
            inimigo.sprite.y
            for inimigo in self.inimigos
        )

        self.maior_y = max(
            inimigo.sprite.y + inimigo.sprite.height
            for inimigo in self.inimigos
        )

    def escolhe_boss(self):

        if len(self.inimigos) == 0:
            self.boss = -1
            return

        self.boss = randint(0, len(self.inimigos) - 1)

        for i in range(len(self.inimigos)):
            if i == self.boss:
                x = self.inimigos[i].sprite.x
                y = self.inimigos[i].sprite.y

                self.inimigos[i].sprite = Sprite("sprites/player/boss.png")

                self.inimigos[i].sprite.x = x
                self.inimigos[i].sprite.y = y

    def matar_boss(self, inimigo):

        indice = self.inimigos.index(inimigo)
        cima = indice-7
        esquerda = indice - 1
        direita = indice + 1

        remover = [indice]
        if cima > 0:
            remover.append(cima)
        if esquerda >= 0:
            remover.append(esquerda)

        if direita < len(self.inimigos):
            remover.append(direita)

        remover.sort(reverse=True)

        for i in remover:
            self.inimigos.pop(i)

        self.escolhe_boss()

        return True
