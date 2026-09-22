# TRABALHO DE GOLF !!

# OBS : tive que fazer as imagens no paint, pois nenhuma me agradou o suficiente
# e não possuo os dotes artisticos necessários, então apenas ignore se algo ficar ruim

#OBS2 --> para fazer a mudança das posições 

# COMO JOGAR : Arraste a bola com o mouse para mostrar a direção dela e aperte R para reiniciar o jogo

# Atualizações futuras --> Gostaria que tivesse algo como um randomizer de posição dos objetos, mas não sei fazer no momento



import pygame
from abc import ABC, abstractmethod
from collision import Collider

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# só pra mostrar o "TACADAS : " 

pygame.font.init()
fonte = pygame.font.SysFont("Arial", 24)

class obj(ABC):
    def __init__(self, sprite, coord):
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(sprite)
        self.coord = list(coord)

    def draw(self, screen):
        screen.blit(self.sprite, self.coord) 

    @abstractmethod
    def lidar_colisao(self, outro_obj): pass
    @abstractmethod
    def lidar_bola(self, bola): pass
    @abstractmethod
    def lidar_parede(self, parede): pass
    @abstractmethod
    def lidar_zona(self, zona): pass
    @abstractmethod
    def lidar_buraco(self, buraco): pass 

class Bola(obj):
    def __init__(self, sprite, coord):
        super().__init__(sprite, coord)
        self.vx = 0
        self.vy = 0
        self.atrito = 0.98

    def update(self):
        self.coord[0] += self.vx
        self.coord[1] += self.vy
        self.vx *= self.atrito
        self.vy *= self.atrito
        
        if abs(self.vx) < 0.1: self.vx = 0
        if abs(self.vy) < 0.1: self.vy = 0

    def lidar_colisao(self, outro_obj):
        # avisa o jogo que a bola caiu no buraco
        return Collider().lidar_bola(self, outro_obj)

    def lidar_bola(self, bola): pass 
    def lidar_parede(self, parede): Collider().colisao_bola_parede(self, parede)
    def lidar_zona(self, zona): Collider().colisao_bola_zona(self, zona)
    def lidar_buraco(self, buraco): return Collider().colisao_bola_buraco(self, buraco)

class Parede(obj):
    def lidar_colisao(self, outro_obj): Collider().lidar_parede(self, outro_obj)
    def lidar_bola(self, bola): Collider().colisao_bola_parede(bola, self)
    def lidar_parede(self, parede): pass
    def lidar_zona(self, zona): pass
    def lidar_buraco(self, buraco): pass

class Zona(obj):
    def lidar_colisao(self, outro_obj): Collider().lidar_zona(self, outro_obj)
    def lidar_bola(self, bola): Collider().colisao_bola_zona(bola, self)
    def lidar_parede(self, parede): pass
    def lidar_zona(self, zona): pass
    def lidar_buraco(self, buraco): pass

class Buraco(obj):
    def lidar_colisao(self, outro_obj): return Collider().lidar_buraco(self, outro_obj)
    def lidar_bola(self, bola): return Collider().colisao_bola_buraco(bola, self)
    def lidar_parede(self, parede): pass
    def lidar_zona(self, zona): pass
    def lidar_buraco(self, buraco): pass

# Cria as entidades (certifica-te que as imagens se chamam assim)
bola = Bola(pygame.image.load("bola.png").convert_alpha(), (400, 500))
parede = Parede(pygame.image.load("parede.png").convert_alpha(), (100, 200))
areia1 = areia = Zona(pygame.image.load("areia.png").convert_alpha(), (500, 400))
areia2 = areia = Zona(pygame.image.load("areia.png").convert_alpha(), (500, 200))
buraco = Buraco(pygame.image.load("buraco.png").convert_alpha(), (600, 100))

objects = [bola, parede, areia1, areia2, buraco]

tacadas = 0
vitoria = False
arrastando = False

running = True

while running:
   ## input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo
                arrastando = True
                pos_inicial_mouse = pygame.mouse.get_pos()
                
        # quando da a tacada

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and arrastando:
                arrastando = False
                pos_final_mouse = pygame.mouse.get_pos()
                
                # só pode dar a tacada se não tiver no buraco e soma +1 a cada tacada que não entrou ainda
                if not vitoria:
                    dx = pos_inicial_mouse[0] - pos_final_mouse[0]
                    dy = pos_inicial_mouse[1] - pos_final_mouse[1]
                    
                    bola.vx = dx * 0.05
                    bola.vy = dy * 0.05
                    tacadas += 1 

        # verifica se alguma tecla foi pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Pressionar a tecla "R"
                # Repõe o estado inicial do jogo
                bola.coord = [400, 500] # Usa as coordenadas iniciais da tua bola
                bola.vx = 0
                bola.vy = 0
                tacadas = 0
                vitoria = False
                arrastando = False

    bola.update()

    #colisoes com a parede e a areia

    for o in objects:
        if o != bola:
            offset_x = int(o.coord[0] - bola.coord[0])
            offset_y = int(o.coord[1] - bola.coord[1])
            
            if bola.mask.overlap(o.mask, (offset_x, offset_y)):
                resultado = Collider().lidar_colisao(bola, o)
                
                if isinstance(o, Buraco) and resultado:
                    vitoria = True

    screen.fill((30,30,30))

    # desenho da linha pra bater na bola
    if arrastando and not vitoria:
        pos_atual_mouse = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), bola.coord, pos_atual_mouse, 2)

    for o in objects:
        o.draw(screen)


    texto_tacadas = fonte.render(f"Tacadas: {tacadas}", True, (255, 255, 255))
    screen.blit(texto_tacadas, (10, 10))

    if vitoria:
        texto_vitoria = fonte.render("acertou !", True, (0, 255, 0))
        screen.blit(texto_vitoria, (250, 250))

    pygame.display.flip()
    clock.tick(60)