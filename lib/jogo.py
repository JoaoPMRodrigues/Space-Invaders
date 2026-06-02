from pplay.window import *
from pplay.keyboard import *
from pplay.sprite import *
from lib.player import *
from lib.tiro import *
from lib.botao import *
from lib.inimigo import *
from random import uniform, choice, randint
from time import perf_counter
from datetime import datetime


class Jogo:
    def __init__(self):

        self.largura = 800
        self.altura = 800

        self.janela = Window(self.largura, self.altura)
        self.janela.set_title("--- SPACE INVADERS ---")
        self.fundo = Sprite("sprites/menu/fundo.png")
        self.teclado = Keyboard()
        self.estado = "menu"

        self.dificuldade = 1
        self.pontuacao = 0
        self.criar_player()
        self.criar_menu()
        self.criar_dificuldade()
        self.criar_inimigos()

        self.tiros = []
        self.tiros_inimigos = []
        self.cooldown_inimigo = 1
        self.timer_inimigo = self.cooldown_inimigo
        self.menor_tempo = float("inf")

    def criar_player(self):
        self.velocidade_player = 400

        self.player = Player(
            "sprites/player/nave.png", self.janela, 240, 650, self.velocidade_player)

    def criar_menu(self):

        self.jogar = Botao(
            "sprites/menu/jogar.png", self.janela, 220, 246)

        self.dificuldade_botao = Botao(
            "sprites/menu/dificuldade.png", self.janela, 220, 358.5)

        self.rank = Botao(
            "sprites/menu/rank.png", self.janela, 220, 474)

        self.sair = Botao(
            "sprites/menu/sair.png", self.janela, 220, 597.5)

    def criar_dificuldade(self):

        self.facil = Botao(
            "sprites/modo/facil.png", self.janela, 325, 310)

        self.medio = Botao(
            "sprites/modo/medio.png", self.janela, 325, 400)

        self.dificil = Botao(
            "sprites/modo/dificil.png", self.janela, 325, 487)

    def criar_inimigos(self):

        self.enxame = Enxame(
            "sprites/player/monstro.png", self.janela, linhas=4, colunas=7, velocidade=120)

    def run(self):
        self.cooldown = self.fps = 0
        self.inicio = perf_counter()
        while True:

            self.dt = self.janela.delta_time()
            self.desenhar_fundo()

            if self.estado == "menu":
                self.update_menu()

            elif self.estado == "jogo":
                self.update_gameplay()

            elif self.estado == "dificuldade":
                self.update_dificuldade()
            elif self.estado == "rank":
                self.update_ranking()

            elif self.estado == "sair":
                self.resetar_jogo()
                break

            self.janela.update()

    def update_menu(self):

        self.jogar.draw()
        self.dificuldade_botao.draw()
        self.rank.draw()
        self.sair.draw()

        if self.jogar.update(self.janela):
            self.resetar_jogo()
            self.estado = "jogo"

        elif self.dificuldade_botao.update(self.janela):
            self.estado = "dificuldade"
        elif self.rank.update(self.janela):
            self.estado = "rank"

        elif self.sair.update(self.janela):
            self.estado = "sair"

    def update_gameplay(self):

        self.mostrar_fps()
        self.player.recarga(self.dificuldade)
        self.player.new_speed(
            self.velocidade_player / self.dificuldade
        )

        self.player.update(
            self.janela,
            self.teclado,
            self.dt
        )

        self.update_tiros()
        self.update_inimigos()
        self.update_tiros_inimigos()

        self.verificar_colisoes()
        self.verificar_colisoes_player()
        self.verificar_colisoes_tiros()
        if len(self.enxame.inimigos) == 0:
            self.vitoria()
            self.resetar_jogo()

        if self.enxame.chegou_no_player(self.player):
            self.estado = "menu"
            self.derrota()

        self.draw_gameplay()

        if self.teclado.key_pressed("ESC"):
            self.estado = "menu"

    def draw_gameplay(self):

        self.player.draw()

        for tiro in self.tiros:
            tiro.draw()

        for tiro in self.tiros_inimigos:
            tiro.draw()

        mensagem = ""
        for _ in range(self.player.vidas):
            mensagem += "❤️"
        for _ in range(3-self.player.vidas):
            mensagem += "💔"
        self.janela.draw_text(mensagem,
                              10,
                              40,
                              size=20,
                              color=(255, 255, 255)
                              )
        self.enxame.draw()

    def update_tiros(self):

        if (self.teclado.key_pressed("SPACE") and self.player.timer <= 0):
            self.tiros.append(
                Tiro("sprites/player/tiro.png", self.janela, self.player.sprite.x + self.player.sprite.width // 2, self.player.sprite.y, 600))

            self.player.timer = self.player.cooldown

        for tiro in self.tiros:
            tiro.update(self.dt)

        self.tiros = [
            tiro for tiro in self.tiros
            if not tiro.fora_da_tela()
        ]

    def update_inimigos(self):

        self.enxame.update(self.dt)
        self.enxame.atualizar_limites()

    def update_tiros_inimigos(self):

        self.timer_inimigo -= self.dt

        if (
            self.timer_inimigo <= 0
            and len(self.enxame.inimigos) > 0
        ):

            atirador = choice(self.enxame.inimigos)

            self.tiros_inimigos.append(
                Tiro(
                    "sprites/player/tiro_inimigo.png",
                    self.janela,
                    atirador.sprite.x +
                    atirador.sprite.width // 2,
                    atirador.sprite.y +
                    atirador.sprite.height,
                    -300
                )
            )

            self.timer_inimigo = (
                self.cooldown_inimigo *
                uniform(0.8, 1.2)
            )

        for tiro in self.tiros_inimigos:
            tiro.sprite.y += 300 * self.dt

        self.tiros_inimigos = [
            tiro for tiro in self.tiros_inimigos
            if tiro.sprite.y < self.altura
        ]

    def update_dificuldade(self):

        self.facil.draw()
        self.medio.draw()
        self.dificil.draw()

        if self.facil.update(self.janela):
            self.dificuldade = 1
            self.estado = "menu"

        elif self.medio.update(self.janela):
            self.dificuldade = 1.5
            self.estado = "menu"

        elif self.dificil.update(self.janela):
            self.dificuldade = 2
            self.estado = "menu"

        if self.teclado.key_pressed("ESC"):
            self.estado = "menu"

    def update_ranking(self):

        ranking = self.ler_ranking()

        self.janela.draw_text(
            "TOP 5",
            320,
            100,
            size=30,
            color=(255, 255, 255)
        )

        y = 180

        for posicao, jogador in enumerate(
            ranking,
            start=1
        ):

            texto = (
                f"{posicao}. "
                f"{jogador['nome']} | "
                f"{jogador['pontuacao']} pts | "
                f"{jogador['data']}"
            )

            self.janela.draw_text(
                texto,
                200,
                y,
                size=20,
                color=(255, 255, 255)
            )

            y += 40

        if self.teclado.key_pressed("ESC"):
            self.estado = "menu"

    def desenhar_fundo(self):

        self.janela.set_background_color((0, 0, 0))
        self.fundo.draw()

    def mostrar_fps(self):

        self.cooldown -= self.dt
        if self.cooldown < 0:
            self.fps = int(1 / self.dt) if self.dt > 0 else 0
            self.cooldown = 0.2
        self.janela.draw_text(
            f"FPS: {self.fps}", 10, 10, size=20, color=(255, 255, 255))

    def resetar_jogo(self):
        self.player.sprite.x = 240
        self.player.sprite.y = 650
        self.player.timer = 0
        self.dificuldade = 1
        self.pontuacao = 0
        self.tiros.clear()
        self.tiros_inimigos.clear()
        self.criar_inimigos()
        self.player.vidas = 3
        self.player.invencivel = False
        self.inicio = perf_counter()

    def verificar_colisoes_tiros(self):
        for tiro in self.tiros:
            for tiro_inimigos in self.tiros_inimigos:
                if tiro.sprite.collided(tiro_inimigos.sprite):
                    self.tiros.remove(tiro)
                    self.tiros_inimigos.remove(tiro_inimigos)
                    break

    def verificar_colisoes(self):

        tiros_remover = set()
        inimigos_remover = set()
        for tiro in self.tiros:
            if tiro.sprite.y < self.enxame.menor_y-tiro.sprite.height:
                continue
            if tiro.sprite.x < self.enxame.menor_x-tiro.sprite.width:
                continue
            if tiro.sprite.y > self.enxame.maior_y:
                continue
            if tiro.sprite.x > self.enxame.maior_x:
                continue

            for inimigo in self.enxame.inimigos:

                if tiro.sprite.collided(inimigo.sprite):

                    tiros_remover.add(tiro)
                    inimigos_remover.add(inimigo)
                    self.pontuacao += 100
                    break

        for tiro in tiros_remover:

            if tiro in self.tiros:
                self.tiros.remove(tiro)

        for inimigo in inimigos_remover:

            if inimigo in self.enxame.inimigos:
                self.enxame.inimigos.remove(inimigo)

    def verificar_colisoes_player(self):

        if self.player.invencivel:
            return

        tiros_remover = []

        for tiro in self.tiros_inimigos:

            if tiro.sprite.collided(self.player.sprite):

                tiros_remover.append(tiro)

                self.player.vidas -= 1

                self.player.respawn()

                break

        for tiro in tiros_remover:

            if tiro in self.tiros_inimigos:
                self.tiros_inimigos.remove(tiro)

        if self.player.vidas <= 0:

            self.resetar_jogo()
            self.estado = "menu"
            self.derrota()

    def vitoria(self):
        self.dificuldade += 0.1
        self.fim = perf_counter()
        self.time = self.fim - self.inicio
        if self.time < self.menor_tempo:
            self.menor_tempo = self.time

    def derrota(self):
        self.nome = str(input())
        if self.menor_tempo < float("inf"):
            self.pontuacao /= self.menor_tempo
            self.salvar_ranking()
        self.menor_tempo = float("inf")

    def salvar_ranking(self):
        data = datetime.now().strftime("%d/%m/%Y")

        with open("dados/rank.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{self.nome};{self.pontuacao*100:.0f};{data}\n")

    def ler_ranking(self):
        try:
            with open(
                "dados/rank.txt",
                "r",
                encoding="utf-8"
            ) as arquivo:

                ranking = []

                for linha in arquivo:

                    nome, pontuacao, data = (
                        linha.strip().split(";")
                    )

                    ranking.append({
                        "nome": nome,
                        "pontuacao": int(pontuacao),
                        "data": data
                    })

            ranking.sort(
                key=lambda jogador:
                jogador["pontuacao"],
                reverse=True
            )

            return ranking[:5]

        except FileNotFoundError:

            return []
