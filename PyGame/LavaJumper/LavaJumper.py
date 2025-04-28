# Pygame platform tests
import pygame
import random
import os
pygame.init()

# paths
#game_folder = os.path.dirname(__file__)
#img_folder = os.path.join(game_folder, 'JumperImages')
#player_img = pygame.image.load(os.path.join(img_folder, 'FrogBlob.png')).convert()
# window size and frame rate
WIDTH = 400
HEIGHT = 700
FPS = 30

# define clock
clock = pygame.time.Clock()

# define fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms",25)
token_font = pygame.font.SysFont("comicsansms",20)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUE2 = (0, 160, 255)
ORANGE = (255, 120, 0)
ORANGE2 = (240, 150, 20)
BROWN = (70,40,0)
CYAN = (0,255,255)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((20, 20))
        #self.image.fill(GREEN)
        self.image = pygame.image.load('JumperImages/FrogBlob.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2 - 10)
        self.speedx = 0
        self.speedy = 0
        self.falling = True
        self.platspeedx = 0
        self.score = 0
        self.boostTokens = 0
        self.parachuteTokens = 0
        self.cooldownB = False
        self.cooldownP = False
        

    def update(self):
        #Keyboard input responses
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP] and self.falling == False:
            self.speedy = -10
            self.falling = True
        if keystate[pygame.K_q] and (self.boostTokens > 0) and (self.cooldownB == False):
            self.speedy = -30
            self.falling = True
            self.cooldownB = True
            self.boostTokens -= 1
        if keystate[pygame.K_w] and (self.parachuteTokens > 0) and (self.cooldownP == False):
            self.cooldownP = True
            self.parachuteTokens -= 1
##        if keystate[pygame.K_j]:
##            self.speedy = -40 

        #Change position based on speed
        self.rect.x += self.speedx + self.platspeedx
        self.rect.y += self.speedy

        #Side physics and gravity
        if self.falling == True:
            if self.cooldownP == True:
                if self.speedy < 3:
                    self.speedy += 0.5
                else:
                    self.speedy = 3
            else:
                if self.speedy < 15:
                    self.speedy += 0.5
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom > HEIGHT:
            self.speedy = -self.speedy
        if self.rect.right < 0:
            self.rect.left = WIDTH

        #Makes the player match the speed of, and stand on a platform,
        #Only when falling
        self.platspeedx = 0
        if self.speedy > 0:
            hit = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit:
                self.falling = False
                for platform in g.platforms:
                    if self.isOn(platform):
                        if self.rect.bottom >= platform.rect.top and self.rect.top < platform.rect.top:
                            self.rect.bottom = platform.rect.top
                            self.platspeedx = platform.speedx
                            self.speedx = 0
                            self.speedy = 1
                            self.cooldownB = False
                            self.cooldownP = False
            else:
                self.falling = True

        #Scrolls the platforms
        if self.rect.top <= HEIGHT / 4:
            self.rect.y += max(abs(self.speedy), 2)
            for platform in g.platforms:
                platform.rect.y += max(abs(self.speedy), 2)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.score += 10
            for boost in g.boosts:
                boost.rect.y += max(abs(self.speedy), 2)
                if boost.rect.top >= HEIGHT:
                    boost.kill()
            for parachute in g.parachutes:
                parachute.rect.y += max(abs(self.speedy), 2)
                if parachute.rect.top >= HEIGHT:
                    parachute.kill()

        #Checks for boost/parachute token hits, increases the total and
        #kills the token sprite
        hitB = pygame.sprite.spritecollide(self, g.boosts, False)
        if hitB:
            for boost in g.boosts:
                if self.isOn(boost):
                    boost.kill()
                    self.boostTokens += 1
        hitP = pygame.sprite.spritecollide(self, g.parachutes, False)
        if hitP:
            for parachute in g.parachutes:
                if self.isOn(parachute):
                    parachute.kill()
                    self.parachuteTokens += 1
            

    #Checks whether the player is touching the platform
    def isOn(self, platform):
        return (pygame.Rect(self).colliderect(platform.rect))
    

class Platform(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((49, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = random.randrange(1,7)
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH and self.speedx > 0:
            self.speedx = -self.speedx
        if self.rect.left < 0 and self.speedx < 0:
            self.speedx = -self.speedx

class BoostToken(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(ORANGE2)
        self.rect = self.image.get_rect()
        self.centerPos = (random.randrange((0+20), (WIDTH-20))), random.randrange(0, (HEIGHT - 600))
        self.rect.center = self.centerPos

class ParachuteToken(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(BLUE2)
        self.rect = self.image.get_rect()
        self.centerPos = (random.randrange((0+20), (WIDTH-20))), random.randrange(0, (HEIGHT - 600))
        self.rect.center = self.centerPos

# Game loop
class GameLoop(pygame.sprite.Sprite):
    #Initialises the game and the gameloop
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Platforms")
        self.clock = pygame.time.Clock()
        self.running = True
        self.gameOver = False
        self.highScore = "0"

    #Sets up a new game
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.platforms = pygame.sprite.Group()
        self.boosts = pygame.sprite.Group()
        self.parachutes = pygame.sprite.Group()
        for i in range(9):
            self.center = ((i+1)*WIDTH/9, ((i+1)*HEIGHT/8)-10)
            self.p = Platform(self.center)
            self.all_sprites.add(self.p)
            self.platforms.add(self.p)
        self.HighScore()
        self.backColour = (0,0,0)
        self.stage = 0
        
        self.run()

    #Waits for a key input
    def waitForKey(self):
        waiting = True
        self.running = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    waiting = False

    #Game Over Screen
    def endScreen(self):
        self.screen.fill(WHITE)
        self.HighScore()
        smg = "%s" "%s" %("Score = ",self.player.score)
        gms = "%s" "%s" %("High Score = ",self.highScore)
        self.message(smg, RED, -5)
        self.message(gms, RED, -4)
        self.message("Game Over!", RED, 0)
        self.message("Press any key ", RED, 1)
        self.message("to start again!", RED, 2)
        self.message("Or quit!", RED, 4)
        pygame.display.update()
        self.waitForKey()

    #Start screen
    def startScreen(self):
        self.screen.fill(BLACK)
        #self.HighScore()
        gms = "%s" "%s" %("High Score = ",self.highScore)
        self.message("Lava Jumper!!!!", WHITE, -8)
        self.message("Climb as high as you can", WHITE, -7)
        self.message("without falling into the lava", WHITE, -6)
        self.message("Use the arrow keys to move", WHITE, -4)
        self.message("Use q/w for specials", WHITE, -3)
        #self.message(gms, WHITE, -1)
        self.message("Press any key ", WHITE, 1)
        self.message("to start!", WHITE, 2)
        self.message("Or immediately quit!!", WHITE, 5)
        pygame.display.update()
        self.waitForKey()

    def events(self):
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False
        # Death?
        if self.player.rect.bottom > (HEIGHT - 100):
            self.gameOver = True
            self.running = False
            

    def update(self):
        # Update
        self.all_sprites.update()
        # New Platforms
        if len(self.platforms) < 7:
            self.ChangeBackColour()
            self.center = (WIDTH/2, (1*HEIGHT/8)-10)
            self.p = Platform(self.center)
            self.all_sprites.add(self.p)
            self.platforms.add(self.p)
            n = random.randrange(1,10)
            if n == 5:
                self.b = BoostToken()
                self.boosts.add(self.b)
                self.all_sprites.add(self.b)
            if n == 4:
                self.para = ParachuteToken()
                self.parachutes.add(self.para)
                self.all_sprites.add(self.para)

    def draw(self):
        # Draw / render
        self.screen.fill(self.backColour)
        self.ScoreDisplay(self.player.score)
        self.TokenDisplay()
        self.all_sprites.draw(self.screen)
        pygame.draw.rect(self.screen, ORANGE, [0,HEIGHT-100,WIDTH,100]) #Lava
        # *after* drawing everything, flip the display
        pygame.display.flip()

    # Main running loop
    def run(self):
        self.running = True
        while self.running:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()            
    
    # Writes a message in the middle of the screen.
    def message(self,msg,colour,pos):
        mesg = font_style.render(msg, True, colour)
        self.screen.blit(mesg, [WIDTH/6, (pos*25)+(HEIGHT/3)])

    # Writes the score at the top
    def ScoreDisplay(self, score):
        value = score_font.render("Score: " + str(score), True, WHITE)
        self.screen.blit(value, [0,0])
        value = score_font.render("High Score: " + str(self.highScore), True, WHITE)
        self.screen.blit(value, [0,25])

    # Writes the token counts on the screen
    def TokenDisplay(self):
        value = token_font.render("Boosts: " + str(self.player.boostTokens), True, WHITE)
        if self.player.boostTokens > 0:
            self.screen.blit(value, [0,50])
        value = token_font.render("Parachutes: " + str(self.player.parachuteTokens), True, WHITE)
        if self.player.parachuteTokens > 0:
            self.screen.blit(value, [0,70])

    # Reads and writes the highscore to file
    def HighScore(self):
        try:
            f = open("highScore.txt")
            f.close()
        except IOError:
            f = open("highScore.txt", "w")
            f.write("0")
            f.close()  
        f = open("highScore.txt", "r")
        self.highScore = (f.read())
        f.close()
        if int(float(self.player.score)) > int(float(self.highScore)):
            f = open("highScore.txt", "w")
            f.write(str(self.player.score))
            f.close()
            self.highScore = self.player.score
        else:
            self.highScore = self.highScore

    # Determines the background colour
    def ChangeBackColour(self):
        intvl = 15
        if self.stage == 0:
            #Brown(70,40,0)
            red = self.backColour[0] + (70/intvl)
            green = self.backColour[1] + (40/intvl)
            blue = self.backColour[2] + (0)
            self.backColour = (red,green,blue)
            if (round(self.backColour[0]),round(self.backColour[1]),round(self.backColour[2])) == (70,40,0):
                self.stage = 1
                self.backColour = (70,40,0)
        if self.stage == 1:
            #Dark Green(10,60,20)
            red = self.backColour[0] + (-60/intvl)
            green = self.backColour[1] + (20/intvl)
            blue = self.backColour[2] + (20/intvl)
            self.backColour = (red,green,blue)
            if (round(self.backColour[0]),round(self.backColour[1]),round(self.backColour[2])) == (10,60,20):
                self.stage = 2
                self.backColour = (10,60,20)
        if self.stage == 2:
            #Dark Cyan(10,90,90)
            red = self.backColour[0] + (0)
            green = self.backColour[1] + (30/intvl)
            blue = self.backColour[2] + (70/intvl)
            self.backColour = (red,green,blue)
            if (round(self.backColour[0]),round(self.backColour[1]),round(self.backColour[2])) == (10,90,90):
                self.stage = 3
                self.backColour = (10,90,90)
        if self.stage == 3:
            #Dark Purple(50,20,80)
            red = self.backColour[0] + (40/intvl)
            green = self.backColour[1] + (-70/intvl)
            blue = self.backColour[2] + (-10/intvl)
            self.backColour = (red,green,blue)
            if (round(self.backColour[0]),round(self.backColour[1]),round(self.backColour[2])) == (50,20,80):
                self.stage = 4
                self.backColour = (50,20,80)
        if self.stage == 4:
            #Black(0,0,0)
            red = self.backColour[0] + (-50/intvl)
            green = self.backColour[1] + (-20/intvl)
            blue = self.backColour[2] + (-80/intvl)
            self.backColour = (red,green,blue)
            if (round(self.backColour[0]),round(self.backColour[1]),round(self.backColour[2])) == (0,0,0):
                self.stage = 5
                self.backColour = (0,0,0)
                
        
        
        

g = GameLoop()
g.startScreen()
while g.running:
    g.new()
    g.endScreen()
pygame.quit()
