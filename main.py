from lib.jogo import *
from rich.traceback import install
install()


def space_invaders():
    jogo = Jogo()
    jogo.run()


if __name__ == "__main__":
    space_invaders()
