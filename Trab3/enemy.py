import pygame
import math
import random # usei pra colocar novos inimigos na tela
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler

class Enemy:
    def __init__(self, pos, target_player):
        self.pos = pos
        self.target = target_player
        self.state = ChasingState(self)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)
        
    def take_damage(self):
        if not isinstance(self.state, StunnedState):
            self.change_state(StunnedState)

class EnemyState(ABC):
    sprite = pygame.Surface((32, 32))

    def __init__(self, enemy):
        self.E = enemy

    def draw(self, screen):
        screen.blit(self.sprite, self.E.pos)

    def delete(self):
        pass 

    @abstractmethod
    def update(self, dt):
        pass

class ChasingState(EnemyState):
    sprite = colored_sprite((255, 200, 0)) 

    def __init__(self, enemy):
        super().__init__(enemy)
        self.velocidade = 2 

    def update(self, dt):
        alvo_x, alvo_y = self.E.target.pos
        meu_x, meu_y = self.E.pos
        
        dx = alvo_x - meu_x
        dy = alvo_y - meu_y
        distancia = math.hypot(dx, dy)
        
        if distancia > 0:
            meu_x += (dx / distancia) * self.velocidade * dt
            meu_y += (dy / distancia) * self.velocidade * dt
            self.E.pos = (meu_x, meu_y)

class StunnedState(EnemyState):
    # Fica cinza
    sprite = colored_sprite((150, 150, 150)) 

    def __init__(self, enemy):
        super().__init__(enemy)
        self.timer = 0 

    def update(self, dt):
        self.timer += dt
        if self.timer > 30:
            EventHandler().notify("DestroyObj", self.E)

class EnemySpawner:
    def __init__(self, target_player):
        self.target = target_player
        self.timer = 0
        self.spawn_rate = 120 

    def update(self, dt):
        self.timer += dt
        
        # bateu o limite do cronometro, aparece um novo inimigo
        if self.timer >= self.spawn_rate:
            self.timer = 0
            
            x = random.choice([-50, 850]) 
            y = random.randint(-50, 650)
            
            novo_inimigo = Enemy((x, y), self.target)
            EventHandler().notify("AddObj", novo_inimigo)

    def draw(self, screen):
        pass 