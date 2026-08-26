import pygame
from grid import Grid

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Eat the Duck")


font = pygame.font.Font(None, 36)
font_go = pygame.font.Font(None, 72)


clock = pygame.time.Clock()

grid_size = (20, 15)


meu_grid = Grid(x=0, y=0, sprites=[], grid_size=grid_size)
objects = [meu_grid]

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: # Botão esquerdo
                pos_mouse = pygame.mouse.get_pos()
                meu_grid.processar_clique(pos_mouse)

        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            else:
                
                meu_grid.processar_tecla(event.key)

    
    for obj in objects:
        obj.update(1)

    
    screen.fill((30, 30, 30))

    for obj in objects:
        obj.draw(screen)

    
    texto_pontos = font.render(f"Pontos: {meu_grid.pontos}", True, (255, 255, 255))
    screen.blit(texto_pontos, (10, 10))
    
    if meu_grid.game_over:
        texto_gameover = font_go.render("GAME OVER", True, (255, 50, 50))
        screen.blit(texto_gameover, (WIDTH//2 - texto_gameover.get_width()//2, HEIGHT//2 - 50))

    pygame.display.flip()
    
    
    clock.tick(8)