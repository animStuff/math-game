"""
the coming lines feature the most dumbest waY possible to write the code in order to performt he function,
please forgive me im dumb and dont know much about pYgame onlY basics and what ive written SO YES THANKSSSSS

-some dood
written by aryan govil
"""
import pygame as pg
from pygame.locals import *
from core_logic import *
import sys

class character(pg.sprite.Sprite):
    def __init__(self, plPos: tuple, walls: pg.sprite.Group):
        # loading all character related sprites
        baseLst = ['1_1b.png', '2_2b.png', '3_3b.png', '4_4b.png', '5_5b.png']
        self.sprites = [
            [pg.image.load(f'sprites/{folder}/{file}') for file in baseLst] 
            for folder in ['left', 'right']]
        
        # setting up the character and his rect with 
        # a base image and specific vars
        self.image = pg.image.load('sprites/still.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = plPos[0], plPos[1]
        self.width, self.height = self.rect.width, self.rect.height
        self.sprites.append(self.image)

        # character states according to which 
        # game will function
        self.isJump, self.isStill = False, True
        self.Ypos = 0
        self.direct, self.Cwalk = 0, 0
        self.stepSize = 6
        self.Ysize = -16.5

        # sprite group 
        self.walls = walls
        self.killed = False
 

    def move(self):
        k_events = pg.key.get_pressed()
        dX, dY = 0, 0 
        if self.rect.y > 850:
            self.killed = True

        # Jumping 
        if k_events[K_SPACE] and self.isJump == False:
            self.Ypos = self.Ysize
            self.isJump = True
    
        
        # left, right, standing
        if k_events[K_d]:
            dX += self.stepSize
            self.direct = +1
            self.isStill = False

        elif k_events[K_a]:
            dX -= self.stepSize 
            self.direct = -1
            self.isStill = False

        else:
            self.isStill = True
            self.direct, self.Cwalk = 0, 0
        
        # keeping char on screen
        if self.rect.x < 10.:
            self.rect.x = 10.
        if self.rect.x > 667:
            self.rect.x = 667
    
        
        self.Ypos += 1.25 
        # limiting force of gravit to 15
        if  self.Ypos > 15:
            self.Ypos = 15 
        dY += self.Ypos

        # collision checks
        for wall in self.walls:
            if wall.rect.colliderect(self.rect.x + dX, self.rect.y, self.width, self.height):
                dX = 0

            if wall.rect.colliderect(self.rect.x, self.rect.y + dY, self.width, self.height):
                if dY < 0:
                    dY = wall.rect.bottom - self.rect.top
                    self.Ypos = 0

                elif dY >= 0:
                    dY = wall.rect.top - self.rect.bottom 
                    self.Ypos = 0
                    self.isJump = False
    
        #print(self.isStill)
        # updating the values based on input
        self.UpdateRects(dX, dY)
    

    def UpdateRects(self, num1:int, num2:int):
        self.rect.x += num1 * 1.1
        self.rect.y += num2

    def reutrnFrame(self):
        # adding a check to see if maximum has been reached and maximum is 
        # total * x as for showing a image for x frames instead of switching immediate
        if self.Cwalk == (len(self.sprites[0]) - 1) * (self.stepSize - 1):
            self.Cwalk = 0
        
        # checking for which direction and then according to that
        # which sprite is to be drawn 
        if self.direct == -1:   
            self.Cwalk += 1
            self.image = self.sprites[0][self.Cwalk//(self.stepSize - 1)]
        
        if self.direct == +1:
            self.Cwalk += 1
            self.image = self.sprites[1][self.Cwalk//(self.stepSize - 1)]

        if self.isStill:
            self.image = self.sprites[2]
        
        # final return after creation and calculating
        return self.image


    def update(self):
        # according to functions of this class 
        # returning all objs using Just one call to update method
        self.move()
        image = self.reutrnFrame()

        # return statement
        return image, self.rect, self.direct



class genWall(pg.sprite.Sprite):
    def __init__(self, pos: tuple, size: int):
        super().__init__()
        # creating a tile and its rect at a specific pos 
        self.image = pg.Surface((size, size))
        self.image.set_alpha(175)
        self.rect = self.image.get_rect(topleft = pos)

class map():
    def __init__(self, gameInstance):
        # initialize 
        self.askQuestion = makeMCQ()
        self.fontRender = pg.font.Font('Quicksand-Medium.ttf', 25)
        self.fontDict = pg.font.Font('Rubik.ttf', 18)
        self.gameScreen = pg.image.load('sprites/bg_game.png')
        self.game = gameInstance
        self.clock = pg.time.Clock()

        #vars
        self.stopBlit = False
        self.time = 0
        self.whichLevel = 1
        self.trial = 0
        self.pressedOnce = 0
        self.dict = {}
        self.numberOftimes = 0
        self.Ypos = 67
        self.timeDeathScreen = 0

        # creation of map and all needed vars
        self.level(self.whichLevel)

        # end screen
        self.endScreen = pg.image.load('sprites/base_game/Ending Screen.png')
        self.statsScreen = pg.image.load('sprites/base_game/stats screen.png')
        self.buttonN, self.buttonH = pg.image.load('sprites/base_game/button.png'), pg.image.load('sprites/base_game/buttonHover.png')
        self.heading = self.fontRender.render('Performance Overview:', True, (255, 255, 255))
        self.death = pg.image.load('sprites/death.png')
        self.dictFont = pg.font.Font('SecularOne-Regular.ttf', 22)

        # game timer
        self.timeTaken = 0
        self.deltaTime = 0


        
    def setup(self, data: list):
        # creating a sprite group containg ll walls
        self.walls = pg.sprite.Group()
        self.Tsize = 32
        
        # for loop run once to generate and put objs in the sprite group
        # (going through each cell and checking for thing)
        for posY, row in enumerate(data):
            for posX, column in enumerate(row):
                pos1 = posX * self.Tsize
                pos2 = posY * self.Tsize
                if column == '1':
                    tile = genWall((pos1, pos2), self.Tsize)
                    self.walls.add(tile)
                if column == 'P':
                    self.plPos = (pos1 - 32, pos2 - 32)
                    self.char = character(self.plPos, self.walls)

    def loadLevel(self):  
        if self.whichLevel != 5:
            self.timeTaken += self.deltaTime 
            txt = self.fontRender.render(f'Time: {str(self.timeTaken)[:5]}', True, (255, 255, 255))
            self.game.screen.blit(txt, (0, 0))

        # drawing the sprite group after storing with init method
        self.walls.draw(self.game.screen)

        # character related
        updatedVal = self.char.update()
    

        if updatedVal[1] == self.compareRect:
            self.walls.empty()
            self.stopBlit = True
            self.game.screen.blit(self.gameScreen, (0, 0))
           
        if self.stopBlit is False:
            if self.char.killed and self.whichLevel != 5:
                self.game.screen.blit(self.gameScreen, (0, 0)) 
                if self.timeDeathScreen != 20:
                    self.game.screen.blit(self.death, (0, 0)) 
                    self.timeDeathScreen += 1
                else:
                    exit()
            else:
                self.game.screen.blit(updatedVal[0], updatedVal[1])
            if self.whichLevel == 5:
                self.stopBlit = True
        
        else:
            if self.whichLevel == 5:
                self.game.screen.blit(self.gameScreen, (0,0))
                if self.time != 8:
                    self.game.screen.blit(self.endScreen, (0, 0))
                    self.buttonPressCode()
                    txt = self.fontRender.render(f'{str(self.timeTaken)[:5]} seconds', True, (255, 255, 255))
                    self.game.screen.blit(txt, (250, 287))

                else:
                    self.game.screen.blit(self.statsScreen, (0, 0))
                    self.game.screen.blit(self.heading, (230, 10))
                    self.Ypos = 37
                    for index, each in enumerate(self.dict.keys()):
                        checker = each[:-1]
                        if checker == 'correct':
                            text = f'{index + 1}. correct'
                        
                        if checker == 'wrong':
                            text = f'{index + 1}. wrong, correct = {self.dict[each][1]}'
                        text = self.dictFont.render(text, True, (255, 255, 255))
                        self.Ypos += 25
                        pos = (10, self.Ypos)

                        self.game.screen.blit(text, pos)


            elif self.askQuestion.time != 8:
                self.askQuestion.renderToscreen(self.game)
                
            else:
                if self.askQuestion.wrongAns == True:
                    if self.whichLevel == 1:
                        pass
                    else:
                        self.whichLevel = self.whichLevel
                else:
                    self.whichLevel += 1
                
                if self.whichLevel <= 4:
                    self.numberOftimes += 1
                    if self.askQuestion.wrongAns:
                        self.dict[f'wrong{self.numberOftimes}' ] = self.askQuestion.value
                    else:
                        self.dict[f'correct{self.numberOftimes}'] = self.askQuestion.value
                    self.level(self.whichLevel)
                    self.stopBlit = False
                    self.askQuestion = makeMCQ()
                    if self.whichLevel == 4:
                        self.whichLevel = 5
        
        self.deltaTime = self.clock.tick(30) / 1000

    def readData(self, filename: str):
        with open(filename, 'r') as file:
            data = file.read()
            self.mapData = data.splitlines()
        
    def level(self, which: int):
        if which == 1:
            self.readData('map_files/map0.txt')
            self.setup(self.mapData)
            self.compareRect = pg.Rect(673, 38, 58, 58)
            
        if which == 2:
            self.readData('map_files/map1.txt')
            self.setup(self.mapData)
            self.compareRect = pg.Rect(673, 6, 58, 58)      
            
        if which == 3:
            self.readData('map_files/map2.txt')
            self.setup(self.mapData)
            self.compareRect = pg.Rect(673, 38, 58, 58)
    
    def buttonPressCode(self):
        mousePos, toBlit = pg.mouse.get_pos(), None
    
        if (mousePos[0] >= 200 and mousePos[0] <= 450) and (mousePos[1] >= 525 and mousePos[1] <= 650):
            if self.pressedOnce == 0:
                toBlit = self.buttonH
            
            if pg.mouse.get_pressed()[0]:
                self.pressedOnce = 1
        else:
            toBlit = self.buttonN
        
        if self.pressedOnce == 1:
            toBlit = self.buttonH
            self.time += 1

        self.game.screen.blit(toBlit, (200,525))
    
 
        

class makeMCQ:
    def __init__(self):
        # loading images (prerequisites)
        self.nbox, self.hbox = pg.image.load('sprites/qRelate/notHover.png'), pg.image.load('sprites/qRelate/onHover.png')
        self.correct, self.wrong = pg.image.load('sprites/qRelate/correctBox.png'), pg.image.load('sprites/qRelate/wrongBox.png')
        self.qbox = pg.image.load('sprites/qRelate/qBox.png')
        self.fontRender = pg.font.Font('Quicksand-Medium.ttf', 22)

        # generating question and its setup
        data = algebraRandom().generate()
        from random import shuffle
        self.options = data[2] + [data[1]]
        shuffle(self.options)
        self.answer_index = self.options.index(data[1])

        # question rendering stuff
        question = self.fontRender.render(data[0], True, (255, 255, 255))
        self.qPos, self.question = ((((600 - question.get_width())/2) + 68), (((160 - question.get_height())/2) + 50)), question

        # checking vars
        self.index, self.stillCheck = None, True
        self.count, self.time = 0, 0 
        self.toShow = None
        self.wrongAns, self.answer = False, False
        self.value = None

    
    def renderToscreen(self, game):
        # base variables for calc
        mouse_pos = pg.mouse.get_pos()
        positions = [[68, 250], [378, 250], [68, 430], [378, 430]]

        # blitting question
        game.screen.blit(self.qbox, (68, 50))
        game.screen.blit(self.question, self.qPos) 
        
        # which version of image to be shown 
        # in different states like onHover, normal, if correct, if wrong
        for index, pos in enumerate(positions):
            # calculating font position and creating a renderable obj
            opts = self.fontRender.render(self.options[index], True, (255, 255, 255))
            aPos = ((((290 - opts.get_width())/2) + pos[0]), (((160 - opts.get_height())/2) + pos[1]))
            
            # checking if hovering is being done
            if (mouse_pos[0] >= pos[0] and mouse_pos[0] <= pos[0]  + self.nbox.get_width()) and (mouse_pos[1] >= pos[1] and mouse_pos[1] <= pos[1] + self.nbox.get_height()):  
                # setting hover image
                if self.stillCheck:
                    self.toShow = self.hbox
                    # if left clicked on image then is it correct or wrong?
                    if pg.mouse.get_pressed()[0]:
                        if index == self.answer_index:
                            self.answer = True
                            
                        else:
                            self.wrongAns = True
                            if self.count == 0:
                                self.index = index
                                self.count = 1

            # if not hover
            else:
                self.toShow = self.nbox


            # after calculating and creation final render each frame
            # checking if correct option pressed
            if index == self.answer_index and self.answer:
                game.screen.blit(self.correct, pos)
                self.stillCheck = False   
                self.value = self.options[index]
                self.time += 1         

            # checking if wrong__ option pressed   
            elif index == self.index and self.wrong:
                game.screen.blit(self.wrong, pos)
                self.stillCheck = False
                self.value = [self.options[index], self.options[self.answer_index]]
                self.time += 1

            # checking for hover
            else:
                game.screen.blit(self.toShow, pos)

            # blitting of text
            game.screen.blit(opts,  aPos) 