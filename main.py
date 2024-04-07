import pygame
import algoritoAEstrella
from assets import *
import random
import time
import threading
import math
from interfaz import Interfaz ,BATERIA_MAX , VIDAS_MAX , Button


# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 850

# Colores
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
FONDO = ( 200, 200, 200 )

# Crear la ventana del juego
screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( "Agente Inteligente - IA U1" )

#------ Crecion de objetos ----
# interfaz
interfaz = Interfaz()
btn_start = Button( screen , 650, 800, 'Buscar', 100 , 40 )
btn_reinicio = Button(screen, 500, 800, 'Reiniciar',100,40 )


# Matriz del juego
mapaJuego = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 2, 0, 1],
    [1, 3, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 2, 2, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Posiciones posible para el personaje
posiciones_personaje = [(1,1), (1,8), (8,1), (8,8)]
pos_personaje_x, pos_personaje_y = random.choice(posiciones_personaje)
pos_personaje__final = algoritoAEstrella.Nodo(pos_personaje_x,pos_personaje_y)

# Dirección inicial del personaje
if (pos_personaje_x, pos_personaje_y) == (1,1) or (pos_personaje_x, pos_personaje_y) == (8,1):
    direccion = "abajo"
else:
    direccion = "arriba"

# Almacenar la posición anterior del personaje
old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y

# Fuera de la función colocar(), define un arreglo para las posiciones de los coleccionables
posiciones_coleccionables = [(random.randrange(1, 9), random.randrange(1, 9)) for _ in range(10)]

def colocar(posiciones):
    ancho_collec, alto_collect = CELL_SIZE // 1.5, CELL_SIZE // 1.5

    i = 0
    while i < len(posiciones):

        pos_x, pos_y = posiciones[i]

        # Verificar si la posición aleatoria coincide con la posición de las bayas o si el valor de la posición en la matriz es 3
        if (pos_x, pos_y) != (4, 8) and \
            mapaJuego[pos_y][pos_x] != 3 and \
            (pos_x, pos_y) not in posiciones_personaje and \
            mapaJuego[pos_y][pos_x] != 2:
            # Calcular la posición del coleccionable en la casilla actual
            collec_pos_x = pos_x * CELL_SIZE + (CELL_SIZE - ancho_collec) 
            collec_pos_y = pos_y * CELL_SIZE + (CELL_SIZE - alto_collect)
            screen.blit(coleccionables[i], (collec_pos_x, collec_pos_y))
            i += 1
        else:
            while True:
                pos_x = random.randrange(1, 9)
                pos_y = random.randrange(1, 9)
                if (pos_x, pos_y) not in posiciones:
                    break
            posiciones[i] = (pos_x, pos_y)

            # Calcular la posición del coleccionable en la nueva casilla
            collec_pos_x = pos_x * CELL_SIZE + (CELL_SIZE - ancho_collec) 
            collec_pos_y = pos_y * CELL_SIZE + (CELL_SIZE - alto_collect)
            screen.blit(coleccionables[i], (collec_pos_x, collec_pos_y))


# Define el índice del frame actual de la animación de la imagen_3
frame_index_imagen_3, frame_index_bayas = 0,0

# Función para animar la imagen_3
def animate_imagen_3():
    global frame_index_imagen_3
    frame_index_imagen_3 = (frame_index_imagen_3 + 1) % len(snorlax_tierra)

def animate_bayas():
    global frame_index_bayas
    frame_index_bayas = ( frame_index_bayas + 1 ) % len(bayas)

# Definir variables para controlar la animación de Muk
frame_index_muk = 0
muk_animation_counter = 0
muk_animation_speed = 3  # Ajusta este valor para ralentizar la animación de Muk

# Definir variables para controlar la animación de Voltorb
frame_index_voltorb = 0
voltorb_animation_counter = 0
voltorb_animation_speed = 3  # Ajusta este valor para ralentizar la animación de Voltorb

# Función para animar a Muk
def animate_muk():
    global frame_index_muk, muk_animation_counter

    muk_animation_counter += 1
    if muk_animation_counter >= muk_animation_speed:
        frame_index_muk = (frame_index_muk + 1) % len(muk)
        muk_animation_counter = 0

# Función para animar a Voltorb
def animate_voltorb():
    global frame_index_voltorb, voltorb_animation_counter

    voltorb_animation_counter += 1
    if voltorb_animation_counter >= voltorb_animation_speed:
        frame_index_voltorb = (frame_index_voltorb + 1) % len(voltorb)
        voltorb_animation_counter = 0

posiciones_muk = [(random.randrange(1, 9), random.randrange(1, 9)) for _ in range(4)]
posiciones_voltorb = [(random.randrange(1, 9), random.randrange(1, 9)) for _ in range(4)]

def colocar_enemigos(posiciones_enemigos, posiciones_colectables, frame_enemigo, enemigo_images):
    ancho_enemigo, alto_enemigo = 40 , 40

    if posiciones_enemigos == posiciones_muk:
        posiciones_ocupadas = set(posiciones_colectables) | set(posiciones_voltorb) | set( posiciones_personaje )
    elif posiciones_enemigos == posiciones_voltorb:
        posiciones_ocupadas = set(posiciones_colectables) | set(posiciones_muk) | set( posiciones_personaje )

    for i, (pos_x, pos_y) in enumerate(posiciones_enemigos):
        while (pos_x, pos_y) in posiciones_ocupadas or \
                mapaJuego[pos_y][pos_x] in [2, 3] or \
                (pos_x, pos_y) == (4, 8):
            pos_x = random.randrange(1, 9)
            pos_y = random.randrange(1, 9)
        
        posiciones_enemigos[i] = (pos_x, pos_y)
        posiciones_ocupadas.add((pos_x, pos_y))

        enemigo_pos_x = pos_x * CELL_SIZE + (CELL_SIZE - ancho_enemigo) // 2
        enemigo_pos_y = pos_y * CELL_SIZE + (CELL_SIZE - alto_enemigo) // 2
        screen.blit(enemigo_images[frame_enemigo], (enemigo_pos_x, enemigo_pos_y))


tipo_piso = []

for y, row in enumerate(mapaJuego):
        for x, cell in enumerate(row):
            if cell == 0:
                piso = random.choice( [ tierra, tierra, pasto, lodo ] )
                tipo_piso.append(piso)

# Función para dibujar el mapa del juego
def draw_map(mapa):

    index = 0

    for y, row in enumerate(mapa):
        for x, cell in enumerate(row):
            if cell == 0:
                screen.blit( tipo_piso[index], (x * CELL_SIZE, y * CELL_SIZE))
                index += 1
            elif cell == 1:
                screen.blit(arbol_pasto, (x * CELL_SIZE, y * CELL_SIZE))
            elif cell == 2:
                screen.blit(arbol_tierra, (x * CELL_SIZE, y * CELL_SIZE))
            elif cell == 3:
                screen.blit(snorlax_tierra[frame_index_imagen_3], (x * CELL_SIZE, y * CELL_SIZE))




# Elimina el colecionable si esta en la posicion del pj
def recolectar_coleccionables(x , y):
    posicion_pj = ( x , y )
    for posicion in posiciones_coleccionables :
        if  posicion_pj == posicion :
            posiciones_coleccionables.remove(posicion)

# Comprueba colicion con enemigo
def contacto_enemigo(x , y):
    pos_enemigos = posiciones_muk + posiciones_voltorb
    posicion_pj = ( x , y )
    i = 10
    for posicion in pos_enemigos :
        interfaz.dibujar_texto(screen, str(posicion), 0, i)
        if posicion == posicion_pj :
            return True
        i = i + 20
    return False    
        
def mover_personaje(camino_final,pos_personaje_x,pos_personaje_y):
    
    for nodo in camino_final:
        posicion_nodo_x, posicion_nodo_y = nodo
        dif_posicion_x= posicion_nodo_x-pos_personaje_x
        dif_posicion_y= posicion_nodo_y-pos_personaje_y
        # recolectar_coleccionables(pos_personaje_x,pos_personaje_y)
        
        if(dif_posicion_x >= 0 and dif_posicion_y>=0):
            
            for i in range(dif_posicion_x):
                pos_personaje_x+=1
               
                # mover_personaje_derecha()
                
            for j in range(dif_posicion_y):
                pos_personaje_y+=1
                # mover_personaje_abajo()
                
            
            # thread_derecha.join()
        if (dif_posicion_x<0 and dif_posicion_y<0):
            for i in range(dif_posicion_x*-1):
                pos_personaje_x-=1
                # mover_personaje_izquierda()
               
                
            for j in range(dif_posicion_y*-1):
                pos_personaje_y-=1
                # mover_personaje_arriba()
                
        if(dif_posicion_x<0 and dif_posicion_y>=0):
            for i in range(dif_posicion_x*-1):
                pos_personaje_x-=1
                
            for j in range(dif_posicion_y):
                pos_personaje_y+=1
               
            
        if(dif_posicion_x>=0 and dif_posicion_y<0):
            for i in range(dif_posicion_x):
                pos_personaje_x+=1
                
            for j in range(dif_posicion_y*-1):
                pos_personaje_y-=1
                
        
def mover_personaje_derecha():
    right_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
    pygame.event.post(right_event)
    pygame.event.poll()
    direccion = "derecha"
    
def mover_personaje_izquierda():
    left_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    pygame.event.post(left_event)
    
    direccion = "izquierda"
def mover_personaje_arriba():
    up_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
    pygame.event.post(up_event)
   
    direccion = "arriba"
def mover_personaje_abajo():
    down_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
    pygame.event.post(down_event)
    
    direccion = "abajo"
def distancia_entre_puntos(x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia
def reiniciar_juego():
    frames_per_second = 20  # Velocidad de cambio de frames por segundo
    time_elapsed = 0
    frame = 0
    
    posiciones_personaje = [(1,1), (1,8), (8,1), (8,8)]
    pos_personaje_x, pos_personaje_y = random.choice(posiciones_personaje)

    pos_personaje__final = algoritoAEstrella.Nodo(pos_personaje_x,pos_personaje_y)
    posiciones_coleccionables = [(random.randrange(1, 9), random.randrange(1, 9)) for _ in range(10)]
    screen.fill(FONDO)
    draw_map(mapaJuego)
    colocar(posiciones_coleccionables)
    colocar_enemigos( posiciones_muk, posiciones_coleccionables, frame_index_muk, muk )
    colocar_enemigos( posiciones_voltorb, posiciones_coleccionables, frame_index_voltorb, voltorb )
    personaje_ancho, personaje_alto = CELL_SIZE // 1.5, CELL_SIZE // 1.5 
    personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5 
    personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
    
    bayas_pos_x = 4 * CELL_SIZE
    bayas_pos_y = 8 * CELL_SIZE
    screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
    screen.blit( bayas[frame_index_bayas], (bayas_pos_x, bayas_pos_y) ) 
    pygame.display.update()
    
    # interfaz.dibujar_interface( screen , costo , vidas  )
    # Función principal del juego

def main():
    clock = pygame.time.Clock()  # Crear un objeto para ayudar a controlar el tiempo
    frames_per_second = 20  # Velocidad de cambio de frames por segundo
    time_elapsed = 0
    frame = 0    

    global pos_personaje_x, pos_personaje_y, direccion , vidas , costo, ruta_optima, posiciones_coleccionables, movimiento_on, elemento_tupla, num_elemento    # Para modificar las variables globales
    global se_esta_recargando, se_termino_de_recargar
    global camino_a_pila_aux
    camino_a_pila_aux = []
    movimiento_on= False
    num_elemento=0
    se_esta_recargando=False
    se_termino_de_recargar= False
    vidas = VIDAS_MAX # Para cambiar la vida y bateria maxima ir a interfaz.py
    costo = 0  
    running = True
       
    while running:
        if(movimiento_on==True and ruta_optima is not None and len(ruta_optima)>0):
            
            dif_posicion_x_pila= 4 - pos_personaje_x
            dif_posicion_y_pila= 8-pos_personaje_y
            posicion_pila=[(4,8)]
       
            nodo_jugador=algoritoAEstrella.Nodo(pos_personaje_x,pos_personaje_y)
            if(se_esta_recargando==False):
                camino_a_pila= algoritoAEstrella.a_estrella(mapaJuego,nodo_jugador,posicion_pila)
                # print("Camino Aux:", camino_a_pila)
                camino_a_pila.reverse()
            distancia_entre_nodos = len(camino_a_pila)
            print("pos_jugador: ",nodo_jugador.x,nodo_jugador.y)
            print("Distancia: ", distancia_entre_nodos)
            if(se_termino_de_recargar==True):
                tamano = len(camino_a_pila_aux)
                if(tamano != 0):
                    nodo_siguiente_pila= camino_a_pila_aux.pop()
                    print("Camino a de regreso: ", camino_a_pila_aux)
                    pos_personaje_x, pos_personaje_y = nodo_siguiente_pila
                else:
                    se_termino_de_recargar= False
            elif(distancia_entre_nodos>=19-costo):
                se_esta_recargando=True
                
                
                nodo_siguiente_pila= camino_a_pila.pop()
                print("Camino a la pila: ", camino_a_pila)
                camino_a_pila_aux.append(nodo_siguiente_pila)
                pos_personaje_x, pos_personaje_y = nodo_siguiente_pila
                
                if pos_personaje_x == 4 and pos_personaje_y == 8 :
                    vidas = VIDAS_MAX
                    costo = 0
                    se_termino_de_recargar=True
                    print("camino aux 2:", camino_a_pila_aux)
                    se_esta_recargando=False
            
            else:
                elemento_tupla= ruta_optima.pop()
                if(pos_personaje_x<elemento_tupla[0]):
                    direccion = "derecha"
                elif(pos_personaje_x>elemento_tupla[0]):
                    direccion="izquierda"
                elif(pos_personaje_y<elemento_tupla[1]):
                    direccion="abajo"
                else:
                    direccion="arriba"
                    
                # Recarga si esta en la estacion // ESTATICA //
                if pos_personaje_x == 4 and pos_personaje_y == 8 :
                    vidas = VIDAS_MAX
                    costo = 0
                # Quita una vida si choca con enemigos    
                # if contacto_enemigo( pos_personaje_x , pos_personaje_y ) :
                #     vidas = vidas -1  if vidas > 0 else 0
                # num_elemento+=1
            
                time.sleep(.2)
                pos_personaje_x,pos_personaje_y= elemento_tupla
                costo+=1
                recolectar_coleccionables(pos_personaje_x,pos_personaje_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:  # Manejar eventos de teclado
                costo +=  1  if costo < BATERIA_MAX else 0
                if event.key == pygame.K_UP:
                    if pos_personaje_y > 0 and mapaJuego[pos_personaje_y - 1][pos_personaje_x] == 0: 
                        pos_personaje_y -= 1
                        # time.sleep(0.125)
                        direccion = "arriba"
                elif event.key == pygame.K_DOWN:
                    if pos_personaje_y < len(mapaJuego) - 1 and mapaJuego[pos_personaje_y + 1][pos_personaje_x] == 0: 
                        pos_personaje_y += 1
                        # time.sleep(0.125)
                        direccion = "abajo"
                elif event.key == pygame.K_LEFT:
                    if pos_personaje_x > 0 and mapaJuego[pos_personaje_y][pos_personaje_x - 1] == 0: 
                        pos_personaje_x -= 1
                        # time.sleep(0.125)
                        direccion = "izquierda"
                elif event.key == pygame.K_RIGHT:
                    if pos_personaje_x < len(mapaJuego[0]) - 1 and mapaJuego[pos_personaje_y][pos_personaje_x + 1] == 0: 
                        pos_personaje_x += 1
                        # time.sleep(0.125)
                        direccion = "derecha"

           
            # Recarga si esta en la estacion // ESTATICA //
            elif pos_personaje_x == 4 and pos_personaje_y == 8 :
                vidas = VIDAS_MAX
                costo = 0

            # Quita una vida si choca con enemigos    
            elif contacto_enemigo( pos_personaje_x , pos_personaje_y ) :
                vidas = vidas -1  if vidas > 0 else 0
            
        

        # Dibujar el mapa del juego
        screen.fill(FONDO)
        draw_map(mapaJuego)
        colocar(posiciones_coleccionables)

       
        #recolectar_coleccionables ( pos_personaje_x, pos_personaje_y)

        personaje_ancho, personaje_alto = CELL_SIZE // 1.5, CELL_SIZE // 1.5 

        # Actualiza el estado del boton
        btn_start.update()
        if(vidas == 0):
            print("TE QUEDASTE SIN VIDAS!!")
            break

        # Calcular la posición del personaje en la casilla actual
        personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5 
        personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5

        bayas_pos_x = 4 * CELL_SIZE
        bayas_pos_y = 8 * CELL_SIZE

        time_elapsed += 1
        if time_elapsed >= frames_per_second:
            time_elapsed = 0
            frame = (frame + 1) % 2  # This line switches the frame between 0 and 1
            animate_imagen_3()
            animate_bayas()
            
            animate_muk()
            animate_voltorb()

        colocar_enemigos( posiciones_muk, posiciones_coleccionables, frame_index_muk, muk )
        colocar_enemigos( posiciones_voltorb, posiciones_coleccionables, frame_index_voltorb, voltorb )
        # btn_start.pressed= True
        if btn_start.pressed :
            movimiento_on = True
            interfaz.dibujar_texto( screen , "Buscando ... " , WIDTH / 2 - 80 , 10 )
            print("Lista coleccionables:",posiciones_coleccionables )
            print("Posicion jugador: ", pos_personaje__final.x, pos_personaje__final.y)
            ruta_optima = algoritoAEstrella.a_estrella(mapaJuego,pos_personaje__final,posiciones_coleccionables)
            
            if ruta_optima:
                print("Ruta óptima encontrada Final:", ruta_optima)
                ruta_optima.reverse()
            else:
                print("No se encontró una ruta válida.")
            # mover_personaje(ruta_optima,pos_personaje_x,pos_personaje_y)
            # if (ruta_optima is not None):
            #     for nodo in ruta_optima:
            #         if(vidas == 0):
            #             print("TE QUEDASTE SIN VIDAS!!")
            #             break
            #         recolectar_coleccionables(pos_personaje_x,pos_personaje_y)
            #         distancia_entre_nodos= distancia_entre_puntos(4,8,pos_personaje_x,pos_personaje_y)
            #         dif_posicion_x_pila= 4 - pos_personaje_x
            #         dif_posicion_y_pila= 8-pos_personaje_y
            #         posicion_pila=[(4,8)]
            #         nodo_jugador=algoritoAEstrella.Nodo(pos_personaje_x,pos_personaje_y)
            #         if(distancia_entre_nodos>19-costo):
            #             algoritoAEstrella.a_estrella(mapaJuego,nodo_jugador,posicion_pila)
            #             if(dif_posicion_x_pila>=0 and dif_posicion_y_pila>=0):
            #                 for i in range(dif_posicion_x_pila):
            #                     pos_personaje_x+=1
            #                     costo +=  1
            #                     # mover_personaje_derecha()
            #                     direccion = "derecha"
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
                                
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y_pila):
            #                     pos_personaje_y+=1
            #                     costo +=  1
            #                     direccion = "abajo"
            #                     # mover_personaje_abajo()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #             if(dif_posicion_x_pila<0 and dif_posicion_y_pila<0):
            #                 for i in range(dif_posicion_x_pila*-1):
            #                     pos_personaje_x-=1
            #                     costo +=  1
            #                     direccion = "izquierda"
            #                     # mover_personaje_izquierda()
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5 
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y_pila*-1):
            #                     pos_personaje_y-=1
            #                     costo +=  1
            #                     direccion = "arriba"
            #                     # mover_personaje_arriba()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #             if(dif_posicion_x_pila<0 and dif_posicion_y_pila>=0):
            #                 for i in range(dif_posicion_x_pila*-1):
            #                     pos_personaje_x-=1
            #                     costo +=  1
            #                     direccion = "izquierda"
            #                     # mover_personaje_izquierda()
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y_pila):
            #                     pos_personaje_y+=1
            #                     costo +=  1
            #                     direccion = "abajo"
            #                     # mover_personaje_abajo()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #             if(dif_posicion_x_pila>=0 and dif_posicion_y_pila<0):
            #                 for i in range(dif_posicion_x_pila):
            #                     pos_personaje_x+=1
            #                     costo +=  1
            #                     # mover_personaje_derecha()
            #                     direccion = "derecha"
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5 
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y_pila*-1):
            #                     pos_personaje_y-=1
            #                     costo +=  1
            #                     direccion = "arriba"
            #                     # mover_personaje_arriba()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #             if(pos_personaje_x==4 and pos_personaje_y==8):
            #                 costo=0
            #         else: 
            #             posicion_nodo_x, posicion_nodo_y = nodo
            #             dif_posicion_x= posicion_nodo_x-pos_personaje_x
            #             dif_posicion_y= posicion_nodo_y-pos_personaje_y
                    
                        
                        
            #             if(dif_posicion_x >= 0 and dif_posicion_y>=0):
                            
            #                 for i in range(dif_posicion_x):
            #                     pos_personaje_x+=1
            #                     costo +=  1
            #                     # mover_personaje_derecha()
            #                     direccion = "derecha"
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y):
            #                     pos_personaje_y+=1
            #                     costo +=  1
            #                     direccion = "abajo"
            #                     # mover_personaje_abajo()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5    
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 # thread_derecha.join()
            #             if (dif_posicion_x<0 and dif_posicion_y<0):
            #                 for i in range(dif_posicion_x*-1):
            #                     pos_personaje_x-=1
            #                     direccion = "izquierda"
            #                     # mover_personaje_izquierda()
            #                     costo +=  1
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) ) 
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y*-1):
            #                     pos_personaje_y-=1
            #                     costo +=  1
            #                     direccion = "arriba"
            #                     # mover_personaje_arriba()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #             if(dif_posicion_x<0 and dif_posicion_y>=0):
            #                 for i in range(dif_posicion_x*-1):
            #                     pos_personaje_x-=1
            #                     costo +=  1
            #                     direccion = "izquierda"
            #                     # mover_personaje_izquierda()
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y):
            #                     pos_personaje_y+=1
            #                     costo +=  1
            #                     direccion = "abajo"
            #                     # mover_personaje_abajo()
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #             if(dif_posicion_x>=0 and dif_posicion_y<0):
            #                 for i in range(dif_posicion_x):
            #                     pos_personaje_x+=1
            #                     costo +=  1
            #                     direccion = "derecha"
            #                     # mover_personaje_derecha()
            #                     personaje_pos_x = pos_personaje_x * CELL_SIZE + (CELL_SIZE - personaje_ancho) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)
            #                 for j in range(dif_posicion_y*-1):
            #                     pos_personaje_y-=1
            #                     costo +=  1
            #                     direccion = "arriba"
            #                     # mover_personaje_arriba()
            #                     # mover_personaje(ruta_optima)
            #                     personaje_pos_y = pos_personaje_y * CELL_SIZE + (CELL_SIZE - personaje_alto) // 1.5
            #                     screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
            #                     pygame.display.update()
            #                     clock.tick(5)

                btn_start.pressed=False
                # btn_start.update()
                
            
            btn_start.pressed = False
            
        if costo == BATERIA_MAX  or not posiciones_coleccionables or vidas == 0:
            btn_start.pressed = False
        
        screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )

        screen.blit( bayas[frame_index_bayas], (bayas_pos_x, bayas_pos_y) )        

        interfaz.dibujar_interface( screen , costo , vidas  )
        btn_reinicio.update()
        # btn_reinicio.pressed= False
        if btn_reinicio.pressed:
            
            btn_reinicio.pressed=False
            btn_reinicio.update()
            reiniciar_juego()
            posiciones_personaje = [(1,1), (1,8), (8,1), (8,8)]
            # posiciones_personaje = [(1,8)]
            pos_personaje_x, pos_personaje_y = random.choice(posiciones_personaje)      
            posiciones_coleccionables = [(random.randrange(1, 9), random.randrange(1, 9)) for _ in range(10)]
            colocar(posiciones_coleccionables)
            costo=0
            vidas=VIDAS_MAX
            # # pygame.display.update()
            

        pygame.display.update()
        # clock.tick(15)

    pygame.quit()

if __name__ == "__main__":
    main()
    
