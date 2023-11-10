#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Inicializamos
pygame.init()

#Cargamos la musica
pygame.mixer.music.load("Sonidos/background.wav")
pygame.mixer.music.play(-1)
 
#Seteamos los FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creamos los colores para los textos
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Variables del tamaño de la pantalla
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#Variables de la velocidad del juego y puntaje
SPEED = 5
SCORE = 0
 
#Creamos las fuentes de texto y los textos a imprimir
font = pygame.font.SysFont("Verdana", 55)
font_small = pygame.font.SysFont("Verdana", 13)
game_over = font.render("GAME OVER", True, WHITE)
text_score = font.render("SCORE:", True, WHITE)

#Agregamos el fondo de pantalla del juego
background = pygame.image.load("Imagenes/AnimatedStreet.png")
 
#Creamos la pantalla
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

#Creamos al enemigo
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Imagenes/Enemy.png")
        self.rect = self.image.get_rect() #hitbox
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) #posicion random
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 10
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
#Creamos al personaje
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Imagenes/Player.png")
        self.rect = self.image.get_rect() #hitbox
        self.rect.center = (160, 520) #posicion central
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0) #moverse a la izq
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0) #moverse a la der
        #podemos hacer lo mismo para arriba y abajo
                   
#Creamos los Sprites        
P1 = Player()
E1 = Enemy()
 
#Creamos los grupos de Sprites
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
#Podemos crear y agregar mas enemigos
 
#Creamos evento de aumento de velocidad
INC_SPEED = pygame.USEREVENT + 1 #generamos un ID unico para el evento
pygame.time.set_timer(INC_SPEED, 2000) #1000 miliseg = 1 seg
 
#Game Loop
while True:
       
    #Ciclos a través de todos los eventos que ocurren  
    for event in pygame.event.get():
        if event.type == INC_SPEED: #Si el evento IND_SPEED se ejecuta
              SPEED += 0.5     
        if event.type == QUIT: #Si el evento QUIT se ejecuta
            pygame.quit() #Cerramos el juego
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10)) #posicionamos el score en la pantalla (arriba a la izq)
 
    #Mueve y redibuja todos los Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 
    #A ejecutar si se produce colisión entre Jugador y Enemigo
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.music.stop()
          pygame.mixer.Sound("Sonidos/crash.wav").play()
          time.sleep(0.5)

          final_scr = font.render(str(SCORE), True, WHITE)
        
          #Pantalla de Game Over
          DISPLAYSURF.fill(BLACK)
          DISPLAYSURF.blit(game_over, (30,250))
          DISPLAYSURF.blit(text_score, (30,300))
          DISPLAYSURF.blit(final_scr, (250,300))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit() #Termina el juego
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)