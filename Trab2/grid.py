# como precisava utilizar imagens, a cobra vai comer o pato disponibilizado na pasta de imagens do trabalho

import pygame
import random
from abc import ABC, abstractmethod


TAMANHO_CELULA = 40
img_vazia = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA))
img_vazia.fill((30, 30, 30))
pygame.draw.rect(img_vazia, (40, 40, 40), (0, 0, TAMANHO_CELULA, TAMANHO_CELULA), 1)


img_maca = pygame.image.load("images/duck/base.png")
img_maca = pygame.transform.scale(img_maca, (TAMANHO_CELULA, TAMANHO_CELULA))

img_corpo = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA), pygame.SRCALPHA)
pygame.draw.rect(img_corpo, (0, 180, 0), (0, 0, TAMANHO_CELULA, TAMANHO_CELULA), border_radius=4)

img_cabeca = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA), pygame.SRCALPHA)
pygame.draw.rect(img_cabeca, (50, 255, 50), (0, 0, TAMANHO_CELULA, TAMANHO_CELULA), border_radius=8)
pygame.draw.circle(img_cabeca, (0, 0, 0), (12, 12), 4)
pygame.draw.circle(img_cabeca, (0, 0, 0), (28, 12), 4)

img_parede = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA))
img_parede.fill((100, 100, 100))
pygame.draw.rect(img_parede, (0, 0, 0), (0, 0, TAMANHO_CELULA, TAMANHO_CELULA), 2)



class obj(ABC):
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(s, (self.x, self.y)) 

    @abstractmethod
    def update(self, dt):
        pass


class Cell(obj):
    def __init__(self, x, y, sprites, grid_size):
        super().__init__(x, y, sprites)
        self.estado = "vazio"

    def set_estado(self, novo_estado, direcao=(0,1)):
        self.estado = novo_estado
        if novo_estado == "vazio":
            self.sprites = [img_vazia]
        elif novo_estado == "maca":
            self.sprites = [img_vazia, img_maca]
        elif novo_estado == "corpo":
            self.sprites = [img_vazia, img_corpo]
        elif novo_estado == "parede":
            self.sprites = [img_parede]
        elif novo_estado == "cabeca":
            angulo = 0
            if direcao == (0, -1): angulo = 90
            elif direcao == (1, 0): angulo = 180
            elif direcao == (0, 1): angulo = 270
            cabeca_rot = pygame.transform.rotate(img_cabeca, angulo)
            self.sprites = [img_vazia, cabeca_rot]

    def update(self, dt):
        pass 


class Grid(obj):
    def __init__(self, x, y, sprites, grid_size):
        super().__init__(x, y, sprites)
        self.colunas, self.linhas = grid_size
        self.tamanho_celula = TAMANHO_CELULA
        
        self.matriz = []
        for l in range(self.linhas):
            linha_celulas = []
            for c in range(self.colunas):
                px = self.x + (c * self.tamanho_celula)
                py = self.y + (l * self.tamanho_celula)
                linha_celulas.append(Cell(px, py, [img_vazia], grid_size))
            self.matriz.append(linha_celulas)

        self.cobra = [(self.linhas//2, self.colunas//2)]
        self.direcao = (0, 1)
        self.obstaculos = []
        self.pontos = 0
        self.game_over = False
        self.maca = self.gerar_maca()
        
        self.atualizar_visual_celulas()

    def gerar_maca(self):
        while True:
            nova = (random.randint(0, self.linhas - 1), random.randint(0, self.colunas - 1))
            if nova not in self.cobra and nova not in self.obstaculos:
                return nova

    def processar_tecla(self, key):
        if key == pygame.K_UP and self.direcao != (1, 0): self.direcao = (-1, 0)
        elif key == pygame.K_DOWN and self.direcao != (-1, 0): self.direcao = (1, 0)
        elif key == pygame.K_LEFT and self.direcao != (0, 1): self.direcao = (0, -1)
        elif key == pygame.K_RIGHT and self.direcao != (0, -1): self.direcao = (0, 1)

    def processar_clique(self, pos_mouse):
        mx, my = pos_mouse
        c = (mx - self.x) // self.tamanho_celula
        l = (my - self.y) // self.tamanho_celula
        
        if 0 <= l < self.linhas and 0 <= c < self.colunas:
            alvo = (l, c)
            if alvo not in self.cobra and alvo != self.maca:
                self.obstaculos.append(alvo)
                self.atualizar_visual_celulas()

    def atualizar_visual_celulas(self):
        for l in range(self.linhas):
            for c in range(self.colunas):
                self.matriz[l][c].set_estado("vazio")
        for obs in self.obstaculos:
            self.matriz[obs[0]][obs[1]].set_estado("parede")
            
        self.matriz[self.maca[0]][self.maca[1]].set_estado("maca")
        
        for i, pedaco in enumerate(self.cobra):
            l, c = pedaco
            if i == 0:
                self.matriz[l][c].set_estado("cabeca", self.direcao)
            else:
                self.matriz[l][c].set_estado("corpo")

    def draw(self, screen):
        for l in range(self.linhas):
            for c in range(self.colunas):
                self.matriz[l][c].draw(screen)

    def update(self, dt):
        if self.game_over: 
            return
        
        l_cabeca, c_cabeca = self.cobra[0]
        nova_l = (l_cabeca + self.direcao[0]) % self.linhas
        nova_c = (c_cabeca + self.direcao[1]) % self.colunas
        nova_cabeca = (nova_l, nova_c)
        
        if nova_cabeca in self.cobra or nova_cabeca in self.obstaculos:
            self.game_over = True
        else:
            self.cobra.insert(0, nova_cabeca)
            if nova_cabeca == self.maca:
                self.pontos += 10
                self.maca = self.gerar_maca()
            else:
                self.cobra.pop()
                
        self.atualizar_visual_celulas()