# Programming Project
# Hassaan Naveed - N0898071

# Imports
import pygame
import random


class MainMenu(object):

    def __init__(self, width=640, height=480):
        # Initilising the screen
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        # Creating fonts to use
        self.titleFont = pygame.font.SysFont('verdana', 75, bold=True)
        self.difficultyFont = pygame.font.SysFont('verdana', 60, bold=True)
        # Booleans for screen management
        self.mainScreen = True
        self.difficultyScreen = False

    def main(self):
        loop = True
        # mainloop
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            # Change screens
            if self.mainScreen and not self.difficultyScreen:
                self.mainMenu()

            if self.difficultyScreen and not self.mainScreen:
                self.difficultySelect()

    def mainMenu(self):
        # Title text
        text = "60.0"
        fontW, fontH = self.titleFont.size(text)
        surface = self.titleFont.render(text, True, (255, 255, 255))
        self.screen.blit(surface, ((self.width - fontW) // 2, (self.height - fontH) // 10))
        # Buttons
        play = Button(320, 240, self.screen).createButton("Play")
        quit = Button(320, 320, self.screen).createButton("Quit")
        # If play button pressed, change screens
        if play.onClick():
            self.mainScreen = False
            self.difficultyScreen = True
        # If exit button pressed, exit game
        if quit.onClick():
            pygame.quit()
        # fill background black
        self.background.fill((0, 0, 0))
        self.background.blit(self.screen, (0, 0))
        # update display
        pygame.display.update()

    def difficultySelect(self):
        # fill screen black
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.screen, (0, 0))
        # Title text
        text = "Select Difficulty"
        fontW, fontH = self.difficultyFont.size(text)
        surface = self.difficultyFont.render(text, True, (255, 255, 255))
        self.screen.blit(surface, ((self.width - fontW) // 2, (self.height - fontH) // 10))
        # Buttons for selecting difficulty
        easy = Button(320, 240, self.screen).createButton("Easy")
        medium = Button(320, 320, self.screen).createButton("Medium")
        hard = Button(320, 400, self.screen).createButton("Hard")
        # Call main game with relevent parameters
        if easy.onClick():
            Game(self.width, self.height, self.screen, self.background, 60, 0).main()
        if medium.onClick():
            Game(self.width, self.height, self.screen, self.background, 60, 1).main()
        if hard.onClick():
            Game(self.width, self.height, self.screen, self.background, 60, 2).main()

        # fill background black
        self.background.fill((0, 0, 0))
        self.background.blit(self.screen, (0, 0))
        #update display
        pygame.display.update()


class Game(object):

    def __init__(self, width, height, screen, background, fps=60, difficulty=0):
        # initilise screen
        self.screen = screen
        self.background = background
        self.width = width
        self.height = height
        # initilise timers
        self.clock = pygame.time.Clock
        self.fps = fps
        self.playtime = 0
        self.countdown = 15
        self.ms = 0
        self.difficulty = difficulty
        # for tracking the state of the background
        self.bgChange = True
        self.curBG = []
        # fonts for buttons and text
        self.font = pygame.font.SysFont('verdana', 20, bold=True)
        self.endFont = pygame.font.SysFont('verdana', 75, bold=True)
        self.reasonFont = pygame.font.SysFont('verdana', 30, bold=True)
        self.endTitle = ""
        self.endText = ""
        # border
        self.img = pygame.image.load('border.png').convert_alpha()
        # keep track of enemies
        self.enemyList = []
        self.enemySpeed = 0
        self.spawnRate = 0
        self.enemyCountdown = 0
        # initilise player and begin game
        self.p = Player()
        self.mainloop = True
        self.end = False

        # update difficulty depending on given parameters
        self.changeDifficulty()

    def changeDifficulty(self):
        diffs = ["easy", "medium", "hard"]
        # stores enemyspeed, spawnrate in dict
        settings = {
            "easy": [5, 2],
            "medium": [7, 1],
            "hard": [8, 0.5]
        }
        # selects based on given params
        diffList = settings[diffs[self.difficulty]]

        self.enemySpeed = diffList[0]
        self.spawnRate = diffList[1]

    def main(self):
        self.mainloop = True

        while self.mainloop:
            for event in pygame.event.get():
                # if the game is exited, stop the mainloop
                if event.type == pygame.QUIT:
                    self.mainloop = False
                if event.type == pygame.KEYDOWN:
                    # instantiate a projectile w/ given velocity/direction depending on the keypress
                    if event.key == pygame.K_LEFT:
                        self.p.instantiate(-5, 0)
                    if event.key == pygame.K_RIGHT:
                        self.p.instantiate(5, 0)
                    if event.key == pygame.K_UP:
                        self.p.instantiate(0, -5)
                    if event.key == pygame.K_DOWN:
                        self.p.instantiate(0, 5)
            # if game hasnt ended
            if not self.end:
                # update the clock and playtime
                self.ms = self.clock().tick(self.fps)
                self.playtime += self.ms / 1000.0

                # move any projectiles
                self.p.moveProjectile(self.screen)
                # always duisaply player above
                self.p.displayPlayer(self.screen)
                # create and move any enemies
                self.createEnemy()
                self.moveEnemy()
                # update playtime and background
                self.displayPlaytime(str("{:.1f}".format(self.playtime)))
                self.changeBackground()

                # if playtime reaches 60 end game
                if self.playtime > 60:
                    self.endTitle = "You Win!"
                    self.endText = "You survived 60 seconds!"
                    self.end = True

            # if game has ended display end screen
            if self.end:
                self.gameEnd(self.endTitle, self.endText)

        pygame.quit()

    def colourSelect(self):
        # choose random colour form list and return it
        col = ["red", "blue", "green", "purple"]
        rnd = random.randint(0, len(col)-1)
        colChoice = col[rnd]

        return colChoice

    def changeBackground(self):
        # always display border, update countdown
        self.screen.blit(self.img, (0, 0))
        self.countdown += self.ms / 1000.0
        # dictionary containing rgb colour codes for each colour
        # number at end associated with tracking which enemies can be killed
        bgColours = {
            "red": [245, 50, 115, 1],
            "blue": [75, 100, 215, 2],
            "green": [90, 200, 100, 3],
            "purple": [120, 60, 200, 4]
        }
        # if background should be changed
        if self.bgChange:
            # select a list using dictionary key
            # key randomly generated from earlier function
            bgChoice = bgColours[self.colourSelect()]
            # change current background to that list
            self.curBG = bgChoice
            self.bgChange = False

        # if bgCHange not currently true but countdown is greater than 10, set to true and reset countdown
        if not self.bgChange and int(self.countdown) >= 10:
            self.bgChange = True
            self.countdown = 0

        # update background
        pygame.display.flip()
        self.background.fill((self.curBG[0], self.curBG[1], self.curBG[2]))
        self.screen.blit(self.background, (0, 0))

    def displayPlaytime(self, text):
        # select font to render for playtime counter
        fontW, fontH = self.font.size(text)
        surface = self.font.render(text, True, (0, 0, 0))
        # blit text
        self.screen.blit(surface, ((self.width - fontW) // 14, (self.height - fontH) // 14))

    def createEnemy(self):
        # update countdown for enemy spawn
        self.enemyCountdown += self.ms / 1000.0
        # if the countdown is greater than the spawnrate
        if self.enemyCountdown > self.spawnRate:
            # instantiate new enemy and add to list
            enemy = Enemy()
            enemy.instantiate()
            self.enemyList.append(enemy)
            self.enemyCountdown = 0

    def moveEnemy(self):
        # for each enemy in the enemy list
        for e in self.enemyList:
            # decide which direction the enemy has spawned in and move them in a direction depending on that
            # towards the centre of the screen
            if e.spawnDirection == 0:
                e.updatePos(-self.enemySpeed, 0)
            elif e.spawnDirection == 1:
                e.updatePos(self.enemySpeed, 0)
            elif e.spawnDirection == 2:
                e.updatePos(0, -self.enemySpeed)
            elif e.spawnDirection == 3:
                e.updatePos(0, self.enemySpeed)

            # update the sprite
            self.screen.blit(e.enSprite, (e.rect.x, e.rect.y))

            # if the enemy has collided with the player and it is a different colour to the background
            # kill the enemy
            if e.rect.colliderect(self.p.rect) and e.chooseColor[1] != self.curBG[3]:
                self.enemyList.remove(e)
            # if the enemy has collided with the player and it is the same colour as the background
            # kill the player, end the game with relevant message
            elif e.rect.colliderect(self.p.rect) and e.chooseColor[1] == self.curBG[3]:
                self.enemyList.remove(e)
                self.endTitle = "Game Over"
                self.endText = "A bad guy killed you"
                self.end = True

            # for each projectile in the projectile list
            for p in self.p.projList:
                # if enemy collides with projectile and enemy is the same colour as the background
                # kill the enemy
                if e.rect.colliderect(p.rect) and e.chooseColor[1] == self.curBG[3]:
                    self.enemyList.remove(e)
                    self.p.projList.remove(p)
                # if enemy collides with projectile and enemy is different colour to background
                # kill player, end game with relevant message
                elif e.rect.colliderect(p.rect) and e.chooseColor[1] != self.curBG[3]:
                    self.p.projList.remove(p)
                    self.endTitle = "Game Over"
                    self.endText = "You killed a good guy"
                    self.end = True

    def gameEnd(self, text, reason):
        # on ending the game, fill the background with black
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        # create the you win/lose text
        textW, textH = self.endFont.size(text)
        endText = self.endFont.render(text, True, (255, 255, 255))
        self.screen.blit(endText, ((self.width - textW) // 2, (self.height - textH) // 4))
        # create the message - this is variable depending on how the player lost
        reasonW, reasonH = self.reasonFont.size(reason)
        reasonText = self.reasonFont.render(reason, True, (255, 255, 255))
        self.screen.blit(reasonText, ((self.width - reasonW) // 2, (self.height - reasonH) // 2))
        # create buttons
        retry = Button(160, 360, self.screen).createButton("Retry")
        quit = Button(460, 360, self.screen).createButton("Quit")

        # if player presses retry, restart main game with current params
        if retry.onClick():
            Game(self.width, self.height, self.screen, self.background, self.fps, self.difficulty).main()
        # if player presses quit, exit game
        if quit.onClick():
            pygame.quit()

        pygame.display.flip()


class Player(object):

    def __init__(self):
        # load player sprite
        self.pSprite = pygame.image.load("player.png").convert()
        # list to keep track of projectile objects
        self.projList = []
        self.rect = self.pSprite.get_rect()

    def displayPlayer(self, screen):
        # position player in center of screen
        self.rect.x = 320 - self.pSprite.get_width() // 2
        self.rect.y = 240 - self.pSprite.get_width() // 2
        screen.blit(self.pSprite, self.rect)

    def instantiate(self, x, y):
        # create projectile object, giving the direction to move in as params
        projectile = Projectile(x, y)
        # position it in center of screen
        projectile.rect.center = self.rect.center
        # add projectile object to list
        self.projList.append(projectile)

    def moveProjectile(self, screen):
        # for each projectile in the list
        for proj in self.projList:
            # update its porsition and blit the sprite
            proj.updatePos()
            screen.blit(proj.proj, (proj.rect.x, proj.rect.y))

            # if the projectile goes off screen, delete it
            if proj.rect.y < 0 or proj.rect.y > 480 or proj.rect.x < 0 or proj.rect.x > 640:
                self.projList.remove(proj)


class Projectile(object):

    def __init__(self, dirx, diry):
        # create sprite
        self.proj = pygame.image.load("bullet2.png").convert()
        # set position
        self.dirx = dirx
        self.diry = diry
        self.rect = self.proj.get_rect()

    def updatePos(self):
        # update the position of th eprojectile with the given directions
        self.rect.x += self.dirx
        self.rect.y += self.diry


class Enemy(object):

    def __init__(self):
        # list of lists containing image file and associated colour
        # number at end links to colours for the background
        # used for keeping track of which enemies can be hit etc
        self.colors = [["redEnemy.png", 1],
                       ["blueEnemy.png", 2],
                       ["greenEnemy.png", 3],
                       ["purpleEnemy.png", 4]]
        # choose random colour for enemy
        self.chooseColor = self.colors[random.randint(0, len(self.colors)-1)]
        # load that as sprite
        self.enSprite = pygame.image.load(self.chooseColor[0]).convert()
        self.rect = self.enSprite.get_rect()
        self.spawnDirection = None
        # possible spawnpoints
        # numbers at end used for keeping track of where it spawned. so it can be moved in the correct direction
        self.spawn = {
            "right": [640, 240, 0],
            "left": [0, 240, 1],
            "bottom": [320, 480, 2],
            "top": [320, 0, 3]
        }

    def chooseDirection(self):
        # choose a random place to spawn the enemy
        directions = ["right", "left", "bottom", "top"]
        rnd = directions[random.randint(0, len(directions)-1)]

        return rnd

    def instantiate(self):
        # spawn enemy in given location
        dir = self.spawn[self.chooseDirection()]
        # update its position to those coordinates
        self.rect.center = dir[0], dir[1]
        # chaneg spawn direction variable to number at end
        self.spawnDirection = dir[2]

    def updatePos(self, x, y):
        # update enemies position using given directions
        self.rect.x += x
        self.rect.y += y


# PyGame has no way of creating buttons, and tools that were available to attempt doing so were frustrating
# Created my own button class to make this easier

class Button(object):

    def __init__(self, x, y, screen):
        # load sprite
        self.button = pygame.image.load("button.png").convert()
        self.x = x
        self.y = y
        self.width = 200
        self.height = 55
        self.screen = screen
        self.rect = self.button.get_rect()
        self.font = pygame.font.SysFont('verdana', 30, bold=True)

    def createButton(self, text):
        # position button in given x, y coordinates
        self.rect.center = self.x, self.y
        self.screen.blit(self.button, self.rect)
        # add any text to the button
        self.addText(text)

        return self

    def addText(self, btnText):
        # add any given text to the button
        text = btnText
        surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surface, self.rect)

    def onClick(self):
        # get position of mouse cursor
        mousePos = pygame.mouse.get_pos()

        # if cursor inside button coordinates
        if self.rect.x + self.width > mousePos[0] > self.rect.x \
                and self.rect.y + self.height > mousePos[1] > self.rect.y:

            # if button click detected, return true
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    return True


if __name__ == "__main__":
    pygame.init()
    MainMenu().main()
