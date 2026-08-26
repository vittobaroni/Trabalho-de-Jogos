#Este documento vai ser todo comentado e separado em seções, para não haver confusão em atualizações futuras
#não consegui pensar em uma função mais útil pro input do mouse, então está aberto a sugestões futuras e possíveis alterações

import pygame
import sys
import random

pygame.init()
pygame.font.init()

# --- configurações básicas do jogo (pode alterar qualquer um desses de acordo com a preferência) ---
LARGURA = 600
ALTURA = 600
TAMANHO_CELULA = 40
LINHAS = ALTURA // TAMANHO_CELULA
COLUNAS = LARGURA // TAMANHO_CELULA

# -- cores gerais --

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 180, 0)
VERDE_CLARO = (50, 255, 50)
VERMELHO = (220, 0, 0)
CINZA = (100, 100, 100)
CINZA_ESCURO = (30, 30, 30)
AMARELO = (255, 200, 0)



# configurações gerais do pygame 


tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("jogo da cobra")
relogio = pygame.time.Clock()

fonte_ui = pygame.font.SysFont("arial", 20, bold=True)
fonte_gameover = pygame.font.SysFont("arial", 36, bold=True)
fonte_contador = pygame.font.SysFont("arial", 72, bold=True)


# -- gerando as imagens --

img_maca_original = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA), pygame.SRCALPHA)
pygame.draw.circle(img_maca_original, VERMELHO, (TAMANHO_CELULA//2, TAMANHO_CELULA//2), TAMANHO_CELULA//2 - 2)
pygame.draw.ellipse(img_maca_original, VERDE_CLARO, (TAMANHO_CELULA//2, 2, 10, 6))

img_cabeca_original = pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA), pygame.SRCALPHA)
pygame.draw.rect(img_cabeca_original, VERDE_CLARO, (0, 0, TAMANHO_CELULA, TAMANHO_CELULA), border_radius=8)
pygame.draw.circle(img_cabeca_original, PRETO, (12, 12), 4) 
pygame.draw.circle(img_cabeca_original, PRETO, (28, 12), 4) 



# --atualização feita dia 26/08 : Ideia de colocar um placar de líderes da sessão atual ( max 3 )

melhores_pontuacoes = []


# -- lógica inicial --
def iniciar_jogo():
    return {
        "cobra": [(10, 10), (10, 9), (10, 8)], 
        "direcao": (0, 1), 
        "maca": gerar_maca([(10, 10), (10, 9), (10, 8)], []),
        "obstaculos": [],
        "pontos": 0,
        "nivel": 1,
        "velocidade": 5,
        "frame": 0,
        "game_over": False,
        "pausado": False,       
        "em_contagem": False,   
        "tempo_inicio_contagem": 0 
    }

def gerar_maca(cobra, obstaculos):
    while True:
        nova = (random.randint(0, LINHAS - 1), random.randint(0, COLUNAS - 1))
        if nova not in cobra and nova not in obstaculos:
            return nova

estado = iniciar_jogo()


# --- loop do jogo ---
while True:
    estado["frame"] += 1

    # --- 1. EVENTOS (TECLADO E MOUSE) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if estado["game_over"]:
                estado = iniciar_jogo()
            else:
                if evento.key == pygame.K_p:
                    if not estado["pausado"] and not estado["em_contagem"]:
                        estado["pausado"] = True
                    elif estado["pausado"]:
                        estado["pausado"] = False
                        estado["em_contagem"] = True
                        estado["tempo_inicio_contagem"] = pygame.time.get_ticks()

                if not estado["pausado"] and not estado["em_contagem"]:
                    if evento.key == pygame.K_UP and estado["direcao"] != (1, 0):
                        estado["direcao"] = (-1, 0)
                    elif evento.key == pygame.K_DOWN and estado["direcao"] != (-1, 0):
                        estado["direcao"] = (1, 0)
                    elif evento.key == pygame.K_LEFT and estado["direcao"] != (0, 1):
                        estado["direcao"] = (0, -1)
                    elif evento.key == pygame.K_RIGHT and estado["direcao"] != (0, -1):
                        estado["direcao"] = (0, 1)

        if evento.type == pygame.MOUSEBUTTONDOWN and not estado["game_over"]:
            if evento.button == 1 and not estado["pausado"] and not estado["em_contagem"]:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                linha_clique = y_mouse // TAMANHO_CELULA
                coluna_clique = x_mouse // TAMANHO_CELULA
                alvo = (linha_clique, coluna_clique)
                
                if alvo not in estado["cobra"] and alvo != estado["maca"]:
                    estado["obstaculos"].append(alvo)

    # --- 2. LÓGICA DO JOGO ---
    if not estado["game_over"]:
        if estado["pausado"]:
            pass 
        elif estado["em_contagem"]:
            tempo_agora = pygame.time.get_ticks()
            if tempo_agora - estado["tempo_inicio_contagem"] >= 3000:
                estado["em_contagem"] = False
        else:
            linha_cabeca, coluna_cabeca = estado["cobra"][0]
            
            nova_linha = (linha_cabeca + estado["direcao"][0]) % LINHAS
            nova_coluna = (coluna_cabeca + estado["direcao"][1]) % COLUNAS
            nova_cabeca = (nova_linha, nova_coluna)
            
            bateu_corpo = nova_cabeca in estado["cobra"]
            bateu_obstaculo = nova_cabeca in estado["obstaculos"]
            
            if bateu_corpo or bateu_obstaculo:
                estado["game_over"] = True
                
                # NOVO: Salva a pontuação no placar
                melhores_pontuacoes.append(estado["pontos"])
                # Ordena a lista do maior para o menor
                melhores_pontuacoes.sort(reverse=True)
                # Mantém apenas as 3 melhores pontuações na lista para não encher a tela
                melhores_pontuacoes = melhores_pontuacoes[:3]
                
            else:
                estado["cobra"].insert(0, nova_cabeca)
                
                if nova_cabeca == estado["maca"]:
                    estado["pontos"] += 10
                    estado["nivel"] = (estado["pontos"] // 50) + 1 
                    estado["velocidade"] = 5 + estado["nivel"] 
                    estado["maca"] = gerar_maca(estado["cobra"], estado["obstaculos"])
                else:
                    estado["cobra"].pop()

    # --- 3. desenho ---

    tela.fill(PRETO)
    
    for l in range(LINHAS):
        for c in range(COLUNAS):
            pygame.draw.rect(tela, CINZA_ESCURO, (c * TAMANHO_CELULA, l * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 1)

    for obs in estado["obstaculos"]:
        pygame.draw.rect(tela, CINZA, (obs[1] * TAMANHO_CELULA, obs[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
        pygame.draw.rect(tela, PRETO, (obs[1] * TAMANHO_CELULA, obs[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 2)

    for i in range(1, len(estado["cobra"])):
        pedaco = estado["cobra"][i]
        pygame.draw.rect(tela, VERDE, (pedaco[1] * TAMANHO_CELULA, pedaco[0] * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), border_radius=4)

    cabeca = estado["cobra"][0]
    angulo = 0
    if estado["direcao"] == (0, -1): angulo = 90
    elif estado["direcao"] == (1, 0): angulo = 180
    elif estado["direcao"] == (0, 1): angulo = 270
    
    img_cabeca_rotacionada = pygame.transform.rotate(img_cabeca_original, angulo)
    tela.blit(img_cabeca_rotacionada, (cabeca[1] * TAMANHO_CELULA, cabeca[0] * TAMANHO_CELULA))

    if estado["frame"] % 10 < 5 and not estado["pausado"]:
        img_maca_animada = pygame.transform.scale(img_maca_original, (TAMANHO_CELULA - 6, TAMANHO_CELULA - 6))
        tela.blit(img_maca_animada, (estado["maca"][1] * TAMANHO_CELULA + 3, estado["maca"][0] * TAMANHO_CELULA + 3))
    else:
        tela.blit(img_maca_original, (estado["maca"][1] * TAMANHO_CELULA, estado["maca"][0] * TAMANHO_CELULA))

    texto_pontos = fonte_ui.render(f"Pontos: {estado['pontos']}", True, BRANCO)
    texto_nivel = fonte_ui.render(f"Nível: {estado['nivel']} (Vel: {estado['velocidade']})", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_nivel, (LARGURA - texto_nivel.get_width() - 10, 10))

    # --- overlays ---
    
    if estado["game_over"]:
        
        # Aumentei o tamanho do fundo preto para caber o placar
        fundo_overlay = pygame.Surface((LARGURA, 320))
        fundo_overlay.set_alpha(220) 
        fundo_overlay.fill(PRETO)
        tela.blit(fundo_overlay, (0, ALTURA//2 - 160))

        texto_go = fonte_gameover.render("GAME OVER", True, VERMELHO)
        tela.blit(texto_go, (LARGURA//2 - texto_go.get_width()//2, ALTURA//2 - 140))
        
        # desenhando o placa
        texto_titulo_placar = fonte_ui.render("--- Melhores Pontuações ---", True, AMARELO)
        tela.blit(texto_titulo_placar, (LARGURA//2 - texto_titulo_placar.get_width()//2, ALTURA//2 - 80))
        
        
        for indice, pontuacao in enumerate(melhores_pontuacoes):
            texto_recorde = fonte_ui.render(f"{indice + 1}º Lugar: {pontuacao} pts", True, BRANCO)
            
            tela.blit(texto_recorde, (LARGURA//2 - texto_recorde.get_width()//2, ALTURA//2 - 40 + (indice * 30)))

        texto_dica = fonte_ui.render("Pressione qualquer tecla para recomeçar", True, CINZA)
        tela.blit(texto_dica, (LARGURA//2 - texto_dica.get_width()//2, ALTURA//2 + 100))
        
    elif estado["pausado"]:
        fundo_overlay = pygame.Surface((LARGURA, 120))
        fundo_overlay.set_alpha(200) 
        fundo_overlay.fill(PRETO)
        tela.blit(fundo_overlay, (0, ALTURA//2 - 60))
        
        texto_pause = fonte_gameover.render("PAUSADO", True, AMARELO)
        texto_dica_pause = fonte_ui.render("Pressione 'P' para voltar", True, BRANCO)
        tela.blit(texto_pause, (LARGURA//2 - texto_pause.get_width()//2, ALTURA//2 - 40))
        tela.blit(texto_dica_pause, (LARGURA//2 - texto_dica_pause.get_width()//2, ALTURA//2 + 10))
        
    elif estado["em_contagem"]:
        fundo_overlay = pygame.Surface((LARGURA, 120))
        fundo_overlay.set_alpha(200) 
        fundo_overlay.fill(PRETO)
        tela.blit(fundo_overlay, (0, ALTURA//2 - 60))
        
        tempo_agora = pygame.time.get_ticks()
        passado = tempo_agora - estado["tempo_inicio_contagem"]
        
        if passado < 1000:
            numero = "3"
        elif passado < 2000:
            numero = "2"
        else:
            numero = "1"
            
        texto_num = fonte_contador.render(numero, True, AMARELO)
        tela.blit(texto_num, (LARGURA//2 - texto_num.get_width()//2, ALTURA//2 - 40))

    pygame.display.flip()
    relogio.tick(estado["velocidade"])