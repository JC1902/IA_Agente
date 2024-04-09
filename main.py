import pygame
import algoritoAEstrella
from assets import *
import random
import time
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
btn_reinicio = Button( screen, 500, 800, 'Reiniciar',100,40 )


# Matriz del juego
mapaJuego = [
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 0, 0, 0, 2, 0, 0, 0, 0, 1 ],
    [ 1, 0, 0, 0, 3, 0, 0, 2, 0, 1 ],
    [ 1, 0, 3, 0, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 0, 0, 2, 2, 0, 2, 0, 1 ],
    [ 1, 0, 3, 0, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 2, 0, 0, 0, 0, 0, 0, 1 ],
    [ 1, 0, 2, 0, 0, 0, 2, 0, 3, 1 ],
    [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
]

# Posiciones posible para el personaje
posiciones_personaje = [ ( 1,1 ), ( 1,8 ), ( 8,1 ), ( 8,8 ) ]
pos_personaje_x, pos_personaje_y = random.choice( posiciones_personaje )
nodo_jugador = algoritoAEstrella.Nodo( pos_personaje_x, pos_personaje_y )

# Dirección inicial del personaje
if ( pos_personaje_x, pos_personaje_y ) == ( 1,1 ) or ( pos_personaje_x, pos_personaje_y ) == ( 8,1 ):
    direccion = "abajo"
else:
    direccion = "arriba"

# Almacenar la posición anterior del personaje
old_pos_personaje_x, old_pos_personaje_y = pos_personaje_x, pos_personaje_y

# Fuera de la función colocar(), define un arreglo para las posiciones de los coleccionables
posiciones_coleccionables = [ ( random.randrange( 1, 9 ), random.randrange( 1, 9 ) ) for _ in range( 10 ) ]

def colocar( posiciones ):
    ancho_collec, alto_collect = CELL_SIZE // 1.5, CELL_SIZE // 1.5

    i = 0
    while i < len( posiciones ):

        pos_x, pos_y = posiciones[ i ]

        # Verificar si la posición aleatoria coincide con la posición de las bayas o si el valor de la posición en la matriz es 3
        if ( pos_x, pos_y ) != ( 4, 8 ) and \
            mapaJuego[ pos_y ][ pos_x ] != 3 and \
            ( pos_x, pos_y ) not in posiciones_personaje and \
            mapaJuego[ pos_y ][ pos_x ] != 2:
            # Calcular la posición del coleccionable en la casilla actual
            collec_pos_x = pos_x * CELL_SIZE + ( CELL_SIZE - ancho_collec ) 
            collec_pos_y = pos_y * CELL_SIZE + ( CELL_SIZE - alto_collect )
            screen.blit( coleccionables[ i ], ( collec_pos_x, collec_pos_y ) )
            i += 1
        else:
            while True:
                pos_x = random.randrange( 1, 9 )
                pos_y = random.randrange( 1, 9 )
                if ( pos_x, pos_y ) not in posiciones:
                    break
            posiciones[ i ] = ( pos_x, pos_y )

            # Calcular la posición del coleccionable en la nueva casilla
            collec_pos_x = pos_x * CELL_SIZE + ( CELL_SIZE - ancho_collec ) 
            collec_pos_y = pos_y * CELL_SIZE + ( CELL_SIZE - alto_collect )
            screen.blit(coleccionables[ i ], ( collec_pos_x, collec_pos_y ) )


# Define el índice del frame actual de la animación de la imagen_3
frame_index_imagen_3, frame_index_bayas = 0, 0

# Función para animar la imagen_3
def animate_imagen_3():
    global frame_index_imagen_3
    frame_index_imagen_3 = ( frame_index_imagen_3 + 1 ) % len( snorlax_tierra )

def animate_bayas():
    global frame_index_bayas
    frame_index_bayas = ( frame_index_bayas + 1 ) % len( bayas )

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
        frame_index_muk = ( frame_index_muk + 1 ) % len( muk )
        muk_animation_counter = 0

# Función para animar a Voltorb
def animate_voltorb():
    global frame_index_voltorb, voltorb_animation_counter

    voltorb_animation_counter += 1
    if voltorb_animation_counter >= voltorb_animation_speed:
        frame_index_voltorb = ( frame_index_voltorb + 1 ) % len( voltorb )
        voltorb_animation_counter = 0
        
# Establece las posiciones de los enemigos
posiciones_muk = [ ( random.randrange( 1, 9 ), random.randrange( 1, 9 ) ) for _ in range( 2 )]
posiciones_voltorb = [ ( random.randrange( 1, 9 ), random.randrange( 1, 9 ) ) for _ in range( 2 )]

# Funcion la cual coloca los enemigos en el mapa
def colocar_enemigos( posiciones_enemigos, posiciones_colectables, frame_enemigo, enemigo_images ):
    ancho_enemigo, alto_enemigo = 40 , 40

    if posiciones_enemigos == posiciones_muk:
        posiciones_ocupadas = set( posiciones_colectables ) | set( posiciones_voltorb ) | set( posiciones_personaje )
    elif posiciones_enemigos == posiciones_voltorb:
        posiciones_ocupadas = set( posiciones_colectables ) | set( posiciones_muk ) | set( posiciones_personaje )

    for i, ( pos_x, pos_y ) in enumerate( posiciones_enemigos ):
        while ( pos_x, pos_y ) in posiciones_ocupadas or \
                mapaJuego[ pos_y ][ pos_x ] in [ 2, 3 ] or \
                ( pos_x, pos_y ) == ( 4, 8 ):
            pos_x = random.randrange( 1, 9 )
            pos_y = random.randrange( 1, 9 )
        
        posiciones_enemigos[ i ] = ( pos_x, pos_y )
        posiciones_ocupadas.add( ( pos_x, pos_y ) )

        enemigo_pos_x = pos_x * CELL_SIZE + ( CELL_SIZE - ancho_enemigo ) // 2
        enemigo_pos_y = pos_y * CELL_SIZE + ( CELL_SIZE - alto_enemigo ) // 2
        screen.blit(enemigo_images[ frame_enemigo ], ( enemigo_pos_x, enemigo_pos_y ) )


tipo_piso = []

index_pisos = 0

# Intercambia los 0 por diferentes numeros, para agregar diferente tipo de suelo
for y, row in enumerate( mapaJuego ):
        for x, cell in enumerate( row ):
            if cell == 0:
                piso = random.choice( [ tierra, tierra, pasto, lodo ] )
                tipo_piso.append( piso )
                


for y, row in enumerate( mapaJuego ):
    for x, cell in enumerate( row ):
        if cell == 0:
            if tipo_piso[ index_pisos ] == tierra:
                mapaJuego[ y ][ x ] = 4
            
            if tipo_piso[ index_pisos ] == pasto:
                mapaJuego[ y ][ x ] = 5

            if tipo_piso[ index_pisos ] == lodo:
                mapaJuego[ y ][ x ] = 6
        
            index_pisos += 1


# Función para dibujar el mapa del juego
def draw_map( mapa ):

    index = 0

    for y, row in enumerate( mapa ):
        for x, cell in enumerate( row ):
            
            if cell == 1:
                screen.blit( arbol_pasto, ( x * CELL_SIZE, y * CELL_SIZE ) )
            if cell == 2:
                screen.blit( arbol_tierra, ( x * CELL_SIZE, y * CELL_SIZE ) )
            if cell == 3:
                screen.blit( snorlax_tierra[ frame_index_imagen_3 ], ( x * CELL_SIZE, y * CELL_SIZE ) )
            if cell == 4:
                screen.blit( tierra, ( x * CELL_SIZE, y * CELL_SIZE ) )
            if cell == 5:
                screen.blit( pasto, ( x * CELL_SIZE, y * CELL_SIZE ) )
            if cell == 6:
                screen.blit( lodo, ( x * CELL_SIZE, y * CELL_SIZE ) )



# Elimina el colecionable si esta en la posicion del pj
def recolectar_coleccionables( x , y ):
    posicion_pj = ( x , y )
    for posicion in posiciones_coleccionables :
        if  posicion_pj == posicion :
            posiciones_coleccionables.remove( posicion )

# Comprueba colicion con enemigo
def contacto_enemigo( x , y ):
    pos_enemigos = posiciones_muk + posiciones_voltorb
    posicion_pj = ( x , y )
    i = 10
    for posicion in pos_enemigos :
        
        if posicion == posicion_pj :
            return True
        i = i + 20

    return False    
        
# Funcion la cual reinicia el juego
def reiniciar_juego():
    
    frame = 0
    
    posiciones_personaje = [ ( 1,1 ), ( 1,8 ), ( 8,1 ), ( 8,8 ) ] 
    pos_personaje_x, pos_personaje_y = random.choice( posiciones_personaje )

    
    posiciones_coleccionables = [ ( random.randrange( 1, 9 ), random.randrange ( 1, 9 ) ) for _ in range( 10 )]
    screen.fill( FONDO )
    draw_map( mapaJuego )
    colocar( posiciones_coleccionables )
    colocar_enemigos( posiciones_muk, posiciones_coleccionables, frame_index_muk, muk )
    colocar_enemigos( posiciones_voltorb, posiciones_coleccionables, frame_index_voltorb, voltorb )
    personaje_ancho, personaje_alto = CELL_SIZE // 1.5, CELL_SIZE // 1.5 
    personaje_pos_x = pos_personaje_x * CELL_SIZE + ( CELL_SIZE - personaje_ancho ) // 1.5 
    personaje_pos_y = pos_personaje_y * CELL_SIZE + ( CELL_SIZE - personaje_alto ) // 1.5
    
    bayas_pos_x = 4 * CELL_SIZE
    bayas_pos_y = 8 * CELL_SIZE
    screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )
    screen.blit( bayas[ frame_index_bayas ], (bayas_pos_x, bayas_pos_y) ) 
    pygame.display.update()
    
   
   
# Función principal del juego

def main():
   
    frames_per_second = 20  # Velocidad de cambio de frames por segundo
    time_elapsed = 0
    frame = 0    

    # Se inicializan las variables globales a utilizar
    global pos_personaje_x, pos_personaje_y, direccion , vidas , costo, ruta_optima, posiciones_coleccionables, movimiento_on, elemento_tupla, num_elemento    # Para modificar las variables globales
    global se_esta_recargando, se_termino_de_recargar
    global camino_a_pila_aux
    global nodo_jugador
    global primer_ruta
    camino_a_pila_aux = []
    movimiento_on = False
    num_elemento = 0
    se_esta_recargando = False
    se_termino_de_recargar = False
    vidas = VIDAS_MAX # Para cambiar la vida y bateria maxima ir a interfaz.py
    costo = 0  
    running = True
       
    while running:
        
        # Se comprueba si el costo supero la bateria para detener el juego
        if costo>BATERIA_MAX :
            interfaz.dibujar_texto( screen , "Te quedaste sin energia " , 350 , 400 )
            pygame.display.update()
        # Se comprueba si se acabo de recoger todos los coleccionables para mostrar el mensaje de victoria
        if( len( posiciones_coleccionables ) == 0 ):
            interfaz.dibujar_texto( screen , " HAS GANADO!! " , 350 , 400 )
            pygame.display.update()
        # Se comprueba si tuvo un contacto con el enemigo
        if contacto_enemigo( pos_personaje_x , pos_personaje_y ) :
            vidas = vidas -1  if vidas > 0 else 0
            
        # Determina si el boton de inicio fue presionado y comienza el movimiento
        
        if( movimiento_on == True and ruta_optima is not None and len( ruta_optima ) !=0 and len( ruta_optima ) > 0):
            interfaz.dibujar_texto( screen , "Buscando ... " , WIDTH / 2 - 80 , 10 )
            pygame.display.update()
                     
            posicion_pila=[ ( 4,8 ) ]
       
            nodo_jugador=algoritoAEstrella.Nodo( pos_personaje_x, pos_personaje_y )
            # Comprueba si no se encuentra recargando para calcular una ruta a la bateria
            if( se_esta_recargando == False ):
                camino_a_pila= algoritoAEstrella.a_estrella( mapaJuego, nodo_jugador, posicion_pila )
                
                camino_a_pila.reverse()
                camino_a_pila.pop()
            distancia_entre_nodos = len( camino_a_pila )
            print( "pos_jugador: ", nodo_jugador.x, nodo_jugador.y )
            print( "Distancia: ", distancia_entre_nodos)
            
            # En este if se hace el regreso hacia la pila 
            if( ( distancia_entre_nodos >= 40 - costo and se_termino_de_recargar is False ) or vidas < 2 ):
                 
                se_esta_recargando = True

                # If que realiza lo siguiente:
                # Si solo le queda un coleccionable y tiene energia suficiente, acude al coleccionable
                if( len( posiciones_coleccionables ) == 1 ):
                    elemento_lista_coleccionable = posiciones_coleccionables[ 0 ]
                    print( "Elemento lista: ", elemento_lista_coleccionable )
                    ruta_auxiliar_un_coleccionable = algoritoAEstrella.a_estrella( mapaJuego,nodo_jugador, posiciones_coleccionables )
                    tamano_ruta = len( ruta_auxiliar_un_coleccionable )
                    
                    #If el cual determina si el camino al coleccionable es menor a la energia restante
                    if( tamano_ruta < 60 - costo ):

                        # Genera una nueva ruta al ultimo coleccionable
                        if primer_ruta is True:
                            ruta_optima= algoritoAEstrella.a_estrella( mapaJuego, nodo_jugador, posiciones_coleccionables )
                            primer_ruta=False
                            ruta_optima.reverse()
                            ruta_optima.pop()

                        time.sleep(.2)
                        nodo_sig= ruta_optima.pop()

                        # Establece las direcciones
                        if( pos_personaje_x < nodo_sig[ 0 ] ):
                            direccion = "derecha"
                        elif( pos_personaje_x > nodo_sig[ 0 ] ):
                            direccion = "izquierda"
                        elif( pos_personaje_y < nodo_sig[ 1 ] ):
                            direccion = "abajo"
                        else:
                            direccion = "arriba"

                        # Mueve el personaje al siguiente nodo
                        pos_personaje_x, pos_personaje_y = nodo_sig
                        recolectar_coleccionables( pos_personaje_x, pos_personaje_y )
                        
                    
                else:   
                    #Se establece el estado de recargando al juego
                    interfaz.dibujar_texto( screen , "Recargando ... " , 80 , 10 )
                    print( "Recargando" )
                    pygame.display.update()

                    nodo_siguiente_pila = camino_a_pila.pop()
                    print( "Camino a la pila: ", camino_a_pila )
                    camino_a_pila_aux.append( nodo_siguiente_pila )
                    time.sleep( .2 )

                    # Establece las direcciones del personaje
                    if( pos_personaje_x < nodo_siguiente_pila[ 0 ] ):
                        direccion = "derecha"
                    elif( pos_personaje_x > nodo_siguiente_pila[ 0 ] ):
                        direccion = "izquierda"
                    elif( pos_personaje_y < nodo_siguiente_pila[ 1 ] ):
                        direccion = "abajo"
                    else:
                        direccion = "arriba"

                    # Mueve el personaje al siguiente nodo
                    pos_personaje_x, pos_personaje_y = nodo_siguiente_pila
                    recolectar_coleccionables( pos_personaje_x, pos_personaje_y )
                    
                    # Si el personaje llego a la pila, recarga sus vidas y su energia
                    if pos_personaje_x == 4 and pos_personaje_y == 8 :
                        vidas = VIDAS_MAX
                        costo = 0
                        
                        print( "camino aux 2:", camino_a_pila_aux )
                        se_esta_recargando = False
                         
                        nodo_pos_personaje = algoritoAEstrella.Nodo( pos_personaje_x, pos_personaje_y )
                        ruta_optima = algoritoAEstrella.a_estrella( mapaJuego,nodo_pos_personaje, posiciones_coleccionables )
                        ruta_optima.reverse()
                        ruta_optima.pop()
            else:
                # Recorrido normal de la ruta sin recurrir a la pila
                elemento_tupla= ruta_optima.pop()

                if( pos_personaje_x < elemento_tupla[ 0 ] ):
                    direccion = "derecha"
                elif( pos_personaje_x > elemento_tupla[ 0 ] ):
                    direccion = "izquierda"
                elif( pos_personaje_y < elemento_tupla[ 1 ] ):
                    direccion = "abajo"
                else:
                    direccion = "arriba"
                    
                # Recarga si esta en la estacion // ESTATICA //
                if pos_personaje_x == 4 and pos_personaje_y == 8 :
                    vidas = VIDAS_MAX
                    costo = 0
                
                time.sleep( .2 )
                pos_personaje_x,pos_personaje_y = elemento_tupla

                if pos_personaje_x == 4 and pos_personaje_y == 8 :
                    vidas = VIDAS_MAX
                    costo = 0

                recolectar_coleccionables(pos_personaje_x,pos_personaje_y)

            # Establece el costo por cada tipo de piso
            if mapaJuego[ pos_personaje_x ][ pos_personaje_y ] == 6:
                costo += 3
            elif mapaJuego[ pos_personaje_x ][ pos_personaje_y ] == 4:
                costo += 2
            else:
                costo += 1
           
            
            recolectar_coleccionables(pos_personaje_x,pos_personaje_y)

        # El programa estara alerta de cualquier evento que pase ene el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            

        # Dibujar el mapa del juego
        screen.fill( FONDO )
        draw_map( mapaJuego )
        colocar( posiciones_coleccionables )

        personaje_ancho, personaje_alto = CELL_SIZE // 1.5, CELL_SIZE // 1.5 

        # Actualiza el estado del boton
        btn_start.update()
        if( vidas == 0 ):
            interfaz.dibujar_texto( screen , "TE QUEDASTE SIN VIDAS!! " , 300 , 400 )
            
            pygame.display.update()
            pygame.time.delay( 5000 )
            break

        # Calcular la posición del personaje en la casilla actual
        personaje_pos_x = pos_personaje_x * CELL_SIZE + ( CELL_SIZE - personaje_ancho ) // 1.5 
        personaje_pos_y = pos_personaje_y * CELL_SIZE + ( CELL_SIZE - personaje_alto ) // 1.5

        bayas_pos_x = 4 * CELL_SIZE
        bayas_pos_y = 8 * CELL_SIZE

        time_elapsed += 1
        
        # Genera las animaciones de todos los elementos del juego
        if time_elapsed >= frames_per_second:
            time_elapsed = 0
            frame = ( frame + 1 ) % 2  
            animate_imagen_3()
            animate_bayas()
            
            animate_muk()
            animate_voltorb()

        colocar_enemigos( posiciones_muk, posiciones_coleccionables, frame_index_muk, muk )
        colocar_enemigos( posiciones_voltorb, posiciones_coleccionables, frame_index_voltorb, voltorb )
        
        # Si el boton de inicio es presionado, comienza el juego
        if btn_start.pressed :
            movimiento_on = True
            primer_ruta = True
            print( "Lista coleccionables:",posiciones_coleccionables )
            print( "Posicion jugador: ", nodo_jugador.x,nodo_jugador.y )
            ruta_optima = algoritoAEstrella.a_estrella( mapaJuego,nodo_jugador, posiciones_coleccionables )
            
            
            if ruta_optima:
                print( "Ruta óptima encontrada Final:", ruta_optima )
                ruta_optima.reverse()
                ruta_optima.pop()
            else:
                print( "No se encontró una ruta válida." )
          

                btn_start.pressed = False
                
                
            
            btn_start.pressed = False
            
        if costo == BATERIA_MAX  or not posiciones_coleccionables or vidas == 0:
            btn_start.pressed = False
        
        # Dibuja al personaje y los coleccionables
        screen.blit( personajes[ direccion ][ frame ], ( personaje_pos_x, personaje_pos_y ) )

        screen.blit( bayas[ frame_index_bayas ], ( bayas_pos_x, bayas_pos_y ) )        

        interfaz.dibujar_interface( screen , costo , vidas  )
        btn_reinicio.update()
        
        # Si el boton de reinicio es presionado, se reestablece el juego
        if btn_reinicio.pressed:
            
            btn_reinicio.pressed = False
            btn_reinicio.update()
            reiniciar_juego()
            posiciones_personaje = [ ( 1,1 ), ( 1,8 ), ( 8,1 ), ( 8,8 ) ]
            
            pos_personaje_x, pos_personaje_y = random.choice( posiciones_personaje ) 
            nodo_jugador=algoritoAEstrella.Nodo( pos_personaje_x, pos_personaje_y )     
            posiciones_coleccionables = [ ( random.randrange( 1, 9 ), random.randrange( 1, 9 ) ) for _ in range( 10 ) ]
            colocar( posiciones_coleccionables )
            costo = 0
            camino_a_pila = []
            se_esta_recargando = False
            ruta_optima = []
            vidas = VIDAS_MAX
            
        
        # Actualiza el juego
        pygame.display.update()
        
    # Termina el juego
    pygame.quit()

if __name__ == "__main__":
    main()
    
