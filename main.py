"""
written by aryan govil
"""
import pygame as pg
from sprites import * 
import sys
    
class Game:     
    def __init__(self):
        # baseline arguments
        self.mapSize = (736, 736)
        self.title = 'multiple choices of death'
        self.frameRate = 60
        self.bg_image = pg.image.load('sprites/bg_game.png') 
        self.startScreens = pg.image.load('sprites/base_game/stats screen.png')
        self.bh, self.bn = pg.image.load('sprites/qRelate/onHover.png'), pg.image.load('sprites/qRelate/notHover.png')

        # module prequisetes
        pg.init()   
        pg.display.set_caption(self.title.capitalize())
        self.screen = pg.display.set_mode(self.mapSize)
        self.fClock = pg.time.Clock()
        self.fontRenderer = pg.font.Font('Montserrat.ttf', 30)
        self.fontButton = pg.font.Font('SecularOne-Regular.ttf', 25)
        self.font = pg.font.Font('Quicksand-Medium.ttf', 30)
        icon = pg.image.load('sprites/icon.png')
        pg.display.set_icon(icon)

        # sprite files initialize
        self.loadLevel = map(self)
        self.startClicked, self.about = False, False
        self.stillCheck = True      
        self.time, self.toShow = 0, None
        self.trial = False
        self.pressedOnce, self.ntime = 0, 0

    def drawToWindow(self):
        # drawing background image

        if self.trial:
            self.screen.blit(self.bg_image, (0, 0))   
            self.loadLevel.loadLevel()

        else:
            self.startScreen()

        pg.display.update()

    def mainloop(self):
        active = True
        while active:
            for event in pg.event.get():
                if event.type == pg.QUIT:  
                    active = False
                    
            self.drawToWindow()
    
    def startScreen(self):
        if self.time != 8:
            self.screen.blit(self.startScreens, (0, 0))
            txt = self.fontRenderer.render('multiple choices of death', True, (255, 255, 255))
            self.screen.blit(txt, (177.5, 30))
            self.buttonLogic()
        else:
            if self.startClicked:
                self.trial = True
            
            elif self.about:
                if self.ntime != 8:
                    self.screen.fill((0, 0, 0))
                    txt = self.font.render('Nothing much, developed by maths group 5', True, (255, 255, 255))
                    self.screen.blit(txt, ((736 - txt.get_width())/2,  (736 - txt.get_height())/2))
                    self.backButton()
                
                else:
                    exit()

    def buttonLogic(self):
        mousePos = pg.mouse.get_pos()
        pos = [[220, 200], [220, 400]]
        texts = ['START', 'ABOUT']
        txtPos = [[326.5, 265], [323.5, 465]]
        
        for index, each in enumerate(pos):
            if (mousePos[0] >= each[0] and mousePos[0] <= each[0] + 290) and (mousePos[1] >= each[1] and mousePos[1] <= each[1] + 160):
                if self.stillCheck:
                    self.toShow = self.bh

                    if pg.mouse.get_pressed()[0]:
                        if each == [220, 200]:
                            self.startClicked = True
                        else:
                            self.about = True
            
            else:
                self.toShow = self.bn
            
            if self.startClicked and each == [220, 200]:
                self.screen.blit(self.bh, each)
                self.stillCheck = False
                self.time += 1
            
            elif self.about and each == [220, 400]:
                self.screen.blit(self.bh, each)
                self.stillCheck = False
                self.time += 1
            
            else:
                self.screen.blit(self.toShow, each)
                
            text = self.fontButton.render(texts[index], True, (255, 255, 255))
            self.screen.blit(text, txtPos[index])

    def backButton(self):
        mousePos, toBlit = pg.mouse.get_pos(), None
        text = self.fontButton.render('EXIT', True, (255, 255, 255))
        x_axis = 215     
        if (mousePos[0] >= x_axis and mousePos[0] <= x_axis + 290) and (mousePos[1] >= 510 and mousePos[1] <= 510 + 160):
            if self.pressedOnce == 0:
                toBlit = self.bh
            
            if pg.mouse.get_pressed()[0]:
                self.pressedOnce = 1
            
        else:
            toBlit = self.bn
        
        if self.pressedOnce == 1:
            toBlit = self.bh
            self.ntime += 1
        
        self.screen.blit(toBlit, (x_axis, 510))
        self.screen.blit(text, (333, 571.5))
    
    
 

if __name__ == '__main__':
    game = Game()   
    game.mainloop()
