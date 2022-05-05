
from pygame import *

from random import randint

from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
lost = 0
win1 = 0

class GameSprite(sprite.Sprite):
    def __init__(self,player_image1,x,y,speed,e,e1,pp):
        super().__init__()
        self.image = transform.scale(image.load(player_image1),(e,e1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.f = 0
        self.pp = pp
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):    
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 715:
            self.rect.x += self.speed
    def fire(self):
        bullets.add(Bullet('bullet.png',self.rect.centerx,self.rect.top,4,19,19,0))

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y >= 600:
            self.rect.y = 0
            self.rect.x = randint(15,745)
            if self.pp == 1:
                lost += 1
        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        if self.rect.y < -0:
            self.kill()
        else:
            self.rect.y -= self.speed

window = display.set_mode((800,600))
display.set_caption('GALAXY')
background = transform.scale(image.load('galaxy.jpg'),(800,600))

player = Player('rocket.png',0,495,6,95,95,0)
 
monsters = sprite.Group()

for i in range(3):
    monsters.add(Enemy('ufo.png',randint(15,745),0,1,85,85,1))

asteroids = sprite.Group()

for k in range(1):
    asteroids.add(Enemy('asteroid.png',randint(15,745),0,2,65,65,0))

bullets = sprite.Group()

font.init()
font1 = font.Font(None,30)
win = font1.render('VICTORY!',True,(255,255,255))
lose = font1.render('LOSE!',True,(255,255,255))

www = 2
game = True
finish = False
clock = time.Clock()
FPS = 60
flag = False
count = 0
time1 = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if flag == False and count < 5:
                    player.fire()
                    count += 1
                if flag == False and count >= 5:
                    flag = True
                    time1 = timer()
    if not finish:
        window.blit(background,(0,0))
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        player.reset()
        player.update()
        win2 = font1.render('Счет: '+str(win1),True,(255,255,255))
        window.blit(win2,(3,6))
        lost1 = font1.render('Пропущено: '+str(lost),True,(255,255,255))
        window.blit(lost1,(3,40))
        clock.tick(FPS)
        if flag == True:
            time2 = timer()
            if time2-time1 < 3:
                font.init()
                font2 = font.Font(None,30)
                r = font2.render('Wait, reload...',True,(150,0,0))
                window.blit(r,(260,550))
            elif time2-time1 >= 3:
                count = 0
                flag = False
        sprite.groupcollide(asteroids,bullets,False,True)
        if sprite.spritecollide(player,asteroids,False):
            finish = True
            font.init()
            font = font.Font(None,90)
            lose = font.render('LOSE!',True,(255,255,255))
            window.blit(lose,(270,220))
        if sprite.groupcollide(monsters,bullets,True,True):
            win1 += 1
            monsters.add(Enemy('ufo.png',randint(15,745),0,1,85,85,1))        
        if  lost >= 5:
            finish = True
            font.init()
            font = font.Font(None,90)
            lose = font.render('LOSE!',True,(255,255,255))
            window.blit(lose,(270,220))
        if win1 == 20:
            font.init()
            font1 = font.Font(None,90)
            win = font1.render('VICTORY!',True,(255,255,255))
            finish = True
            window.blit(win,(270,220))
    display.update()