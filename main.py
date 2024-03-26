import pygame
from interfaz import Interfaz
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 850
CELL_SIZE = 80
VIDAS_MAX = 3
BATERIA_MAX = 15 

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interfaz de juego con Pygame")

# Interfaz 
interfaz = Interfaz()



# Cargar las imágenes
imagen_0 = pygame.image.load('pisos/tierra.png')
imagen_0 = pygame.transform.scale(imagen_0, (CELL_SIZE, CELL_SIZE))
imagen_1 = pygame.image.load('pisos/pasto.png')
imagen_1 = pygame.transform.scale(imagen_1, (CELL_SIZE, CELL_SIZE))
imagen_2 = pygame.image.load('obstaculos/arbol_00.png')
imagen_2 = pygame.transform.scale(imagen_2, (CELL_SIZE, CELL_SIZE))
imagen_3 = pygame.image.load('obstaculos/sprite_45.png')
imagen_3 = pygame.transform.scale(imagen_3, (CELL_SIZE, CELL_SIZE))

personaje_arriba = [pygame.image.load(f'pikachu/pikachu_arriba_{i}.png') for i in range(2)]
personaje_abajo = [pygame.image.load(f'pikachu/pikachu_abajo_{i}.png') for i in range(2)]
personaje_izquierda = [pygame.image.load(f'pikachu/pikachu_izq_{i}.png') for i in range(2)]
personaje_derecha = [pygame.image.load(f'pikachu/pikachu_der_{i}.png') for i in range(2)]

personajes = {
    "arriba": personaje_arriba,
    "abajo": personaje_abajo,
    "izquierda": personaje_izquierda,
    "derecha": personaje_derecha
}

personajes = {direccion: [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in sprites] for direccion, sprites in personajes.items()}

# Matriz del juego
mapaJuego = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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
pos_personaje_x, pos_personaje_y = 1, 1

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
    frame = 0

    global pos_personaje_x, pos_personaje_y, direccion, old_pos_personaje_x, old_pos_personaje_y , btn_Ini_Visble  , vidas , bateria, move# Para modificar las variables globales
    
    move = False
    vidas = VIDAS_MAX
    bateria = BATERIA_MAX
    btn_Ini_Visble = True
    running = True

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if interfaz.btn_Inciar.collidepoint(event.pos):
                    btn_Ini_Visble = False
            
            elif event.type == pygame.KEYDOWN:  # Manejar eventos de teclado
             
                if event.key == pygame.K_UP:
                    if pos_personaje_y > 0 and mapaJuego[pos_personaje_y - 1][pos_personaje_x] == 0:
                        mapaJuego[pos_personaje_y][pos_personaje_x] = 0  # Restablecer la casilla anterior
                        old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y
                        pos_personaje_y -= 1
                        direccion = "arriba"
                        bateria = bateria -1  if bateria > 0 else  0

                        move = True
                elif event.key == pygame.K_DOWN:
                    if pos_personaje_y < len(mapaJuego) - 1 and mapaJuego[pos_personaje_y + 1][pos_personaje_x] == 0:
                        #mapaJuego[pos_personaje_y][pos_personaje_x] = 0  # Restablecer la casilla anterior
                        old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y
                        pos_personaje_y += 1
                        bateria = bateria -1  if bateria > 0 else  0
                        direccion = "abajo"
                        move = True
                elif event.key == pygame.K_LEFT:
                    if pos_personaje_x > 0 and mapaJuego[pos_personaje_y][pos_personaje_x - 1] == 0:
                        mapaJuego[pos_personaje_y][pos_personaje_x] = 0  # Restablecer la casilla anterior
                        old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y
                        pos_personaje_x -= 1
                        direccion = "izquierda"
                        bateria = bateria -1  if bateria > 0 else  0
                        move = True
                elif event.key == pygame.K_RIGHT:
                    if pos_personaje_x < len(mapaJuego[0]) - 1 and mapaJuego[pos_personaje_y][pos_personaje_x + 1] == 0:
                        mapaJuego[pos_personaje_y][pos_personaje_x] = 0  # Restablecer la casilla anterior
                        old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y
                        pos_personaje_x += 1
                        direccion = "derecha"
                        bateria = bateria -1  if bateria > 0 else  0
                        
            elif pos_personaje_x == 1 and pos_personaje_y == 1 :
                vidas = VIDAS_MAX
                bateria = BATERIA_MAX
            
            elif mapaJuego[ pos_personaje_x ] [pos_personaje_y ] != 1 :
                vidas -= 1

           
            

        # Dibujar el mapa del juego
        screen.fill(WHITE)
        draw_map(mapaJuego)
     
        # Calcular la posición del personaje en la casilla actual
        personaje_pos_x = pos_personaje_x * CELL_SIZE
        personaje_pos_y = pos_personaje_y * CELL_SIZE

        # Cambiar al siguiente fotograma solo si se está moviendo
        if ( move ):
            frame = (frame + 1) % 2
            move = False
            

        screen.blit(personajes[direccion][frame], (personaje_pos_x, personaje_pos_y))
        
        interfaz.dibujar_interface( screen , bateria , vidas , btn_Ini_Visble )

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
