import pygame, sys, time
from BRKsettings import *
from BRKsprites import Player, Ball, Block, Upgrade, Projectile
from BRKsurface import SurfaceMAKER
from random import choice, randint


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((windowWIDTH, windowHIEGHT))
        pygame.display.set_caption("BREAKOUT")

        self.bg = self.createBG()

        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        self.projectile_sprites = pygame.sprite.Group()

        self.surfacemaker = SurfaceMAKER()
        self.player = Player(self.all_sprites, self.surfacemaker)
        self.stageSET()
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites)

        self.heartSURF = pygame.image.load("other/heart.png").convert_alpha()

        self.projectileSURF = pygame.image.load("other/projectile.png").convert_alpha()
        self.canSHOOT = True
        self.shootTIME = 0

        self.crt = CRT()

        self.laser_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.laser_sound.set_volume(0.1)

        self.powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
        self.powerup_sound.set_volume(0.1)

        self.laserhit_sound = pygame.mixer.Sound('sounds/laser_hit.wav')
        self.laserhit_sound.set_volume(0.02)

        self.music = pygame.mixer.Sound('sounds/music.wav')
        self.music.set_volume(0.1)
        self.music.play(loops=-1)

    def createUP(self, position):
        upTYPE = choice(UPGRADES)
        Upgrade(position, upTYPE, [self.all_sprites, self.upgrade_sprites])

    def createBG(self):
        bgORG = pygame.image.load("other/bg.png").convert()
        scaleFACTOR = windowHIEGHT / bgORG.get_height()
        scaleWIDTH = bgORG.get_width() * scaleFACTOR
        scaleHEIGHT = bgORG.get_height() * scaleFACTOR
        scaleBG = pygame.transform.scale(bgORG, (scaleWIDTH, scaleHEIGHT))
        return scaleBG

    def stageSET(self):
        for ROWindex, row in enumerate(blockMAP):
            for COLindex, col in enumerate(row):
                if col != " ":
                    x = COLindex * (blockWIDTH + gapSIZE) + gapSIZE // 2
                    y = topOFF + ROWindex * (blockHEIGHT + gapSIZE) + gapSIZE // 2
                    Block(col, (x, y), [self.all_sprites, self.block_sprites], self.surfacemaker, self.createUP)

    def displayHEARTS(self):
        for i in range(self.player.hearts):
            x = 2 + i * (self.heartSURF.get_width() + 3)
            self.display_surface.blit(self.heartSURF, (x, 4))

    def upgradeCOL(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player, self.upgrade_sprites, True)
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upTYPE)
            self.powerup_sound.play()

    def projectile(self):
        self.laser_sound.play()
        for projectile in self.player.laserRECTS:
            Projectile(projectile.midtop - pygame.math.Vector2(0, 30), self.projectileSURF,
                       [self.all_sprites, self.projectile_sprites])

    def laserTIMER(self):
        if pygame.time.get_ticks() - self.shootTIME >= 650:
            self.canSHOOT = True

    def projblokCOL(self):
        for projectile in self.projectile_sprites:
            overlap_sprites = pygame.sprite.spritecollide(projectile, self.block_sprites, False)
            if overlap_sprites:
                for sprite in overlap_sprites:
                    sprite.getDAMAGE(1)
                projectile.kill()
                self.laserhit_sound.play()

    def run(self):
        lastTime = time.time()

        while True:
            dt = time.time() - lastTime
            lastTime = time.time()

            # GAME LOOP
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.hearts <= 0:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True
                        if self.canSHOOT:
                            self.projectile()
                            self.canSHOOT = False
                            self.shootTIME = pygame.time.get_ticks()

            self.display_surface.blit(self.bg, (0, 0))

            self.all_sprites.update(dt)
            self.upgradeCOL()
            self.laserTIMER()
            self.projblokCOL()

            self.all_sprites.draw(self.display_surface)
            self.displayHEARTS()

            self.crt.draw()

            pygame.display.update()


class CRT:
    def __init__(self):
        vignette = pygame.image.load("other/tv.png").convert_alpha()
        self.scaledVIG = pygame.transform.scale(vignette, (windowWIDTH, windowHIEGHT))
        self.display_SURF = pygame.display.get_surface()
        self.crtLINES()

    def crtLINES(self):
        lineHIEGHT = 4
        lineAMT = windowHIEGHT // lineHIEGHT
        for line in range(lineAMT):
            y = line * lineHIEGHT
            pygame.draw.line(self.scaledVIG, (20, 20, 20), (0, y), (windowWIDTH, y), 1)

    def draw(self):
        self.scaledVIG.set_alpha(randint(50, 90))
        self.display_SURF.blit(self.scaledVIG, (0, 0))


if __name__ == "__main__":
    game = Game()
    game.run()
