# Creacion de la clase nodo, la cual nos servira para determinar la ruta mas optima
class Nodo:
    def __init__( self, x, y ):
        self.x = x
        self.y = y
        self.g = float( 'inf' )
        self.h = 0
        self.f = 0
        self.padre = None

# Funcion para calcular la distancia manhattan entre dos nodos
def distancia_manhattan( nodo_actual, nodo_destino ):
    return abs( nodo_actual.x - nodo_destino[ 0 ] ) + abs( nodo_actual.y - nodo_destino[ 1 ] )

# Obtiene los nodos vecinos del nodo actual
def obtener_vecinos( nodo, grid ):
    vecinos = []
    direcciones = [ ( -1, 0 ), ( 0, 1 ), ( 1, 0 ), ( 0, -1 ) ]  # Movimientos arriba, abajo, izquierda, derecha
    for dx, dy in direcciones:
        nx, ny = nodo.x + dx, nodo.y + dy
        if 0 <= nx < len( grid ) and 0 <= ny < len( grid[ 0 ] ) and grid[ ny ][ nx ] != 1 and grid[ ny ][ nx ] != 2 and grid[ ny ][ nx ] != 3:
            vecinos.append( Nodo( nx, ny ) )
    return vecinos

# Algoritmo a estrella, el cual nos regresa la ruta mas optima entre la posicion inicial y las metas asignadas
def a_estrella( grid, inicio, metas ):
    # Se inicializan las variables necesarias para el calculo de la ruta
    cola_abierta = []
    cola_cerrada = []
    metas_por_alcanzar = list( metas )
    cola_cerrada.append( inicio )
    inicio.g = 0
    camino_completado = False
    nodo_menor_costo = None
    nodo_esta_en_lista = False
    
    # Comienza el ciclo en while en el cual estara obteniendo la ruta mas optima
    while ( camino_completado == False ):
        nodo_actual = cola_cerrada.__getitem__( len( cola_cerrada ) - 1 )

        # Verifica si el nodo_actual es nulo
        if( nodo_actual is None ):
            break

        # Verifica si se alcanzo alguna meta para eliminarla del arreglo de las metas
        if ( nodo_actual.x, nodo_actual.y ) in metas_por_alcanzar:
            metas_por_alcanzar.remove( ( nodo_actual.x, nodo_actual.y ) )
            # Si ya se lograron todas las metas, regresa el camino optimo
            if not metas_por_alcanzar:
                return devolver_camino( cola_cerrada )
            
        # Ciclo el cual obtiene los vecinos del nodo actual
        for vecino in obtener_vecinos( nodo_actual, grid ):
            # Se verifica si el vecino ya esta en la cola cerrada para no agregarlo nuevamente
            for vecinoAux in cola_cerrada:
                if( vecinoAux.x == vecino.x and vecinoAux.y == vecino.y ):
                    nodo_esta_en_lista = True
                    break
                else:
                    nodo_esta_en_lista = False
            if( nodo_esta_en_lista == False ):
                if( metas ):
                    None
                else:
                    break

                # Se agrega el nuevo vecino a la cola abierta y asigna los diferentes costos, dependiendo del tipo de suelo    
                if grid[ vecino.x ][ vecino.y ] == 4:
                    nuevo_g = nodo_actual.g + 2 #Costo por tierra
                if grid[ vecino.x ][ vecino.y ] == 6:
                    nuevo_g = nodo_actual.g + 3 # Costo por lodo
                if grid[ vecino.x ][ vecino.y ] == 5:
                    nuevo_g = nodo_actual.g + 1  # Costo de movimiento uniforme
                nuevo_g = nodo_actual.g + 1
                vecino.g = nuevo_g
                vecino.h = min( distancia_manhattan( vecino, meta ) for meta in metas )
                vecino.f = vecino.g + vecino.h
                vecino.padre = nodo_actual
                cola_abierta.append( vecino )

        # Determina el nodo de menor costo que tiene como vecino para agregarlo a la ruta optima
        for vecino in cola_abierta:
            if( nodo_menor_costo is None ):
                nodo_menor_costo = vecino
            if ( vecino.f < nodo_menor_costo.f ):
                nodo_menor_costo = vecino
        if( nodo_menor_costo is None):
            nodo_menor_costo = cola_cerrada.__getitem__( len( cola_cerrada ) - 1 ).padre
        
        # Agrega el nodo a la cola cerrada y reinicia las variables 
        cola_cerrada.append( nodo_menor_costo )
        cola_abierta.clear()
        nodo_menor_costo = None

    return None

# funcion para devolver el camino como un arreglo de tuplas
def devolver_camino( camino ):
    camino_final= []
    for nodo in camino:
        camino_final.append( ( nodo.x, nodo.y ) )
    return camino_final

