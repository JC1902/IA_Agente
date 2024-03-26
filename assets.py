import pygame

# Dimensiones de la celda
CELL_SIZE = 80

# Cargar las imágenes de los pisos
imagen_0 = pygame.image.load('pisos/tierra.png')
imagen_0 = pygame.transform.scale(imagen_0, (CELL_SIZE, CELL_SIZE))
imagen_1 = pygame.image.load('pisos/pasto.png')
imagen_1 = pygame.transform.scale(imagen_1, (CELL_SIZE, CELL_SIZE))

# Cargar las imágenes de los obstáculos
imagen_2 = pygame.image.load('obstaculos/arbol_00.png')
imagen_2 = pygame.transform.scale(imagen_2, (CELL_SIZE, CELL_SIZE))
imagen_3 = pygame.image.load('obstaculos/sprite_45.png')
imagen_3 = pygame.transform.scale(imagen_3, (CELL_SIZE, CELL_SIZE))

# Cargar las imágenes del personaje
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

personajes = {direccion: [pygame.transform.scale(img, (CELL_SIZE/1.5, CELL_SIZE/1.5)) for img in sprites] for direccion, sprites in personajes.items()}

coleccionables = [pygame.image.load(f'coleccionables/cc{i}.png') for i in range(10)]



img_vidas = [pygame.image.load(f'interfaz/vida_{i}.png') for i in range(2)]

img_medidor = [
    pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(f'interfaz/medidor/bateria_{i}.png'),
            (int(CELL_SIZE / 3 * 2), CELL_SIZE * 2)
        ),
        90  
    )
    for i in range(16)
]
