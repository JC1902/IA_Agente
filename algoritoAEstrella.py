import heapq

class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')
        self.h = 0
        self.f = 0
        self.padre = None

    def __lt__(self, otro):
        return self.f < otro.f

def distancia_manhattan(nodo_actual, nodo_destino):
    return abs(nodo_actual.x - nodo_destino[0]) + abs(nodo_actual.y - nodo_destino[1])

def obtener_vecinos(nodo, grid):
    vecinos = []
    direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Movimientos arriba, abajo, izquierda, derecha
    for dx, dy in direcciones:
        nx, ny = nodo.x + dx, nodo.y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[ny][nx] != 1 and grid[ny][nx] != 2 and grid[ny][nx] != 3:
            vecinos.append(Nodo(nx, ny))
    return vecinos

def a_estrella(grid, inicio, metas):
    cola_abierta = []
    cola_cerrada = []
    metas_por_alcanzar = list(metas)
    # cola_abierta.append(inicio)
    cola_cerrada.append(inicio)
    inicio.g = 0
    camino_completado=False
    nodo_menor_costo=None
    nodo_esta_en_lista=False
    while (camino_completado==False):
        nodo_actual = cola_cerrada.__getitem__(len(cola_cerrada)-1)
        # if not metas_por_alcanzar:
        #         camino_completado=True
        #         return cola_cerrada
        # if not metas_por_alcanzar:
        #     camino_completado=True
        #     return devolver_camino(cola_cerrada)
        if (nodo_actual.x, nodo_actual.y) in metas_por_alcanzar:
            metas_por_alcanzar.remove((nodo_actual.x, nodo_actual.y))
            if not metas_por_alcanzar:
                return devolver_camino(cola_cerrada)

        for vecino in obtener_vecinos(nodo_actual, grid):
            for vecinoAux in cola_cerrada:
                if(vecinoAux.x==vecino.x and vecinoAux.y==vecino.y):
                    nodo_esta_en_lista=True
                    break
                else:
                    nodo_esta_en_lista=False
            if(nodo_esta_en_lista==False):
                nuevo_g = nodo_actual.g + 1  # Costo de movimiento uniforme

                vecino.g = nuevo_g
                vecino.h = min(distancia_manhattan(vecino, meta) for meta in metas)
                vecino.f = vecino.g + vecino.h
                vecino.padre = nodo_actual
                cola_abierta.append(vecino)
        for vecino in cola_abierta:
            if(nodo_menor_costo is None):
                nodo_menor_costo= vecino
            if (vecino.f<nodo_menor_costo.f):
                nodo_menor_costo=vecino
        if(nodo_menor_costo is None):
            nodo_menor_costo=cola_cerrada.__getitem__(len(cola_cerrada)-1).padre
        
        cola_cerrada.append(nodo_menor_costo)
        cola_abierta.clear()
        nodo_menor_costo=None

    return None

def devolver_camino(camino):
    camino_final= []
    for nodo in camino:
        camino_final.append((nodo.x,nodo.y))
    return camino_final


# Ejemplo de uso:
# grid = [
#     [0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 1],
#     [0, 1, 1, 0, 0],
#     [0, 0, 0, 0, 0]
# ]

# inicio = Nodo(0, 0)
# metas = {(4, 4), (2, 2), (3, 3), (1, 1),(4,3),(3,4)}

# ruta_optima = a_estrella(grid, inicio, metas)
# ruta_formateada=devolver_camino(ruta_optima)
# if ruta_optima:
#     print("Ruta óptima encontrada:", ruta_formateada)
# else:
#     print("No se encontró una ruta válida.")
