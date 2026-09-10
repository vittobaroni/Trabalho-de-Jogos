import pygame
import math
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler
from bullet import StraightBullet 

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.lives = 3
        self.state = NormalState(self)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def action_1(self):
        self.state.action_1()

    def action_2(self):
        self.state.action_2()

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

    def take_damage(self):
        if not isinstance(self.state, DeadState) and not isinstance(self.state, InvincibleState):
            self.lives -= 1
            if self.lives > 0:
                print(f"voce foi atingido, {self.lives} vidas restantes")
                self.change_state(InvincibleState)
            else:
                print("ficou sem vidas, voce morreu :(")
                self.change_state(DeadState)

class PlayerState(ABC):
    sprite = pygame.Surface((32, 32))

    def __init__(self, player):
        self.P = player

    def draw(self, screen):
        screen.blit(self.sprite, self.P.pos)

    def delete(self):
        pass 

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def action_1(self):
        EventHandler().notify("RestartGame",None)

    @abstractmethod
    def action_2(self):
        pass


class NormalState(PlayerState):
    sprite = colored_sprite((0, 255, 0))

    def __init__(self, player):
        super().__init__(player)
        self.velocidade = 4

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        x, y = self.P.pos
        
        if teclas[pygame.K_w] or teclas[pygame.K_UP]: y -= self.velocidade * dt
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]: y += self.velocidade * dt
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]: x -= self.velocidade * dt
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: x += self.velocidade * dt
        
        self.P.pos = (x, y)
    
    def action_1(self):
        # Tiro na direção do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        dx = mouse_x - self.P.pos[0]
        dy = mouse_y - self.P.pos[1]
        
        angulo = math.degrees(math.atan2(dy, dx))
        
        nova_bala = StraightBullet(pos=self.P.pos, angle=angulo, life_time=120)
        
        EventHandler().notify("AddObj", nova_bala)

    def action_2(self):
        print("futuro coisa de invencibilidade aqui e tal!")

class DeadState(PlayerState):
    sprite = colored_sprite((255, 0, 0))

    def __init__(self, player):
        super().__init__(player)

    def update(self, dt):
        pass 
        
    def action_1(self):
        
        EventHandler().notify("RestartGame", None)
        
    def action_2(self):
        pass

class InvincibleState(PlayerState):
    sprite = colored_sprite((0, 150, 255)) # Fica AZUL para mostrar que está invencível

    def __init__(self, player):
        super().__init__(player)
        self.velocidade = 4
        self.timer = 0
        self.duration = 120 
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.P.change_state(NormalState)
            return

        teclas = pygame.key.get_pressed()
        x, y = self.P.pos
        if teclas[pygame.K_w] or teclas[pygame.K_UP]: y -= self.velocidade * dt
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]: y += self.velocidade * dt
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]: x -= self.velocidade * dt
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: x += self.velocidade * dt
        self.P.pos = (x, y)

    def action_1(self):
       
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.P.pos[0]
        dy = mouse_y - self.P.pos[1]
        angulo = math.degrees(math.atan2(dy, dx))
        nova_bala = StraightBullet(pos=self.P.pos, angle=angulo, life_time=120)
        EventHandler().notify("AddObj", nova_bala)

    def action_2(self):
        pass
