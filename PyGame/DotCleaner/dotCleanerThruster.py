import pygame
import time
import random
import math
pygame.init()

clock = pygame.time.Clock()

blue = (50,153,213)
red = (213,50,80)
yellow = (255,255,102)
green = (0,255,0)
green2 = (50,210,50)
white = (255,255,255)
black = (0,0,0)


disW = 800
disH = 800
dis = pygame.display.set_mode((disW, disH))
pygame.display.set_caption('Test Space')




def gameLoop():

    #GreenCircleVariables
    moveSpeed1 = 20
    x1_change = 0
    y1_change = 0
    x1 = disW/2
    y1 = disH/2

    #TargetVariables
    xTar = 0
    yTar = 0
    targetList = []
    numberOfTargets = 10

    #RedCircleVariables
    moveSpeed2 = 10
    x2 = disW/2
    y2 = disH/2
    x2_change = 0
    y2_change = 0
    x2_rate = 0
    y2_rate = 0
    trail = []
    trailLen = 50

    
    running = True
    targetPlaced = False

    while running == True:
        
        #Kill switch
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Green Dot        
        #Keys
            if event.type == pygame.KEYDOWN:
                #Movement
                if event.key == pygame.K_LEFT:
                    if x1_change >= 0:
                        x1_change += -moveSpeed1
                    else:
                        y1_change = 0
                if event.key == pygame.K_RIGHT:
                    if x1_change <= 0:
                        x1_change += moveSpeed1
                    else:
                        y1_change = 0
                if event.key == pygame.K_UP:
                    if y1_change >= 0:
                        y1_change += -moveSpeed1
                    else:
                        x1_change = 0
                if event.key == pygame.K_DOWN:
                    if y1_change <= 0:
                        y1_change += moveSpeed1
                    else:
                        x1_change = 0
                if event.key == pygame.K_SPACE:
                    xTarg = x1
                    yTarg = y1
                    targetPlaced = True
                    #print("Placing")
                    tarPos = []
                    tarPos.append(xTarg)
                    tarPos.append(yTarg)
                    targetList.append(tarPos)
        x1 += x1_change
        y1 += y1_change

        #Wall collisions
        if x1 >= disW:
            x1 = 0
        if x1 < 0:
            x1 = disW
        if y1 >= disH:
            y1 = 0
        if y1 <0:
            y1 = disH

        #TargetSelection
        tarDistance = 10000
        newTarDistance = 10000
        xTarDistance = 0
        yTarDistance = 0
        chosenTarget = 0
        if len(targetList) > 0:
            for x in targetList:
                xTarDistance = abs(x[0] - x2)
                yTarDistance = abs(x[1] - y2)
                newTarDistance = math.sqrt((xTarDistance ** 2)+(yTarDistance ** 2))
                if newTarDistance < tarDistance:
                    tarDistance = newTarDistance
                    xTar = x[0]
                    yTar = x[1]
                    chosenTarget = targetList.index(x)
        else:
            targetPlaced = False
        #RedCircleMovement
        xThrust = 1
        yThrust = 2
        if targetPlaced == True:
            if (xTar-20 < x2 < xTar+20) and (yTar-20 < y2 < yTar+20):
            #if (x2 == xTar) and (y2 == yTar):
                #print (chosenTarget)
                del targetList[chosenTarget]
            
            if x2 > xTar:
                x2_change = -xThrust
            if x2 < xTar:
                x2_change = xThrust
            if x2 == xTar:
                x2_change = 0
                
            if y2 > yTar:
                y2_change = -yThrust
            if y2 < yTar:
                y2_change = 0
            if y2 == yTar:
                y2_change = 0
        else:
            x2_change = 0
            y2_change = 0
            
        if x2_rate < -5:
            x2_rate += 1
        elif x2_rate > 5:
            x2_rate += -1
        else:
            x2_rate += x2_change
        if x2 < 10:
            x2_rate = 1
        if x2 > disW -10:
            x2_rate = -1
        x2 += x2_rate

        if y2_rate > -10:
            y2_rate += y2_change
        if  y2_rate <  10:
            y2_rate += 1
        if y2 > disH -10:
            y2_rate = -5
        #print(y2_rate, x2_rate)
        y2 += y2_rate



        #Trail
        if len(trail)>trailLen:
            trail.pop(0)
        trail.append([x2, y2])
        
        
        #Base
        dis.fill(blue)

        #Walls
        pygame.draw.rect(dis, yellow, [0,0,disW,5])    #top
        pygame.draw.rect(dis, yellow, [0,0,5,disH])    #left
        pygame.draw.rect(dis, yellow, [disW-5,0,5,disH]) #right
        pygame.draw.rect(dis, yellow, [0,disH-5,disW,5]) #bottom

        #Target
        #print(targetPlaced)
        if targetPlaced == True:
            for x in targetList:
                pygame.draw.circle(dis, green2, [x[0], x[1]], 20, 0)

        #GreenCircleDraw
        pygame.draw.circle(dis, green, [x1, y1], 20, 0)

        #RedCircleDraw
        pygame.draw.circle(dis, red, [x2, y2], 10, 0)

        #RedTrailDraw
        for i in range(len(trail)):
            trailShade = ((213*(i/trailLen)),50,80)
            pygame.draw.circle(dis, trailShade, trail[i], (10*(i/trailLen)), 0)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    quit()

gameLoop()
