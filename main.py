import pygame
from assets import *
import random
from interfaz import Interfaz ,BATERIA_MAX , VIDAS_MAX , Button


# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 850

#Constantes



# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONDO = ( 200, 200, 200)

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agente Inteligente - IA U1")

#interfaz
interfaz = Interfaz()
btn_start = Button(screen , 650, 800, 'Comenzar', 100 , 40)


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

# Fuera de la función colocar(), define un arreglo para las posiciones de los coleccionables
posiciones_coleccionables = []

# Llena el arreglo con posiciones aleatorias
for _ in range(10):  # Suponiendo que tienes 10 coleccionables
    pos_x = random.randrange(1, 9)
    pos_y = random.randrange(1, 9)
    posiciones_coleccionables.append((pos_x, pos_y))

def colocar(posiciones):
    ancho_collec, alto_collect = CELL_SIZE // 1.5, CELL_SIZE // 1.5   

    for i, (pos_x, pos_y) in enumerate(posiciones):
        # Calcular la posición del coleccionable en la casilla actual
        collec_pos_x = pos_x * CELL_SIZE + (CELL_SIZE - ancho_collec) 
        collec_pos_y = pos_y * CELL_SIZE + (CELL_SIZE - alto_collect)
        screen.blit(coleccionables[i], (collec_pos_x, collec_pos_y))        


      

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
    frames_per_second = 10  # Velocidad de cambio de frames por segundo
    time_elapsed = 0
    frame = 0    

    global pos_personaje_x, pos_personaje_y, direccion , vidas , costo , buscando   # Para modificar las variables globales
    
    buscando = False
    vidas = VIDAS_MAX
    costo = 0
    
    
    running = True

   
       
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            

            if event.type == pygame.KEYDOWN:  # Manejar eventos de teclado
                costo +=  1  if costo < BATERIA_MAX else 0
                if event.key == pygame.K_UP:
                    if pos_personaje_y > 0: 
                        pos_personaje_y -= 1
                        direccion = "arriba"
                elif event.key == pygame.K_DOWN:
                    if pos_personaje_y < len(mapaJuego) - 1: 
                        pos_personaje_y += 1
                        direccion = "abajo"
                elif event.key == pygame.K_LEFT:
                    if pos_personaje_x > 0: 
                        pos_personaje_x -= 1
                        direccion = "izquierda"
                elif event.key == pygame.K_RIGHT:
                    if pos_personaje_x < len(mapaJuego[0]) - 1: 
                        pos_personaje_x += 1
                        direccion = "derecha"

           
            #Estacion de recarga vida y energia en 1 , 1
            elif pos_personaje_x == 1 and pos_personaje_y == 1 :
                vidas = VIDAS_MAX
                costo = 0

            elif mapaJuego[ pos_personaje_y ] [pos_personaje_x ] == 3  :
                vidas = vidas -1  if vidas > 0 else 0
            
           
            

               

            

        # Dibujar el mapa del juego
        screen.fill(FONDO)
        draw_map(mapaJuego)
        colocar(posiciones_coleccionables)
        personaje_ancho, personaje_alto = CELL_SIZE // 1.5, CELL_SIZE // 1.5 

        #Boton y  evento 
        btn_start.update()

        if btn_start.pressed :
            interfaz.dibujar_texto( screen , "Buscando ... " , WIDTH / 2 - 80 , 10 )

        if costo == BATERIA_MAX :
            btn_start.pressed = False

       

        # Calcular la posición del personaje en la casilla actual
        personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5 
        personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5

       

        time_elapsed += 1
        if time_elapsed >= frames_per_second:
            time_elapsed = 0
            frame = (frame + 1) % 2  # This line switches the frame between 0 and 1

        screen.blit(personajes[direccion][frame], (personaje_pos_x, personaje_pos_y))
        interfaz.dibujar_interface( screen , costo , vidas  )
       
        

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
    
