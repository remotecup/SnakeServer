#!/usr/bin/python3

import src.Server.Server as Game


def main():
    g = Game.SnakeServer()
    g.connect()
    g.run()
    g.disconnect()


if __name__ == "__main__":
    main()
