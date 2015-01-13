'''
Bryan Cho
Car Game Project
'''
import time, thread, threading
import pygame, sys
import random
import pygame.sprite
import pygame.font
import pygame.mixer
from pygame.locals import *

#----------------Obstacle Class-------------------
class obstacle:
        def __init__(self, numLane, y, image):
                self.numLane = numLane 
                self.y = y #y location property
                self.image = image

#-----------------Interval Manager----------------
class Operation(threading._Timer):
    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        while True:
            self.finished.clear()
            self.finished.wait(self.interval)
            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
            else:
                return
            self.finished.set()

class Manager(object):
        #Manager that contains an array of operations "ops" to be run 
    ops = []

    def add_operation(self, operation, interval, args=[], kwargs={}):
        op = Operation(interval, operation, args, kwargs)
        self.ops.append(op)
        thread.start_new_thread(op.run, ())
       #adds an operation with the given parameters to "ops"
    def clear_operations(self):
                ops.clear()
        
    def stop(self):
        for op in self.ops:
            op.cancel()
        self._event.set()

#--------------------Functions--------------------
def display_text(text, x, y, label): #function that is used to display text on the screen with the given parameters
   font=pygame.font.Font(None,30)
   scoretext=font.render(label+str(text), 1,(255,255,255))
   surface.blit(scoretext, (x, y))

def spawn_obstacle(obstacleArray): #0 is left lane, 1 is middle lane, 2 is right lane
        o = obstacle(random.randint(0,2), 0, obstacleArray[random.randint(0,len(obstacleArray)-1)]) #create an obstacle with random lane, and random image
        spawnedObstacles.append(o) #add to list of obastacles to be rendered
        #difficulty settings:
        if score >= 5000 and score < 15000: 
                o2 = obstacle(random.randint(0,2), (-1)*random.randint(450,500), obstacleArray[random.randint(0,len(obstacleArray)-1)])
                spawnedObstacles.append(o2)
        elif score >= 15000 and obstacleArray != boosts:
                o2 = obstacle(random.randint(0,2), (-1)*random.randint(550,600), obstacleArray[random.randint(0,len(obstacleArray)-1)])
                spawnedObstacles.append(o2)
                o3 = obstacle(random.randint(0,2), (-1)*random.randint(300,350), obstacleArray[random.randint(0,len(obstacleArray)-1)])
                spawnedObstacles.append(o3)     
#----------------Initial Variables----------------
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
fps=pygame.time.Clock()

x=480
y=800
surface=pygame.display.set_mode((x,y),0,32)

pBackground = pygame.image.load("img/Background.png").convert_alpha()
carForward = pygame.image.load("img/carForward.png").convert_alpha()
carLeft = pygame.image.load("img/carLeft.png").convert_alpha()
carRight = pygame.image.load("img/carRight.png").convert_alpha()
carBoost = pygame.image.load("img/boostcar.png").convert_alpha()

#Obstacles
pRock = pygame.image.load("img/Rocks.png").convert_alpha()
pOil = pygame.image.load("img/oil.png").convert_alpha()
pSpikes = pygame.image.load("img/roadSpikes.png").convert_alpha()

#Boosts
pJerryCan = pygame.image.load("img/jerrycan.png").convert_alpha()
pBoost = pygame.image.load("img/booster.png").convert_alpha()

#Sounds
sBackgroundMusic = pygame.mixer.music.load("sounds/backgroundmusic.wav")
sCrash = pygame.mixer.Sound("sounds/CRASH.wav")
sBoost = pygame.mixer.Sound("sounds/BoostCollect.wav")
sFuel = pygame.mixer.Sound("sounds/FuelCollect.wav")
sCrash.set_volume(0.5)
sBoost.set_volume(0.5)
sFuel.set_volume(0.5)

#Obstacle arrays
boosts = [pJerryCan, pJerryCan, pBoost] #fuel added twice to increase probability of spawning
obstacles = [pRock, pOil, pSpikes]
spawnedObstacles = []

cRed = pygame.Color("Red")
cYellow = pygame.Color("Yellow")

#Car variables
carPositionX, carPositionY = (x/2)-(carForward.get_width()/2), y-150
carWidth = carForward.get_width()
carHeight = carForward.get_height()
carFuel = 1000

backgroundY = 0
score = 0
yVelocity = 4
yVelocityCurrent = yVelocity
xVelocity = 0
BoostVelocity = 0
boostTimer = 0
fuelDec = 0.5
fuelDecCurrent = fuelDec

RunGame = True
isMiddle = False

timer = Manager()
timer.add_operation(spawn_obstacle, 1.0, [obstacles]) #starts a thread for adding obstacles
timer.add_operation(spawn_obstacle, 2.3, [boosts]) #starts a thread for adding boosts (fuel and booster)

pygame.mixer.music.play(-1)
#-------------------Game Loop---------------------
while RunGame:  
        backgroundY += yVelocity+BoostVelocity
        score += 2.5
        carFuel -= fuelDec
        
        #makes background move perpetually
        surface.blit(pBackground,(0,backgroundY%y))
        surface.blit(pBackground,(0,backgroundY%y-y))
        
        fps.tick(120)
        
        #UI
        display_text(score,10,10,"Score: ")
        display_text(yVelocity,10,30, "Speed: ")
        display_text("",178,12, "Fuel:")
        display_text("",176,42, "Boost:")
        
        #Car rendering depending on direction
        if xVelocity > 0:
                surface.blit(carRight, (carPositionX,carPositionY))
        elif xVelocity < 0:
                surface.blit(carLeft, (carPositionX,carPositionY))
        elif boostTimer > 0 and xVelocity == 0:
                surface.blit(carBoost, (carPositionX, carPositionY))
        else:                           
                surface.blit(carForward, (carPositionX,carPositionY))
        
        #Flag to make car stop moving at the center to prevent moving between all lanes at once
        if carPositionX == 214:
                isMiddle = True 
                
        #Assigning tasks to keys        
        for event in pygame.event.get():
                if event.type == QUIT:
                        RunGame = False
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                                xVelocity = 15
                                isMiddle = False
                        elif event.key == pygame.K_LEFT:
                                xVelocity = -15
                                isMiddle = False        
        #Car movement   
        if isMiddle == False and xVelocity > 0 and carPositionX < x-110 or isMiddle == False and xVelocity < 0 and carPositionX > x-425:
                carPositionX += xVelocity
        else:
                xVelocity = 0
        
        #Collision detection
        #Different actions based on the type of obstacle
        for o in spawnedObstacles:
                o.y+=yVelocity+BoostVelocity #adds to y property of obstacle object
                obsX = (40+165*o.numLane) 
                if obsX - carWidth < carPositionX < obsX + o.image.get_width() and o.y - carHeight < carPositionY < o.y + o.image.get_height(): #checking for collision using dimensions of car and obstacle
                        if o.image == pJerryCan: #fuel can
                                if (carFuel+250) < 1000:
                                        carFuel += 50 + 50*yVelocityCurrent #adds more according to current speed
                                else:
                                        carFuel = 1000 #max is 1000 fuel
                                sFuel.play(loops=0, maxtime=0, fade_ms=0)       
                        elif o.image == pBoost: #boost
                                sBoost.play(loops=0, maxtime=0, fade_ms=0)
                                boostTimer = 200 + 10*yVelocityCurrent #lasts longer as game gets harder
                        #collision with obstacles
                        elif o.image in obstacles and (carFuel-250) > 0 and carFuel > 0:        
                                sCrash.play(loops=0, maxtime=0, fade_ms=0)
                                carFuel -= 50 + 50*yVelocityCurrent #loses more fuel as game gets more difficult
                        elif o.image in obstacles and (carFuel-250) < 0 and carFuel > 0:
                                sCrash.play(loops=0, maxtime=0, fade_ms=0)
                                carFuel = 0 #minimum is 0
                        elif o.image in obstacles and carFuel == 0:
                                RunGame = False #game ends if fuel is 0 and player collides into obstacle
                        spawnedObstacles.remove(o)              
                if o.y > 800:
                        spawnedObstacles.remove(o)
                else:
                        surface.blit(o.image, ((40+165*o.numLane),o.y))
        
        #Boost and fuel bars
        pygame.draw.line(surface, cRed, (250,20), (250+(carFuel/5),20),5)
        pygame.draw.line(surface, cYellow, (250,50), (250+(boostTimer/5),50),5)
        
        #difficulty, increases speed/fuel consumption as score increases
        if score%2500==0 and yVelocity < 7:
                yVelocityCurrent += 0.5
                yVelocity = yVelocityCurrent #necessary to return yVelocity back to normal when fuel is collected after a depleted state
        if score%3000==0 and fuelDec <= 1.0:
                fuelDecCurrent += 0.1
                fuelDec = fuelDecCurrent
        
        #Boost  
        if boostTimer >= 0:
                BoostVelocity = 2
                boostTimer -= 1
        else: 
                BoostVelocity = 0
        
        #Decrease yVelocity slowly after fuel is completely depleted
        #If fuel is collected during this time, game resumes
        #Once yVelocity is 0, end the game      
        if carFuel <= 0 and yVelocity >= 0:
                fuelDec = 0
                yVelocity -= 0.01
        elif carFuel > 0 and yVelocity > 0:
                yVelocity = yVelocityCurrent
                fuelDec = fuelDecCurrent
        elif yVelocity <= 0:
                RunGame = False 

        pygame.display.update()
