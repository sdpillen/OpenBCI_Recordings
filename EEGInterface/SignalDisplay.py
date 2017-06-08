import pygame, sys
from pygame.locals import *
import numpy as np
import time
import math
from random import randrange  # for starfield, random number generator
from random import randint
import scipy.signal as sig


# For debugging NFT; is updated live by visualizer.py.
DISCONNECT = False
LastDISCONNECT = False  # so current and previous states can be compared

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 50

pygame.display.init()
disp = pygame.display.Info()
WINDOWWIDTH = 1020 # I like the screen slightly smaller than window size for ease of portability
WINDOWHEIGHT = disp.current_h*2/3
size = [WINDOWWIDTH, WINDOWHEIGHT]

# The number of pixels in pygame line functions, by default
LINETHICKNESS = 10

# Set up the colours (RGB values)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 127, 255)
VIOLET = (127, 0, 255)

stage = 0




def FeatureDisplay(DISPLAYSURF, channel): #Delineates the sections and labels them

    for x in range (0,5):
        pygame.draw.line(DISPLAYSURF, BLUE, (x*(WINDOWWIDTH-20)/5, WINDOWHEIGHT / 2), (x*(WINDOWWIDTH-20)/5, 0), 1)
    resultSurf = SCOREFONT.render('EEG Trace: Channel ' + str(channel), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH / 2, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS * 2)
    pygame.draw.line(DISPLAYSURF, WHITE, (0, WINDOWHEIGHT / 2), (WINDOWWIDTH, WINDOWHEIGHT / 2), (LINETHICKNESS))


    for x in range (1,9):
        resultSurf = BASICFONT.render(str(x*5), True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.center = (x*(WINDOWWIDTH-20)/8, WINDOWHEIGHT-30)
        pygame.draw.line(DISPLAYSURF, WHITE, (x*(WINDOWWIDTH-20)/8, WINDOWHEIGHT), (x*(WINDOWWIDTH-20)/8, WINDOWHEIGHT-20), 2)
        DISPLAYSURF.blit(resultSurf, resultRect)
    resultSurf = SCOREFONT.render('Spectrum: Channel ' + str(channel), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 25)
    DISPLAYSURF.blit(resultSurf, resultRect)


# Main function
def main():
    pygame.init()
    ##Font information
    global BASICFONT, BASICFONTSIZE
    global SCOREFONTSIZE, SCOREFONT
    global stage
    global StartTime
    global Keypress
    global COLORTOGGLE


    # Initializing the font values
    BASICFONTSIZE = 10
    SCOREFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SCOREFONT = pygame.font.Font('freesansbold.ttf', SCOREFONTSIZE)



    # A flag that smooths exiting from script
    quittingtime = False

    # Initialize the pygame FPS clock
    FPSCLOCK = pygame.time.Clock()

    # Set the size of the screen and label it
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Trace')

    # make mouse cursor visible
    pygame.mouse.set_visible(1)

    #Used for Dummy Data
    dummyindex = time.time() + .1
    Values = np.random.rand(3, 500)*50
    channel = 0
    SizeMultiplier = 1
    SpecMultiplier = 1

    # Let the games (loop) begin!
    while True:
        # Processes game events like quitting or keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quittingtime = True
                break
            # This portion does keypresses
            if event.type == pygame.KEYDOWN:  # press space to terminate pauses between blocs
                if event.key == pygame.K_c:
                    COLORTOGGLE = not COLORTOGGLE
                if event.key == pygame.K_SPACE:
                    print 'space'
                if event.key == pygame.K_LEFT:
                    channel -= 1
                    if channel == -1:
                        channel = 2
                    print channel
                if event.key == pygame.K_RIGHT:
                    channel += 1
                    if channel == 3:
                        channel = 0
                    print channel
                if event.key == pygame.K_UP:
                    SizeMultiplier += .1
                if event.key == pygame.K_DOWN:
                    SizeMultiplier -= .1
                    if SizeMultiplier <= 0:
                        SizeMultiplier = .1
                if event.key == pygame.K_KP_PLUS:
                    SpecMultiplier *= 2
                if event.key == pygame.K_KP_MINUS:
                    SpecMultiplier *= 0.5

        if time.time() > dummyindex:
            dummyindex = dummyindex+.1
            Values = np.concatenate((Values, np.random.rand(3, 500)*50), 1)
            if len(Values[0, :]) > 25000:
                Values = Values[:, -25000:]



        #needed to exit the program gracefully
        if quittingtime == True:
            break

        DISPLAYSURF.fill((0, 0, 0))

        timeseriesindex = 0  # This is each individual point in the series.
        numpairs = []
        BaselinedValues = Values - np.mean(Values)
        for x in BaselinedValues[channel,0::50]:
            timeseriesindex += 2  # The increment of the x axis. higher number means denser trace
            numpairs.append([10 + timeseriesindex, x*SizeMultiplier + WINDOWHEIGHT/4])
        #if COLORTOGGLE:
        #    pygame.draw.lines(DISPLAYSURF, color, False, numpairs, 1)
        #else:
        pygame.draw.lines(DISPLAYSURF, CYAN, False, numpairs, 1)

        if len(Values[0,:]) ==25000:
            freq, density = sig.welch(BaselinedValues[channel, :], fs=5000, nperseg=25000, noverlap=None, scaling='density')
            timeseriesindex = 0
            numpairs = []
            for x in freq[0:205:5]:
                numpairs.append([10 + timeseriesindex*WINDOWWIDTH/40, WINDOWHEIGHT - 10 - density[int(x)]*500*SpecMultiplier])
                timeseriesindex += 1
            numpairs
            pygame.draw.lines(DISPLAYSURF, GREEN, False, numpairs, 2)



        # Draw outline of arena
        FeatureDisplay(DISPLAYSURF, channel)


        pygame.display.update()
        FPSCLOCK.tick(FPS)# Tells the game system that it is not untouched by the inexorable march of time
        pygame.display.update()

if __name__ == '__main__':
    main()

