import pygame
import random
import math

pygame.init()
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Desvie dos projéteis")

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)

JOGADOR_TAMANHO = 30
obstaculos = []
TAMANHO_OBSTACULO = 40
VEL_OBSTACULO = 3.5
MAX_VELOCIDADE = 7.0
AUMENTOS_VELOCIDADE = 6
aumentos_restantes = AUMENTOS_VELOCIDADE
tempo_ultimo_aumento = pygame.time.get_ticks()
intervalo_aumento = 6000
time_geracao_obstaculo = 1000
clock = pygame.time.Clock()
GERACAO_OBSTACULO = pygame.USEREVENT + 1
pygame.time.set_timer(GERACAO_OBSTACULO, time_geracao_obstaculo)

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
        titulo = font.render("Desvie dos projéteis", True, BRANCO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        # Centralização
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
    global VEL_OBSTACULO, aumentos_restantes, tempo_ultimo_aumento, time_geracao_obstaculo, recorde_tempo
    jogador_x, jogador_y = LARGURA // 2, ALTURA // 2
    rodando = True
    tempo_inicio = pygame.time.get_ticks()

    while rodando:
        clock.tick(60)
        TELA.blit(fundo, (0, 0))

        tempo_atual = pygame.time.get_ticks()
        tempo_jogo = (tempo_atual - tempo_inicio) // 1000

        if tempo_atual - tempo_ultimo_aumento >= intervalo_aumento and aumentos_restantes > 0:
            VEL_OBSTACULO = min(VEL_OBSTACULO + 1.0, MAX_VELOCIDADE)
            aumentos_restantes -= 1
            tempo_ultimo_aumento = tempo_atual
            time_geracao_obstaculo = max(500, time_geracao_obstaculo - 100)
            pygame.time.set_timer(GERACAO_OBSTACULO, time_geracao_obstaculo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == GERACAO_OBSTACULO:
                lado = random.choice(['E', 'D', 'C', 'B'])

                if lado == 'E':
                    x, y = 0, random.randint(0, ALTURA)
                elif lado == 'D':
                    x, y = LARGURA, random.randint(0, ALTURA)
                elif lado == 'C':
                    x, y = random.randint(0, LARGURA), 0
                else:
                    x, y = random.randint(0, LARGURA), ALTURA

                dx, dy = calcular_direcao(x, y, jogador_x, jogador_y, VEL_OBSTACULO)
                angulo = math.degrees(math.atan2(-dy, dx))
                obstaculos.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'angulo': angulo})

        mouse_x, mouse_y = pygame.mouse.get_pos()
        jogador_x += (mouse_x - jogador_x) * 0.2
        jogador_y += (mouse_y - jogador_y) * 0.2

        pygame.draw.circle(TELA, AZUL, (int(jogador_x), int(jogador_y)), JOGADOR_TAMANHO // 2)

        for obs in obstaculos[:]:
            obs['x'] += obs['dx']
            obs['y'] += obs['dy']
            if math.dist((obs['x'], obs['y']), (jogador_x, jogador_y)) < JOGADOR_TAMANHO // 2 + TAMANHO_OBSTACULO // 2:
                if tempo_jogo > recorde_tempo:
                    recorde_tempo = tempo_jogo
                if tela_morte(tempo_jogo):  # jogar de novo
                    main()
                rodando = False
            if obs['x'] < -TAMANHO_OBSTACULO or obs['x'] > LARGURA or obs['y'] < -TAMANHO_OBSTACULO or obs['y'] > ALTURA:
                obstaculos.remove(obs)

        for obs in obstaculos:
            desenhar_triangulo(TELA, VERMELHO, (int(obs['x']), int(obs['y'])), TAMANHO_OBSTACULO // 2, obs['angulo'])

        tempo_texto = font.render(f"Tempo: {tempo_jogo}s", True, PRETO)
        recorde_texto = font.render(f"Recorde: {recorde_tempo}s", True, PRETO)
        TELA.blit(tempo_texto, (10, 10))
        TELA.blit(recorde_texto, (10, 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    menu()
    main()
