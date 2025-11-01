from pygame import *
from random import randint

mixer.init()
mixer.music.load('angelical-pad-143276.mp3')
mixer.music.play()

los_alien_se_rinden = mixer.Sound('ganaste.mp3')
los_aliens_te_han_matado = mixer.Sound('perdiste.mp3')
balas_pero_sonoras = mixer.Sound('sonidodelaser.mp3')    
font.init()
font1 = font.Font(None , 36)
font2 = font.Font(None, 40)
fldsmdfr = font2.render('LOS GATOS ALIEN BEBE SE RINDEN ANTE TI', True , (0, 145, 131))
no_fldsmdfr = font2.render('LOS GATOS ALIEN BEBE TE HAN GANADO', True , (145, 26, 0))                   
imagen_bala = 'bala_tecnologica.png'
imagen_fondo ='fondo.jpeg'
imagen_jugador = 'descarga.png'
imagen_enemigo =  'a.jpeg'

lost = 0 
score = 0 
al_v =  500  

an_v =  700  

display.set_caption('tirador')
ventana = display.set_mode((an_v,al_v ))
fondo = transform.scale(image.load(imagen_fondo),(an_v , al_v ))

class gamesprite(sprite.Sprite):
    
    def __init__(self, player_image, player_x , player_y, size_x , size_y , player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
   
    def reset(self):
        ventana.blit(self.image,(self.rect.x, self.rect.y))

class Player(gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < an_v - 80:
            self.rect.x += self.speed
    def fire(self):
        bala = Bala(imagen_bala,self.rect.centerx, self.rect.top , 40 , 50 , 20)
        balas.add(bala)



class enemy(gamesprite):

    def update(self):
        self.rect.y += self.speed
        global lost



        if self.rect.y > al_v:
            self.rect.x = randint(80, an_v - 80)
            self.rect.y = 0
            lost += 1 

class Bala(gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()
    
    






jugador = Player(imagen_jugador, 5 , al_v - 100, 80 , 100 , 7)
extraterestes = sprite.Group()
for i in range(1,  6):
    extraterrestre = enemy(imagen_enemigo,randint(80 , an_v - 80), -0 , 150 , 160  , randint(1,3))
    extraterestes.add(extraterrestre)

balas = sprite.Group()

finish = False
run = True

while run : 
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                jugador.fire()
                balas_pero_sonoras.play()
    if  not finish:
        ventana.blit(fondo,(0,0))
        
        text = font1.render('puntos: ' + str(score), 1 ,(158, 5, 5))
        ventana.blit(text, (10,20))


        text_lose = font1.render('fallos: ' + str(lost), 1 ,(158, 5, 5))
        ventana.blit(text_lose, (10,50))
        

        balas.update()
        balas.draw(ventana)
        jugador.update()
        extraterestes.update()
        extraterestes.draw(ventana)
        jugador.reset()
        colision = sprite.groupcollide(extraterestes , balas , True , True)
        for c in colision :
            score += 1
            extraterrestre = enemy(imagen_enemigo,randint(80 , an_v - 80), -40 , 80 , 50  , randint(1,3))
            extraterestes.add(extraterrestre)

        if sprite.spritecollide(jugador , extraterestes ,False) or lost >= 3:
            los_aliens_te_han_matado.play()
            finish = True
            ventana.blit(no_fldsmdfr,(30,200))
             
        if score >= 50:
            finish = True
            los_alien_se_rinden.play()
            ventana.blit(fldsmdfr,(30,200 ))

        display.update()
    time.delay(50)

