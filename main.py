import pygame
from assets import *

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 800

# Colores
WHITE = (255, 255, 255)

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agente Inteligente - IA U1")

# Matriz del juego
mapaJuego = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 3, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Posición inicial del personaje
pos_personaje_x, pos_personaje_y = 0, 0

# Dirección inicial del personaje
direccion = "abajo"

# Almacenar la posición anterior del personaje
old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y

# Función para dibujar el mapa del juego
def draw_map(mapa):
    for y, row in enumerate(mapa):
        for x, cell in enumerate(row):
            if cell == 0:
                screen.blit(imagen_0, (x * CELL_SIZE, y * CELL_SIZE))
            elif cell == 1:
                screen.blit(imagen_1, (x * CELL_SIZE, y * CELL_SIZE))
            elif cell == 2:
                screen.blit(imagen_2, (x * CELL_SIZE, y * CELL_SIZE))
            elif cell == 3:
                screen.blit(imagen_3, (x * CELL_SIZE, y * CELL_SIZE))

# Función principal del juego
def main():
    clock = pygame.time.Clock()  # Crear un objeto para ayudar a controlar el tiempo
    frame_rate = 10  # Velocidad de cambio de frames por segundo
    frame_count = 0  # Contador para controlar el cambio de frames
    frame = 0

    global pos_personaje_x, pos_personaje_y, direccion, old_pos_personaje_x, old_pos_personaje_y  # Para modificar las variables globales

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # Manejar eventos de teclado
                if event.key == pygame.K_UP:
                    if pos_personaje_y > 0: #and mapaJuego[pos_personaje_y - 1][pos_personaje_x] == 0:
                        pos_personaje_y -= 1
                        direccion = "arriba"
                elif event.key == pygame.K_DOWN:
                    if pos_personaje_y < len(mapaJuego) - 1: #and mapaJuego[pos_personaje_y + 1][pos_personaje_x] == 0:
                        pos_personaje_y += 1
                        direccion = "abajo"
                elif event.key == pygame.K_LEFT:
                    if pos_personaje_x > 0: #and mapaJuego[pos_personaje_y][pos_personaje_x - 1] == 0:
                        pos_personaje_x -= 1
                        direccion = "izquierda"
                elif event.key == pygame.K_RIGHT:
                    if pos_personaje_x < len(mapaJuego[0]) - 1: #and mapaJuego[pos_personaje_y][pos_personaje_x + 1] == 0:
                        pos_personaje_x += 1
                        direccion = "derecha"

        # Dibujar el mapa del juego
        screen.fill(WHITE)
        draw_map(mapaJuego)

        personaje_ancho, personaje_alto = CELL_SIZE // 2, CELL_SIZE // 2 

        # Calcular la posición del personaje en la casilla actual
        personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 2 
        personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 2

        screen.blit(personajes[direccion][frame], (personaje_pos_x, personaje_pos_y))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
