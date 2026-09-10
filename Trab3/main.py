#o jogo é um joguinho de tiro, que aparece varias hordas de bolinhas laranjas ( inimigos ) que vão de caçar constantemente, e voce deve matá-las
# COMO JOGAR : WASD ou setas para mover, espaço para atirar e recomeçar o jogo, e o mouse para mirar para onde você quer mirar 
# gostaria de adicionar uma parte para aumentar a velocidade dos inimigos sem se tornar muito quebrado, mas vai ficar para futuramente, já que estou muito ocupado com a uff agora
# OBS : A pasta de imagens do pato não foram usadas, mas elas estão aí pois dei um clone no seu repositorio e atualizei o trab1,2 e 3 em meu próprio repositório, com um fork para o seu

import pygame
from player import Player, DeadState, NormalState, InvincibleState
from enemy import Enemy, EnemySpawner, StunnedState
from util import EventHandler, circle_collistiion

# inicialização
pygame.init()
WIDTH = 800; HEIGHT = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

# Criação das Entidades Iniciais
player = Player((50, 50))
gerador = EnemySpawner(target_player=player)

objects = [player, gerador]

# funções auxiliares
def handle_input(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.action_1()
            if event.key == pygame.K_TAB:
                player.action_2()

def remove_obj(obj):
    if obj in objects:
        objects.remove(obj) 

def add_obj(obj):
    if obj not in objects:
        objects.append(obj)


def remove_obj(obj):
    if obj in objects:
        objects.remove(obj) 

def add_obj(obj):
    if obj not in objects:
        objects.append(obj)

def restart_game(data):
    global hitado
    hitado = 0 
    
    objects.clear() 
    
    player.pos = (400, 300)
    player.lives = 3 
    player.change_state(NormalState)
    gerador.timer = 0
    
    objects.append(player)
    objects.append(gerador)
    
    print("\n---o jogo foi reiniciado ---")

# Inscrições de Eventos
EventHandler().subscribe("DestroyObj", remove_obj)
EventHandler().subscribe("AddObj", add_obj)
EventHandler().subscribe("RestartGame", restart_game)

hitado = 0 # contador de inimigos mortos

# loop principal
running = True
while running:

    handle_input(player)

    if not isinstance(player.state, DeadState):
        
        for obj in objects:
            obj.update(1)

        inimigos = [obj for obj in objects if isinstance(obj, Enemy)]
        balas = [obj for obj in objects if hasattr(obj, 'life_time')]
        
        # checa se o tiro acertou o inimigo
        for inimigo in inimigos:
            for bala in balas:
                if circle_collistiion(inimigo.pos, 16, bala.pos, 16):
                    if not isinstance(inimigo.state, StunnedState):
                        hitado = hitado + 1
                        print(f"voce matou {hitado} inimigos !")
                        inimigo.take_damage()
                    if bala in objects:
                        bala.destroy()

        # checa se o inimigo acertou o jogador
        for inimigo in inimigos:
            if circle_collistiion(inimigo.pos, 16, player.pos, 16):
                if not isinstance(inimigo.state, StunnedState):
                    player.take_damage()

    # 3.renderiza a tela
    screen.fill((30,30,30))

    for obj in objects:
        obj.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
