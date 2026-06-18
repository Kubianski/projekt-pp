import pygame
import sys
import random

pygame.init()

SZEROKOSC = 800
WYSOKOSC = 600
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Pong")

zegar = pygame.time.Clock()
FPS = 60

CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)

PALETKA_SZEROKOSC = 15
PALETKA_WYSOKOSC = 100

gracz1_x = 50
gracz1_y = WYSOKOSC // 2 - PALETKA_WYSOKOSC // 2

gracz2_x = SZEROKOSC - 50 - PALETKA_SZEROKOSC
gracz2_y = WYSOKOSC // 2 - PALETKA_WYSOKOSC // 2

predkosc_paletki = 6

PILKA_ROZMIAR = 15
pilka_x = SZEROKOSC // 2 - PILKA_ROZMIAR // 2
pilka_y = WYSOKOSC // 2 - PILKA_ROZMIAR // 2

predkosc_pilka_x = 5 * random.choice((1, -1))
predkosc_pilka_y = 5 * random.choice((1, -1))

wynik_gracz1 = 0
wynik_gracz2 = 0

czcionka = pygame.font.SysFont("Arial", 40)

def resetuj_pilke():
    global pilka_x, pilka_y, predkosc_pilka_x, predkosc_pilka_y
    pilka_x = SZEROKOSC // 2 - PILKA_ROZMIAR // 2
    pilka_y = WYSOKOSC // 2 - PILKA_ROZMIAR // 2
    predkosc_pilka_x *= -1
    predkosc_pilka_y = 5 * random.choice((1, -1))

while True:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    klawisze = pygame.key.get_pressed()
    
    if klawisze[pygame.K_w] and gracz1_y > 0:
        gracz1_y -= predkosc_paletki
    if klawisze[pygame.K_s] and gracz1_y < WYSOKOSC - PALETKA_WYSOKOSC:
        gracz1_y += predkosc_paletki

    if klawisze[pygame.K_UP] and gracz2_y > 0:
        gracz2_y -= predkosc_paletki
    if klawisze[pygame.K_DOWN] and gracz2_y < WYSOKOSC - PALETKA_WYSOKOSC:
        gracz2_y += predkosc_paletki

    pilka_x += predkosc_pilka_x
    pilka_y += predkosc_pilka_y

    if pilka_y <= 0 or pilka_y >= WYSOKOSC - PILKA_ROZMIAR:
        predkosc_pilka_y *= -1

    paletka1_rect = pygame.Rect(gracz1_x, gracz1_y, PALETKA_SZEROKOSC, PALETKA_WYSOKOSC)
    paletka2_rect = pygame.Rect(gracz2_x, gracz2_y, PALETKA_SZEROKOSC, PALETKA_WYSOKOSC)
    pilka_rect = pygame.Rect(pilka_x, pilka_y, PILKA_ROZMIAR, PILKA_ROZMIAR)

    if pilka_rect.colliderect(paletka1_rect) or pilka_rect.colliderect(paletka2_rect):
        predkosc_pilka_x *= -1
        predkosc_pilka_x *= 1.05 
        predkosc_pilka_y *= 1.05

    if pilka_x < 0:
        wynik_gracz2 += 1
        resetuj_pilke()
        predkosc_pilka_x = 5 if predkosc_pilka_x > 0 else -5
        predkosc_pilka_y = 5 if predkosc_pilka_y > 0 else -5

    if pilka_x > SZEROKOSC:
        wynik_gracz1 += 1
        resetuj_pilke()
        predkosc_pilka_x = 5 if predkosc_pilka_x > 0 else -5
        predkosc_pilka_y = 5 if predkosc_pilka_y > 0 else -5

    ekran.fill(CZARNY)

    pygame.draw.aaline(ekran, BIALY, (SZEROKOSC // 2, 0), (SZEROKOSC // 2, WYSOKOSC))

    pygame.draw.rect(ekran, BIALY, paletka1_rect)
    pygame.draw.rect(ekran, BIALY, paletka2_rect)
    pygame.draw.ellipse(ekran, BIALY, pilka_rect)

    tekst_wyniku = czcionka.render(f"{wynik_gracz1}   {wynik_gracz2}", True, BIALY)
    ekran.blit(tekst_wyniku, (SZEROKOSC // 2 - tekst_wyniku.get_width() // 2, 20))

    pygame.display.flip()
    zegar.tick(FPS)