import pygame
import random
import math

pygame.init()
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Dodge")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
CIANO = (0, 255, 255)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128) 
PRETO = (0, 0, 0)

JOGADOR_TAMANHO = 30
TAMANHO_PROJETIL = 40
VEL_PROJETIL = 21
VEL_PROJETIL_VERDE = 16
VELOCIDADE_TIRO = 16
TAMANHO_TIRO = 11
MAX_VELOCIDADE = 60
AUMENTOS_VELOCIDADE = 36
DISTANCIA_MINIMA_SPAWN = 360
aumentos_restantes = AUMENTOS_VELOCIDADE
intervalo_aumento = 6000
time_geracao_projetil = 600
TAMANHO_BOLA_CHEFE = 60
VEL_BOLA_CHEFE = 11
VEL_BOLA_CHEFE_CINZA = 13
SAUDE_BOLA_CHEFE = 23

# Variáveis do jogo
projeteis = []
tiros = []
boss_balls = []
boss_cinzas = [] 
BOSS_ACTIVE = False
BOSS_CINZA_ACTIVE = False  
recorde_tempo = 0
BOSS_DERROTADO = False

clock = pygame.time.Clock()
GERACAO_PROJETIL = pygame.USEREVENT + 1
GERACAO_PROJETIL_VERDE = pygame.USEREVENT + 2

font = pygame.font.Font(None, 36)
fundo = pygame.image.load("ao.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
menu_fundo = pygame.image.load("menu-.jpg")
menu_fundo = pygame.transform.scale(menu_fundo, (LARGURA, ALTURA))

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
        titulo = font.render("Dodge", True, BRANCO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        texto_instrucao = font.render("Clique com o botão esquerdo do mouse para atirar nos projéteis verdes e nos bosses", True, BRANCO)
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

        tempo_final = font.render(f" Tempo obtido: {tempo_jogo}s", True, BRANCO)
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
    global VEL_PROJETIL, aumentos_restantes, recorde_tempo, BOSS_ACTIVE, projeteis, tiros, boss_balls, BOSS_DERROTADO, BOSS_CINZA_ACTIVE, boss_cinzas

    VEL_PROJETIL = 21
    aumentos_restantes = AUMENTOS_VELOCIDADE
    projeteis.clear()
    tiros.clear()
    boss_balls.clear()
    boss_cinzas.clear()
    BOSS_ACTIVE = False
    BOSS_CINZA_ACTIVE = False
    BOSS_DERROTADO = False

    jogador_x, jogador_y = LARGURA // 2, ALTURA // 2
    tempo_inicio = pygame.time.get_ticks()
    tempo_ultimo_aumento = pygame.time.get_ticks()

    pygame.time.set_timer(GERACAO_PROJETIL, time_geracao_projetil)
    pygame.time.set_timer(GERACAO_PROJETIL_VERDE, 3000)

    rodando = True
    while rodando:
        clock.tick(60)
        TELA.blit(fundo, (0, 0))

        tempo_atual = pygame.time.get_ticks()
        tempo_jogo = (tempo_atual - tempo_inicio) // 1000

        if tempo_jogo >= 23 and not BOSS_ACTIVE and not BOSS_DERROTADO and not BOSS_CINZA_ACTIVE and len(boss_balls) == 0:
            BOSS_ACTIVE = True
            pygame.time.set_timer(GERACAO_PROJETIL, 0)  
            pygame.time.set_timer(GERACAO_PROJETIL_VERDE, 0)  
            for _ in range(3):
                while True:
                    x = random.randint(100, LARGURA - 100)
                    y = random.randint(100, ALTURA - 100)
                    if math.hypot(x - jogador_x, y - jogador_y) > 500:  
                        break
                boss_balls.append({
                    'x': x,
                    'y': y,
                    'saude': SAUDE_BOLA_CHEFE,
                    'cor': AMARELO
                })

        # ativação do chefe cinza
        if tempo_jogo >= 60 and not BOSS_CINZA_ACTIVE and len(boss_cinzas) == 0:  
            BOSS_CINZA_ACTIVE = True
            for _ in range(3):
                while True:
                    x = random.randint(100, LARGURA - 100)
                    y = random.randint(100, ALTURA - 100)
                    if math.hypot(x - jogador_x, y - jogador_y) > 500:  
                        break
                boss_cinzas.append({
                    'x': x,
                    'y': y,
                    'saude': SAUDE_BOLA_CHEFE,
                    'cor': CINZA
                })

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == GERACAO_PROJETIL and not BOSS_ACTIVE and not BOSS_CINZA_ACTIVE:  
                lado = random.choice(['E', 'D', 'C', 'B'])
                while True:
                    if lado == 'E': 
                        x, y = 0, random.randint(0, ALTURA)
                    elif lado == 'D': 
                        x, y = LARGURA, random.randint(0, ALTURA)
                    elif lado == 'C': 
                        x, y = random.randint(0, LARGURA), 0
                    else: 
                        x, y = random.randint(0, LARGURA), ALTURA
                    
                    if math.hypot(x - jogador_x, y - jogador_y) > DISTANCIA_MINIMA_SPAWN:
                        break

                dx, dy = calcular_direcao(x, y, jogador_x, jogador_y, VEL_PROJETIL)
                angulo = math.degrees(math.atan2(-dy, dx))
                projeteis.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'angulo': angulo, 'cor': VERMELHO})
            
            if event.type == GERACAO_PROJETIL_VERDE and not BOSS_ACTIVE and not BOSS_CINZA_ACTIVE:  
                lado = random.choice(['E', 'D', 'C', 'B'])
                while True:
                    if lado == 'E': 
                        x, y = 0, random.randint(0, ALTURA)
                    elif lado == 'D': 
                        x, y = LARGURA, random.randint(0, ALTURA)
                    elif lado == 'C': 
                        x, y = random.randint(0, LARGURA), 0
                    else: 
                        x, y = random.randint(0, LARGURA), ALTURA
                    
                    if math.hypot(x - jogador_x, y - jogador_y) > DISTANCIA_MINIMA_SPAWN:
                        break

                dx, dy = calcular_direcao(x, y, jogador_x, jogador_y, VEL_PROJETIL_VERDE)
                angulo = math.degrees(math.atan2(-dy, dx))
                projeteis.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'angulo': angulo, 'cor': VERDE})
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                alvo = None
                min_dist = float('inf')
                targets = projeteis + boss_balls + boss_cinzas if BOSS_ACTIVE or BOSS_CINZA_ACTIVE else projeteis
                
                for obs in targets:
                    valid_target = (obs['cor'] == VERDE) if not BOSS_ACTIVE and not BOSS_CINZA_ACTIVE else True
                    if valid_target:
                        dist = math.dist((jogador_x, jogador_y), (obs['x'], obs['y']))
                        if dist < min_dist:
                            min_dist = dist
                            alvo = obs
                
                if alvo:
                    dx, dy = calcular_direcao(jogador_x, jogador_y, alvo['x'], alvo['y'], VELOCIDADE_TIRO)
                    tiros.append({'x': jogador_x, 'y': jogador_y, 'dx': dx, 'dy': dy, 'tamanho': TAMANHO_TIRO, 'cor': CIANO})

        # Movimento do jogador
        mouse_x, mouse_y = pygame.mouse.get_pos()
        jogador_x += (mouse_x - jogador_x) * 0.2
        jogador_y += (mouse_y - jogador_y) * 0.2
        pygame.draw.circle(TELA, AZUL, (int(jogador_x), int(jogador_y)), JOGADOR_TAMANHO // 2)

        #  tiros e colisões
        for tiro in tiros[:]:
            tiro['x'] += tiro['dx']
            tiro['y'] += tiro['dy']

            if (tiro['x'] < 0 or tiro['x'] > LARGURA or tiro['y'] < 0 or tiro['y'] > ALTURA):
                tiros.remove(tiro)
                continue

            # Colisão com projéteis verdes
            for obs in projeteis[:]:
                if obs['cor'] == VERDE:
                    distancia = math.hypot(tiro['x'] - obs['x'], tiro['y'] - obs['y'])
                    if distancia < TAMANHO_PROJETIL // 2 + TAMANHO_TIRO // 2:
                        projeteis.remove(obs)
                        tiros.remove(tiro)
                        break

            for boss in boss_balls[:]:
                distancia = math.hypot(tiro['x'] - boss['x'], tiro['y'] - boss['y'])
                if distancia < TAMANHO_BOLA_CHEFE // 2 + TAMANHO_TIRO // 2:
                    boss['saude'] -= 1
                    tiros.remove(tiro)
                    if boss['saude'] <= 0:
                        boss_balls.remove(boss)
                    break

            for boss in boss_cinzas[:]:
                distancia = math.hypot(tiro['x'] - boss['x'], tiro['y'] - boss['y'])
                if distancia < TAMANHO_BOLA_CHEFE // 2 + TAMANHO_TIRO // 2:
                    boss['saude'] -= 1
                    tiros.remove(tiro)
                    if boss['saude'] <= 0:
                        boss_cinzas.remove(boss)
                    break

        # Atualização de projéteis
        for obs in projeteis[:]:
            if obs['cor'] == VERDE:
                dx, dy = calcular_direcao(obs['x'], obs['y'], jogador_x, jogador_y, VEL_PROJETIL_VERDE)
                obs['dx'], obs['dy'] = dx, dy
                obs['angulo'] = math.degrees(math.atan2(-dy, dx))
            
            obs['x'] += obs['dx']
            obs['y'] += obs['dy']

            if math.dist((obs['x'], obs['y']), (jogador_x, jogador_y)) < JOGADOR_TAMANHO // 2 + TAMANHO_PROJETIL // 2:
                if tempo_jogo > recorde_tempo:
                    recorde_tempo = tempo_jogo
                if tela_morte(tempo_jogo):
                    main()
                rodando = False

            if (obs['x'] < -TAMANHO_PROJETIL or obs['x'] > LARGURA or obs['y'] < -TAMANHO_PROJETIL or obs['y'] > ALTURA):
                projeteis.remove(obs)

        for boss in boss_balls[:]:
            dx, dy = calcular_direcao(boss['x'], boss['y'], jogador_x, jogador_y, VEL_BOLA_CHEFE)
            boss['x'] += dx
            boss['y'] += dy

            if math.dist((boss['x'], boss['y']), (jogador_x, jogador_y)) < JOGADOR_TAMANHO // 2 + TAMANHO_BOLA_CHEFE // 2:
                if tempo_jogo > recorde_tempo:
                    recorde_tempo = tempo_jogo
                if tela_morte(tempo_jogo):
                    main()
                rodando = False

        for boss in boss_cinzas[:]:
            dx, dy = calcular_direcao(boss['x'], boss['y'], jogador_x, jogador_y, VEL_BOLA_CHEFE_CINZA)
            boss['x'] += dx
            boss['y'] += dy

            if math.dist((boss['x'], boss['y']), (jogador_x, jogador_y)) < JOGADOR_TAMANHO // 2 + TAMANHO_BOLA_CHEFE // 2:
                if tempo_jogo > recorde_tempo:
                    recorde_tempo = tempo_jogo
                if tela_morte(tempo_jogo):
                    main()
                rodando = False

        # Verificação da vitória do boss amarelo  
        if BOSS_ACTIVE and len(boss_balls) == 0:
            BOSS_ACTIVE = False
            BOSS_DERROTADO = True
            pygame.time.set_timer(GERACAO_PROJETIL, time_geracao_projetil) 
            pygame.time.set_timer(GERACAO_PROJETIL_VERDE, 1600)  
            projeteis.clear()

        # Verificação da vitória do boss cinza 
        if BOSS_CINZA_ACTIVE and len(boss_cinzas) == 0:
            BOSS_CINZA_ACTIVE = False
            pygame.time.set_timer(GERACAO_PROJETIL, time_geracao_projetil)  
            pygame.time.set_timer(GERACAO_PROJETIL_VERDE, 6000)  
            projeteis.clear()
            VEL_PROJETIL = 21
            aumentos_restantes = AUMENTOS_VELOCIDADE
            BOSS_DERROTADO = False
            boss_balls.clear()  
            BOSS_ACTIVE = False  

        for obs in projeteis:
            desenhar_triangulo(TELA, obs['cor'], (int(obs['x']), int(obs['y'])), TAMANHO_PROJETIL // 2, obs['angulo'])

        for tiro in tiros:
            pygame.draw.rect(TELA, tiro['cor'], (
                int(tiro['x'] - tiro['tamanho'] // 2), 
                int(tiro['y'] - tiro['tamanho'] // 2), 
                tiro['tamanho'], 
                tiro['tamanho']
            ))

        for boss in boss_balls:
            pygame.draw.circle(TELA, boss['cor'], (int(boss['x']), int(boss['y'])), TAMANHO_BOLA_CHEFE // 2)

        for boss in boss_cinzas:
            pygame.draw.circle(TELA, boss['cor'], (int(boss['x']), int(boss['y'])), TAMANHO_BOLA_CHEFE // 2)

        tempo_texto = font.render(f"Tempo: {tempo_jogo}s", True, BRANCO)
        recorde_texto = font.render(f"Recorde: {recorde_tempo}s", True, BRANCO)
        TELA.blit(tempo_texto, (10, 10))
        TELA.blit(recorde_texto, (10, 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    menu()
    main()
