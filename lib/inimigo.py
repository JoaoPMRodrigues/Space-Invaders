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

        # Sprite base apenas para medir
        base = Sprite(caminho)

        largura = base.width
        altura = base.height

        # Espaçamento = metade do sprite
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

    # =========================
    # UPDATE
    # =========================

    def update(self, dt):

        self.movimentar(dt)

    # =========================
    # DRAW
    # =========================

    def draw(self):

        for inimigo in self.inimigos:
            inimigo.draw()

    # =========================
    # MOVIMENTO
    # =========================

    def movimentar(self, dt):

        inverter = False

        # Verifica colisão lateral
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

        # Inverte TODOS no mesmo frame
        if inverter:

            self.direcao *= -1

            for inimigo in self.inimigos:
                inimigo.sprite.y += 30
                inimigo.sprite.x += self.direcao * self.velocidade * dt

        # Movimento horizontal
        for inimigo in self.inimigos:

            inimigo.sprite.x += (
                self.velocidade
                * self.direcao
                * dt
            )

    # =========================
    # GAME OVER
    # =========================

    def chegou_no_player(self, player):

        for inimigo in self.inimigos:

            colisao_vertical = (
                inimigo.sprite.y + inimigo.sprite.height
                >= player.sprite.y
            )

            colisao_horizontal = (
                inimigo.sprite.x < player.sprite.x + player.sprite.width
                and
                inimigo.sprite.x + inimigo.sprite.width > player.sprite.x
            )

            if colisao_vertical and colisao_horizontal:
                return True

        return False
