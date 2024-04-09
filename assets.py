import pygame

# Dimensiones de la celda
CELL_SIZE = 80

# Cargar las imágenes de los pisos
tierra = pygame.image.load( 'pisos/tierra.png' )
tierra = pygame.transform.scale( tierra, ( CELL_SIZE, CELL_SIZE ) )

pasto = pygame.image.load( 'pisos/pasto.png' )
pasto = pygame.transform.scale( pasto, ( CELL_SIZE, CELL_SIZE ) )

lodo = pygame.image.load( 'pisos/lodo.png' )
lodo = pygame.transform.scale( lodo, ( CELL_SIZE, CELL_SIZE ) )

# Cargar las imagenes de las bayas para cargar la bateria
bayas = [pygame.image.load( f'pisos/bayas_{i}.png' ) for i in range( 3 ) ]
bayas = [ pygame.transform.scale( imagen, ( CELL_SIZE, CELL_SIZE ) ) for imagen in bayas ]

# Cargar las imágenes de los obstaculos
arbol_pasto = pygame.image.load( 'obstaculos/arbol_0.png' )
arbol_pasto = pygame.transform.scale( arbol_pasto, ( CELL_SIZE, CELL_SIZE ) )

arbol_tierra = pygame.image.load( 'obstaculos/arbol_1.png' )
arbol_tierra = pygame.transform.scale( arbol_tierra, ( CELL_SIZE, CELL_SIZE ) )

snorlax_tierra = [ pygame.image.load( f'obstaculos/snorlax_{i}.png') for i in range( 5 ) ]
snorlax_tierra = [pygame.transform.scale( imagen, ( CELL_SIZE, CELL_SIZE ) ) for imagen in snorlax_tierra ]

# Cargar las imagenes de los enemigos
muk = [ pygame.image.load( f'enemigos/MUK_{i}.png' ) for i in range( 3 ) ]

voltorb = [ pygame.image.load( f'enemigos/pozoV40_{i}.png' ) for i in range( 6 ) ]

# Cargar las imágenes del personaje
personaje_arriba = [pygame.image.load( f'pikachu/pikachu_arriba_{i}.png' ) for i in range( 2 ) ]
personaje_abajo = [pygame.image.load( f'pikachu/pikachu_abajo_{i}.png' ) for i in range( 2 ) ]
personaje_izquierda = [pygame.image.load( f'pikachu/pikachu_izq_{i}.png' ) for i in range( 2 ) ]
personaje_derecha = [pygame.image.load( f'pikachu/pikachu_der_{i}.png' ) for i in range( 2 ) ]

# Asignar las imagenes a una direccion en especifico
personajes = {
    "arriba": personaje_arriba,
    "abajo": personaje_abajo,
    "izquierda": personaje_izquierda,
    "derecha": personaje_derecha
}

# Escalar al personaje a un tamaño adecuado
personajes = { direccion: [ pygame.transform.scale( img, ( CELL_SIZE/1.5, CELL_SIZE/1.5 ) ) for img in sprites ] for direccion, sprites in personajes.items() }

# Cargar los coleccionables
coleccionables = [ pygame.image.load( f'coleccionables/cc{i}.png' ) for i in range( 10 ) ]


# Cargar la imagen para las vidas
img_vidas =  [ 
    pygame.transform.scale(
        pygame.image.load( f'interfaz/vida_{i}.png' ),
        ( 45  , 45 )
    ) for i in range(2)
 ]

#[pygame.image.load(f'interfaz/vida_{i}.png') for i in range(2)]

# Cargar y acomodar el medidor de la bateria
img_medidor = [
    pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load( f'interfaz/medidor/bateria_{i}.png' ),
            ( int( CELL_SIZE / 3 * 2 ), CELL_SIZE * 2 )
        ),
        90  
    )
    for i in range( 16 )
]
