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

        self.velocidade = velocidade / 2
        self.direcao = 1

        self.boss_linha = randint(0, linhas - 1)
        self.boss_coluna = randint(0, colunas - 1)

        self.inimigos = [[None for _ in range(colunas)] for _ in range(linhas)]

        base = Sprite(caminho)
        largura = base.width
        altura = base.height

        self.espacamento_x = largura // 4
        self.espacamento_y = altura // 4

        offset_x = 20
        offset_y = 20

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                x = offset_x + coluna * (largura + self.espacamento_x)
                y = offset_y + linha * (altura + self.espacamento_y)

                if linha == self.boss_linha and coluna == self.boss_coluna:
                    inimigo = Inimigo("sprites/player/boss.png", janela, x, y)
                else:
                    inimigo = Inimigo(caminho, janela, x, y)

                self.inimigos[linha][coluna] = inimigo

    def update(self, dt):
        self.movimentar(dt)

    def draw(self):
        for linha in self.inimigos:
            for inimigo in linha:
                if inimigo is not None:
                    inimigo.draw()

    def movimentar(self, dt):
        inverter = False

        for linha in self.inimigos:
            for inimigo in linha:
                if inimigo is not None:
                    if inimigo.sprite.x <= 0:
                        inverter = True
                        break
                    if inimigo.sprite.x + inimigo.sprite.width >= self.janela.width:
                        inverter = True
                        break
            if inverter:
                break

        if inverter:
            self.direcao *= -1
            for linha in self.inimigos:
                for inimigo in linha:
                    if inimigo is not None:
                        inimigo.sprite.y += 30
                        inimigo.sprite.x += self.direcao * self.velocidade * dt

        for linha in self.inimigos:
            for inimigo in linha:
                if inimigo is not None:
                    inimigo.sprite.x += self.velocidade * self.direcao * dt

    def chegou_no_player(self, player):
        for linha in self.inimigos:
            for inimigo in linha:
                if inimigo is not None:
                    colisao_vertical = (
                        inimigo.sprite.y + inimigo.sprite.height >= player.sprite.y
                    )
                    if colisao_vertical:
                        return True
        return False

    def atualizar_limites(self):
        vivos = [
            inimigo for linha in self.inimigos for inimigo in linha if inimigo is not None]

        if not vivos:
            return

        self.menor_x = min(inimigo.sprite.x for inimigo in vivos)
        self.maior_x = max(inimigo.sprite.x +
                           inimigo.sprite.width for inimigo in vivos)
        self.menor_y = min(inimigo.sprite.y for inimigo in vivos)
        self.maior_y = max(inimigo.sprite.y +
                           inimigo.sprite.height for inimigo in vivos)

    def escolhe_boss(self):
        # Encontra as coordenadas de todos os inimigos que ainda estão vivos
        vivos_coords = []
        for l in range(self.linhas):
            for c in range(self.colunas):
                if self.inimigos[l][c] is not None:
                    vivos_coords.append((l, c))

        if not vivos_coords:
            self.boss_linha = -1
            self.boss_coluna = -1
            return

        # Sorteia um dos inimigos vivos para ser o novo Boss
        self.boss_linha, self.boss_coluna = vivos_coords[randint(
            0, len(vivos_coords) - 1)]
        boss_atual = self.inimigos[self.boss_linha][self.boss_coluna]

        # Guarda a posição antiga para aplicar no novo sprite do Boss
        x = boss_atual.sprite.x
        y = boss_atual.sprite.y

        boss_atual.sprite = Sprite("sprites/player/boss.png")
        boss_atual.sprite.x = x
        boss_atual.sprite.y = y

    def matar_boss(self, inimigo_alvo):
        linha_alvo, coluna_alvo = -1, -1
        for l in range(self.linhas):
            for c in range(self.colunas):
                if self.inimigos[l][c] == inimigo_alvo:
                    linha_alvo, coluna_alvo = l, c
                    break
            if linha_alvo != -1:
                break

        if linha_alvo == -1:
            return False

        coordenadas_remover = [
            (linha_alvo, coluna_alvo),          # Boss
            (linha_alvo - 1, coluna_alvo),      # Cima
            (linha_alvo, coluna_alvo - 1),      # Esquerda
            (linha_alvo, coluna_alvo + 1)       # Direita
        ]

        for l, c in coordenadas_remover:
            if 0 <= l < self.linhas and 0 <= c < self.colunas:
                self.inimigos[l][c] = None

        self.escolhe_boss()
        return True
