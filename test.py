import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir la clase para el botón
class Boton:
    def __init__(self, texto, x, y, ancho, alto, color, color_hover, action=None):
        self.texto = texto
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.color_hover = color_hover
        self.action = action

    def dibujar(self, pantalla, fuente, mouse):
        if self.x < mouse[0] < self.x + self.ancho and self.y < mouse[1] < self.y + self.alto:
            pygame.draw.rect(pantalla, self.color_hover, (self.x, self.y, self.ancho, self.alto))
        else:
            pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

        texto_surface = fuente.render(self.texto, True, NEGRO)
        texto_rect = texto_surface.get_rect(center=(self.x + self.ancho/2, self.y + self.alto/2))
        pantalla.blit(texto_surface, texto_rect)

    def click(self):
        if self.action:
            self.action()

# Configurar la pantalla
pantalla = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Botón en Pygame')

# Definir el botón
mi_boton = Boton('Haz clic', 150, 100, 100, 50, BLANCO, (200, 200, 200), action=lambda: print('Haz clic en el botón'))

# Ciclo principal del juego
while True:
    pantalla.fill(NEGRO)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and mi_boton.x < mouse[0] < mi_boton.x + mi_boton.ancho and mi_boton.y < mouse[1] < mi_boton.y + mi_boton.alto:
            mi_boton.click()

    mi_boton.dibujar(pantalla, pygame.font.Font(None, 36), mouse)
    pygame.display.flip()
