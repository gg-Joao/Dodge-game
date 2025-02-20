import pygame
import random
import math

pygame.init()
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Duǒshǎn")

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
CIANO = (0, 255, 255)
PRETO = (0, 0, 0)

JOGADOR_TAMANHO = 30
Projétils = []
tiros = []
TAMANHO_Projétil = 40
VEL_Projétil = 11
VEL_Projétil_VERDE = 11  
VELOCIDADE_TIRO = 16
TAMANHO_TIRO = 11 
MAX_VELOCIDADE = 36
AUMENTOS_VELOCIDADE = 16
aumentos_restantes = AUMENTOS_VELOCIDADE
tempo_ultimo_aumento = pygame.time.get_ticks()
intervalo_aumento = 6000
time_geracao_Projétil = 600

clock = pygame.time.Clock()
GERACAO_Projétil = pygame.USEREVENT + 1
GERACAO_Projétil_VERDE = pygame.USEREVENT + 2
pygame.time.set_timer(GERACAO_Projétil, time_geracao_Projétil)
pygame.time.set_timer(GERACAO_Projétil_VERDE, 3000)

font = pygame.font.Font(None, 36)

fundo = pygame.image.load("ao.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

menu_fundo = pygame.image.load("menu-.jpg")
menu_fundo = pygame.transform.scale(menu_fundo, (LARGURA, ALTURA))

recorde_tempo = 0

def calcular_direcao(x_inicial, y_inicial, destino_x, destino_y, velocidade):
    dx = destino_x - x_inicial
    dy = destino_y - y_inicial
    distancia = math.sqrt(dx**2 + dy**2)
    if distancia == 0:
        return 0, 0
    return (dx / distancia * velocidade, dy / distancia * velocidade)

def desenhar_triangulo(superficie, cor, centro, tamanho, angulo):
    angulo_rad = math.radians(angulo)
    p1 = (centro[0] + tamanho * math.cos(angulo_rad), centro[1] - tamanho * math.sin(angulo_rad))
    p2 = (centro[0] - tamanho * math.cos(angulo_rad + math.pi / 4), centro[1] + tamanho * math.sin(angulo_rad + math.pi / 4))
    p3 = (centro[0] - tamanho * math.cos(angulo_rad - math.pi / 4), centro[1] + tamanho * math.sin(angulo_rad - math.pi / 4))
    pygame.draw.polygon(superficie, cor, [p1, p2, p3])

def menu():
    rodando = True
    while rodando:
        TELA.blit(menu_fundo, (0, 0))
        titulo = font.render("Duǒshǎn", True, BRANCO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        
        texto_instrucao = font.render("Clique com o botão esquerdo do mouse para atirar nos projéteis verdes", True, BRANCO)
        TELA.blit(texto_instrucao, (LARGURA // 2 - texto_instrucao.get_width() // 2, 230))

        botao_jogar = pygame.Rect(LARGURA // 2 - 100, 300, 200, 50)
        texto_jogar = font.render("Jogar", True, BRANCO)
        TELA.blit(texto_jogar, (botao_jogar.x + 75, botao_jogar.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(event.pos):
                    return

def tela_morte(tempo_jogo):
    rodando = True
    while rodando:
        TELA.blit(menu_fundo, (0, 0))
        titulo = font.render("Você perdeu!", True, BRANCO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        tempo_final = font.render(f" Recorde: {tempo_jogo}s", True, BRANCO)
        TELA.blit(tempo_final, (LARGURA // 2 - tempo_final.get_width() // 2, 200))

        botao_jogar_novamente = pygame.Rect(LARGURA // 2 - 220, 300, 200, 50)
        botao_sair = pygame.Rect(LARGURA // 2 + 20, 300, 200, 50)
        texto_jogar_novamente = font.render("Jogar novamente", True, BRANCO)
        texto_sair = font.render("Sair", True, BRANCO)
        TELA.blit(texto_jogar_novamente, (botao_jogar_novamente.x + 25, botao_jogar_novamente.y + 10))
        TELA.blit(texto_sair, (botao_sair.x + 75, botao_sair.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar_novamente.collidepoint(event.pos):
                    return True
                elif botao_sair.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def main():
    global VEL_Projétil, aumentos_restantes, tempo_ultimo_aumento, time_geracao_Projétil, recorde_tempo, Projétils

    VEL_Projétil = 26
    aumentos_restantes = AUMENTOS_VELOCIDADE
    time_geracao_Projétil = 1000
    tempo_ultimo_aumento = pygame.time.get_ticks()
    Projétils.clear()
    tiros.clear()
    pygame.time.set_timer(GERACAO_Projétil, time_geracao_Projétil)
    pygame.time.set_timer(GERACAO_Projétil_VERDE, 3000)

    jogador_x, jogador_y = LARGURA // 2, ALTURA // 2
    rodando = True
    tempo_inicio = pygame.time.get_ticks()

    while rodando:
        clock.tick(60)
        TELA.blit(fundo, (0, 0))

        tempo_atual = pygame.time.get_ticks()
        tempo_jogo = (tempo_atual - tempo_inicio) // 1000

        if tempo_atual - tempo_ultimo_aumento >= intervalo_aumento and aumentos_restantes > 0:
            VEL_Projétil = min(VEL_Projétil + 1.0, MAX_VELOCIDADE)
            aumentos_restantes -= 1
            tempo_ultimo_aumento = tempo_atual
            time_geracao_Projétil = max(500, time_geracao_Projétil - 100)
            pygame.time.set_timer(GERACAO_Projétil, time_geracao_Projétil)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == GERACAO_Projétil:
                lado = random.choice(['E', 'D', 'C', 'B'])

                if lado == 'E':
                    x, y = 0, random.randint(0, ALTURA)
                elif lado == 'D':
                    x, y = LARGURA, random.randint(0, ALTURA)
                elif lado == 'C':
                    x, y = random.randint(0, LARGURA), 0
                else:
                    x, y = random.randint(0, LARGURA), ALTURA

                dx, dy = calcular_direcao(x, y, jogador_x, jogador_y, VEL_Projétil)
                angulo = math.degrees(math.atan2(-dy, dx))
                Projétils.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'angulo': angulo, 'cor': VERMELHO})
            
            elif event.type == GERACAO_Projétil_VERDE:
                lado = random.choice(['E', 'D', 'C', 'B'])
                
                if lado == 'E':
                    x, y = 0, random.randint(0, ALTURA)
                elif lado == 'D':
                    x, y = LARGURA, random.randint(0, ALTURA)
                elif lado == 'C':
                    x, y = random.randint(0, LARGURA), 0
                else:
                    x, y = random.randint(0, LARGURA), ALTURA

                dx, dy = calcular_direcao(x, y, jogador_x, jogador_y, VEL_Projétil_VERDE)
                angulo = math.degrees(math.atan2(-dy, dx))
                Projétils.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'angulo': angulo, 'cor': VERDE})
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    alvo = None
                    min_dist = float('inf')
                    for obs in Projétils:
                        if obs['cor'] == VERDE:
                            dist = math.dist((jogador_x, jogador_y), (obs['x'], obs['y']))
                            if dist < min_dist:
                                min_dist = dist
                                alvo = obs
                    if alvo:
                        dx, dy = calcular_direcao(jogador_x, jogador_y, alvo['x'], alvo['y'], VELOCIDADE_TIRO)
                        tiros.append({'x': jogador_x, 'y': jogador_y, 'dx': dx, 'dy': dy, 'tamanho': TAMANHO_TIRO, 'cor': CIANO})

        mouse_x, mouse_y = pygame.mouse.get_pos()
        jogador_x += (mouse_x - jogador_x) * 0.2
        jogador_y += (mouse_y - jogador_y) * 0.2

        pygame.draw.circle(TELA, AZUL, (int(jogador_x), int(jogador_y)), JOGADOR_TAMANHO // 2)

        # Atualizar projéteis
        for tiro in tiros[:]:
            tiro['x'] += tiro['dx']
            tiro['y'] += tiro['dy']
            
            if (tiro['x'] < 0 or tiro['x'] > LARGURA or 
                tiro['y'] < 0 or tiro['y'] > ALTURA):
                tiros.remove(tiro)
            else:
                for obs in Projétils[:]:
                    if obs['cor'] == VERDE:
                        distancia = math.hypot(tiro['x'] - obs['x'], tiro['y'] - obs['y'])
                        tiro_raio = tiro['tamanho'] // 2
                        obs_raio = TAMANHO_Projétil // 2
                        if distancia < tiro_raio + obs_raio:
                            try:
                                Projétils.remove(obs)
                                tiros.remove(tiro)
                            except ValueError:
                                pass

        # Desenhar tiros
        for tiro in tiros:
            pygame.draw.rect(TELA, tiro['cor'], (
                int(tiro['x'] - tiro['tamanho']//2), 
                int(tiro['y'] - tiro['tamanho']//2), 
                tiro['tamanho'], 
                tiro['tamanho']
            ))  

        # Atualizar projetil (verdes seguem o jogador)
        for obs in Projétils[:]:
            if obs['cor'] == VERDE:
                dx, dy = calcular_direcao(obs['x'], obs['y'], jogador_x, jogador_y, VEL_Projétil_VERDE)
                obs['dx'] = dx
                obs['dy'] = dy
                obs['angulo'] = math.degrees(math.atan2(-dy, dx))
            obs['x'] += obs['dx']
            obs['y'] += obs['dy']
            if math.dist((obs['x'], obs['y']), (jogador_x, jogador_y)) < JOGADOR_TAMANHO//2 + TAMANHO_Projétil//2:
                if tempo_jogo > recorde_tempo:
                    recorde_tempo = tempo_jogo
                if tela_morte(tempo_jogo):
                    main()
                rodando = False
            if obs['x'] < -TAMANHO_Projétil or obs['x'] > LARGURA or obs['y'] < -TAMANHO_Projétil or obs['y'] > ALTURA:
                Projétils.remove(obs)

        # Fazer projetil
        for obs in Projétils:
            desenhar_triangulo(TELA, obs['cor'], (int(obs['x']), int(obs['y'])), TAMANHO_Projétil//2, obs['angulo'])

        tempo_texto = font.render(f"Tempo: {tempo_jogo}s", True, BRANCO)
        recorde_texto = font.render(f"Recorde: {recorde_tempo}s", True, BRANCO)
        TELA.blit(tempo_texto, (10, 10))
        TELA.blit(recorde_texto, (10, 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    menu()
    main()