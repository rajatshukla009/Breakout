import pygame
from BRKsettings import *
from os import walk

class SurfaceMAKER:
    def __init__(self):
        for index,info in enumerate(walk("blocks")):
            if index == 0:
                self.assets = {color:{} for color in info[1]}
            else:
                for imageNAME in  info[2]:
                    colorTYPE = list(self.assets.keys())[index-1]
                    fullPATH = "blocks" + f'/{colorTYPE}/' + imageNAME
                    surf = pygame.image.load(fullPATH).convert_alpha()
                    self.assets[colorTYPE][imageNAME.split(".")[0]] = surf

    def getSURF(self,block_type,size):
        image = pygame.Surface(size)
        image.set_colorkey((0,0,0))     #removing black bg
        sides = self.assets[block_type]

        image.blit(sides["topleft"],(0,0))
        image.blit(sides["topright"],(size[0]-sides["topright"].get_width(),0))
        image.blit(sides["bottomleft"],(0,size[1]-sides["bottomleft"].get_height()))
        image.blit(sides["bottomright"],(size[0]-sides["bottomright"].get_width(),size[1]-sides["bottomright"].get_height()))

        topWIDTH = size[0] - (sides["topleft"].get_width() + sides["topright"].get_width())
        scaledLEFT = pygame.transform.scale(sides["top"], (topWIDTH, sides["top"].get_height()))
        image.blit(scaledLEFT, (sides["topleft"].get_width(), 0))

        leftHEIGHT = size[1] - (sides["topleft"].get_height() + sides["bottomleft"].get_height())
        scaledLEFT = pygame.transform.scale(sides["left"], (sides["left"].get_width(), leftHEIGHT))
        image.blit(scaledLEFT, (0, sides["topleft"].get_height()))

        rightHEIGHT = size[1] - (sides["topright"].get_height() + sides["bottomright"].get_height())
        scaledRIGHT = pygame.transform.scale(sides["right"], (sides["right"].get_width(), rightHEIGHT))
        image.blit(scaledRIGHT, (size[0]-sides["right"].get_width(), sides["topright"].get_height()))

        bottomWIDTH = size[0] - (sides["bottomleft"].get_width() + sides["bottomright"].get_width())
        scaledBOTTOM = pygame.transform.scale(sides["bottom"], (bottomWIDTH, sides["bottom"].get_height()))
        image.blit(scaledBOTTOM, (sides["bottomleft"].get_width(), size[1]-sides["bottom"].get_height()))

        centerHEIGHT = size[1] - (sides["top"].get_height() + sides["bottom"].get_height())
        centerWIDTH = size[0] - (sides["right"].get_width() + sides["left"].get_width())
        scaledCENTER = pygame.transform.scale(sides["center"],(centerWIDTH,centerHEIGHT))
        image.blit(scaledCENTER,sides["topleft"].get_size())

        return image