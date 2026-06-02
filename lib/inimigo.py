from lib.entidade import *


class Inimigo(Entidade):
    def __init__(self, caminho, janela, x, y):

        super().__init__(caminho, janela, x, y)


class Enxame:
    def __init__(
        self,
        caminho,
        janela,
        linhas=3,
        colunas=5,
        velocidade=30
    ):

        self.janela = janela

        self.linhas = linhas
        self.colunas = colunas

        self.velocidade = velocidade

        self.direcao = 1

        self.inimigos = []

        base = Sprite(caminho)

        largura = base.width
        altura = base.height

        espacamento_x = largura // 4
        espacamento_y = altura // 4

        offset_x = 20
        offset_y = 20

        for linha in range(self.linhas):
            for coluna in range(self.colunas):

                x = (
                    offset_x
                    + coluna * (largura + espacamento_x)
                )

                y = (
                    offset_y
                    + linha * (altura + espacamento_y)
                )

                inimigo = Inimigo(
                    caminho,
                    janela,
                    x,
                    y
                )

                self.inimigos.append(inimigo)

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
