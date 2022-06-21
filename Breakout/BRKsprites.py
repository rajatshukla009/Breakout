import pygame
from BRKsettings import *
from random import choice, randint


class Upgrade(pygame.sprite.Sprite):
    def __init__(self,position,upTYPE,groups):
        super().__init__(groups)
        self.upTYPE = upTYPE
        self.image = pygame.image.load(f"upgrades/{upTYPE}.png").convert_alpha()
        self.rect = self.image.get_rect(midtop = position)

        self.position = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def update(self, dt):
        self.position.y += self.speed * dt
        self.rect.y = round(self.position.y)

        if self.rect.top > windowHIEGHT + 100:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self,position,surface,groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(midbottom = position)

        self.position = pygame.math.Vector2(self.rect.topleft)
        self.speed  = 300

    def update(self,dt):
        self.position.y -= self.speed*dt
        self.rect.y = round(self.position.y)

        if self.rect.bottom <= -100:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups,surfacemaker):
        super().__init__(groups)

        self.displaySURF = pygame.display.get_surface()
        self.surfacemaker = surfacemaker
        self.image = surfacemaker.getSURF(block_type="player",size=(windowWIDTH//10,windowHIEGHT//20))

        self.rect = self.image.get_rect(midbottom=(windowWIDTH // 2, windowHIEGHT - 20))
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

        self.hearts = 4

        self.laserAMT = 0
        self.laserSURF = pygame.image.load("other/laser.png").convert_alpha()
        self.laserRECTS = []

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def screenCONST(self):
        if self.rect.right > windowWIDTH:
            self.rect.right = windowWIDTH
            self.position.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x

    def upgrade(self,upType):
        if upType == "speed":
            self.speed += 50

        if upType == "heart":
            self.hearts += 1

        if upType == "size":
            newWIDTH = self.rect.width *1.1
            self.image = self.surfacemaker.getSURF("player",(newWIDTH,self.rect.height))
            self.rect = self.image.get_rect(center = self.rect.center)
            self.position.x = self.rect.x

        if upType == "laser":
            self.laserAMT += 1

    def displayLASERS(self):
        self.laserRECTS = []
        if self.laserAMT > 0:
            dividerLEN = self.rect.width/(self.laserAMT + 1)
            for i in range(self.laserAMT):
                x = self.rect.left + dividerLEN*(i+1)
                laserRECT = self.laserSURF.get_rect(midbottom = (x,self.rect.top))
                self.laserRECTS.append(laserRECT)

            for laserRECT in self.laserRECTS:
                self.displaySURF.blit(self.laserSURF,laserRECT)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.position.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.position.x)
        self.screenCONST()
        self.displayLASERS()


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player,blocks):
        super().__init__(groups)

        self.player = player
        self.blocks = blocks

        self.image = pygame.image.load("other/ball.png").convert_alpha()

        self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2((choice((1, -1)), -1))
        self.speed = 400

        self.active = False

        self.impactSOND = pygame.mixer.Sound("sounds/impact.wav")
        self.impactSOND.set_volume(0.1)

        self.failSOND = pygame.mixer.Sound("sounds/fail.wav")
        self.failSOND.set_volume(0.1)

    def windowCOLL(self, direction):
        if direction == "horizontal":
            if self.rect.left < 0:
                self.rect.left = 0
                self.position.x = self.rect.x
                self.direction.x *= -1

            if self.rect.right > windowWIDTH:
                self.rect.right = windowWIDTH
                self.position.x = self.rect.x
                self.direction.x *= -1

        if direction == "vertical":
            if self.rect.top < 0:
                self.rect.top = 0
                self.position.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom > windowHIEGHT:
                self.active = False
                self.direction.y = -1
                self.player.hearts -= 1
                self.failSOND.play()

    def collisions(self,direction):
        overlapSPRITES = pygame.sprite.spritecollide(self,self.blocks,False)
        if self.rect.colliderect(self.player.rect):
            overlapSPRITES.append(self.player)

        if overlapSPRITES:
            if direction == "horizontal":
                for sprite in overlapSPRITES:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.position.x = self.rect.x
                        self.direction.x *= -1
                        self.impactSOND.play()

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.position.x = self.rect.x
                        self.direction.x *= -1
                        self.impactSOND.play()

                    if getattr(sprite,"health",None):
                        sprite.getDAMAGE(1)

            if direction == "vertical":
                for sprite in overlapSPRITES:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.position.y = self.rect.y
                        self.direction.y *= -1
                        self.impactSOND.play()

                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.position.y = self.rect.y
                        self.direction.y *= -1
                        self.impactSOND.play()

                    if getattr(sprite,"health",None):
                        sprite.getDAMAGE(1)

    def update(self, dt):
        if self.active:

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.old_rect = self.rect.copy()

            # horizontal collision and movement
            self.position.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.position.x)
            self.collisions("horizontal")
            self.windowCOLL("horizontal")

            # vertical movement and collisions
            self.position.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.position.y)
            self.collisions("vertical")
            self.windowCOLL("vertical")
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.position = pygame.math.Vector2(self.rect.topleft)


class Block(pygame.sprite.Sprite):
    def __init__(self,block_type,position,groups,surfacemaker,createUP):

        super().__init__(groups)
        self.surfacemaker = surfacemaker
        self.image = self.surfacemaker.getSURF(colorLEGEND[block_type],(blockWIDTH,blockHEIGHT))
        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()

        self.health = int(block_type)

        self.createUP = createUP

    def getDAMAGE(self,amount):
        self.health -= amount

        if self.health > 0:
            self.image = self.surfacemaker.getSURF(colorLEGEND[str(self.health)],(blockWIDTH,blockHEIGHT))
        else:
            if randint(0,10) < 4:
                self.createUP(self.rect.center)
            self.kill()