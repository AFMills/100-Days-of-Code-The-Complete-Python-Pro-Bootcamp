import threading
import pyautogui as pag

class Dino:
    def __init__(self):
        pag.getActiveWindow().minimize()
        pag.press('space')
        pag.sleep(1)

        dino = pag.locateCenterOnScreen('dino.png', confidence=0.9)
        self.x = int(dino[0])
        self.y = int(dino[1])
        self.offset = 100

    def jump(self):
        while True:
            if pag.pixelMatchesColor(self.x + int(self.offset), self.y, (90, 90, 90), tolerance=100):
                pag.press('space')
                self.offset += 0.7

    def is_game_over(self):
        while True:
            if not pag.locateCenterOnScreen('game_over.png') is None:
                pag.press('space')
                self.offset = 100