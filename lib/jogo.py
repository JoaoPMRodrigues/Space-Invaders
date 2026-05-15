from time import sleep
from pplay.window import *
from pplay.keyboard import *
from pplay.sprite import *
from lib.player import *
from lib.tiro import *
from lib.botao import *
from lib.inimigo import *


class Jogo:
    def __init__(self):

        # Janela
        self.largura = 800
        self.altura = 800

        self.janela = Window(self.largura, self.altura)
        self.janela.set_title("--- SPACE INVADERS ---")

        # Fundo
        self.fundo = Sprite("sprites/menu/fundo.png")

        # Input
        self.teclado = Keyboard()

        # Estado do jogo
        self.estado = "menu"

        # Dificuldade
        self.dificuldade = 1

        # Entidades
        self.criar_player()
        self.criar_menu()
        self.criar_dificuldade()
        self.criar_inimigos()

        # Tiros
        self.tiros = []

    # =========================
    # CRIAÇÃO DE OBJETOS
    # =========================

    def criar_player(self):
        self.velocidade_player = 400

        self.player = Player(
            "sprites/player/nave1.png",
            self.janela,
            240,
            650,
            self.velocidade_player
        )

    def criar_menu(self):

        self.jogar = Botao(
            "sprites/menu/jogar.png",
            self.janela,
            220,
            246
        )

        self.dificuldade_botao = Botao(
            "sprites/menu/dificuldade.png",
            self.janela,
            220,
            358.5
        )

        self.rank = Botao(
            "sprites/menu/rank.png",
            self.janela,
            220,
            474
        )

        self.sair = Botao(
            "sprites/menu/sair.png",
            self.janela,
            220,
            597.5
        )

    def criar_dificuldade(self):

        self.facil = Botao(
            "sprites/modo/facil.png",
            self.janela,
            325,
            310
        )

        self.medio = Botao(
            "sprites/modo/medio.png",
            self.janela,
            325,
            400
        )

        self.dificil = Botao(
            "sprites/modo/dificil.png",
            self.janela,
            325,
            487
        )

    def criar_inimigos(self):

        self.enxame = Enxame(
            "sprites/player/monstro.png",
            self.janela,
            linhas=4,
            colunas=7,
            velocidade=120
        )

    # =========================
    # LOOP PRINCIPAL
    # =========================

    def run(self):

        while True:

            self.dt = self.janela.delta_time()

            self.desenhar_fundo()

            if self.estado == "menu":
                self.update_menu()

            elif self.estado == "jogo":
                self.update_gameplay()

            elif self.estado == "dificuldade":
                self.update_dificuldade()

            elif self.estado == "sair":
                break

            self.janela.update()

    # =========================
    # MENU
    # =========================

    def update_menu(self):

        self.jogar.draw()
        self.dificuldade_botao.draw()
        self.rank.draw()
        self.sair.draw()

        if self.jogar.update(self.janela):
            self.resetar_jogo()
            self.estado = "jogo"
            sleep(0.2)

        elif self.dificuldade_botao.update(self.janela):
            self.estado = "dificuldade"
            sleep(0.2)

        elif self.sair.update(self.janela):
            self.estado = "sair"
            sleep(0.2)

    # =========================
    # GAMEPLAY
    # =========================

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
        self.verificar_colisoes()

        if len(self.enxame.inimigos) == 0:
            tiros_remover = []
            self.criar_inimigos()

        if self.enxame.chegou_no_player(self.player):
            self.estado = "menu"

        self.draw_gameplay()

        if self.teclado.key_pressed("ESC"):
            self.estado = "menu"

    def draw_gameplay(self):

        self.player.draw()

        for tiro in self.tiros:
            tiro.draw()

        self.enxame.draw()

    # =========================
    # TIROS
    # =========================

    def update_tiros(self):

        if (
            self.teclado.key_pressed("SPACE")
            and self.player.timer <= 0
        ):

            self.tiros.append(
                Tiro(
                    "sprites/player/tiro.png",
                    self.janela,
                    self.player.sprite.x
                    + self.player.sprite.width // 2,
                    self.player.sprite.y,
                    600
                )
            )

            self.player.timer = self.player.cooldown

        for tiro in self.tiros:
            tiro.update(self.dt)

        self.tiros = [
            tiro for tiro in self.tiros
            if not tiro.fora_da_tela()
        ]

    # =========================
    # INIMIGOS
    # =========================

    def update_inimigos(self):

        self.enxame.update(self.dt)

    # =========================
    # DIFICULDADE
    # =========================

    def update_dificuldade(self):

        self.facil.draw()
        self.medio.draw()
        self.dificil.draw()

        if self.facil.update(self.janela):
            self.dificuldade = 1
            self.estado = "menu"
            sleep(0.2)

        elif self.medio.update(self.janela):
            self.dificuldade = 1.5
            self.estado = "menu"
            sleep(0.2)

        elif self.dificil.update(self.janela):
            self.dificuldade = 2
            self.estado = "menu"
            sleep(0.2)

        if self.teclado.key_pressed("ESC"):
            self.estado = "menu"

    # =========================
    # UTILITÁRIOS
    # =========================

    def desenhar_fundo(self):
        self.janela.set_background_color((0, 0, 0))
        self.fundo.draw()

    def mostrar_fps(self):

        fps = int(1 / self.dt) if self.dt > 0 else 0

        self.janela.draw_text(
            f"FPS: {fps}",
            10,
            10,
            size=20,
            color=(255, 255, 255)
        )

    def resetar_jogo(self):

        self.player.sprite.x = 240
        self.player.sprite.y = 650

        self.player.timer = 0

        self.tiros.clear()
        self.criar_inimigos()

    def verificar_colisoes(self):

        tiros_remover = []
        inimigos_remover = []

        for tiro in self.tiros:

            for inimigo in self.enxame.inimigos:

                if tiro.sprite.collided(inimigo.sprite):

                    tiros_remover.append(tiro)
                    inimigos_remover.append(inimigo)

        # Remove tiros
        for tiro in tiros_remover:

            if tiro in self.tiros:
                self.tiros.remove(tiro)

        # Remove inimigos
        for inimigo in inimigos_remover:

            if inimigo in self.enxame.inimigos:
                self.enxame.inimigos.remove(inimigo)
