#!/usr/bin/python3

import Conf.conf as conf

if conf.game == 'Simple':
    import Games.Simple.Server.Server as Game
elif conf.game == 'Snake':
    import Games.Snake.Server.Server as Game


def main():
    if conf.game == 'Simple':
        g = Game.SimpleServer()
    elif conf.game == 'Snake':
        g = Game.SnakeServer()
    g.connect()
    g.run()
    g.disconnect()


if __name__ == "__main__":
    main()
