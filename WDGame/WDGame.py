#!/usr/bin/env python

import Actions

if __name__=='__main__':

    Actions.startGame()

    while True:
        try:
            Actions.getAction()
        except KeyboardInterrupt:
            Actions.quitGame()
