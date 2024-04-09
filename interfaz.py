import pygame


from assets import img_medidor ,img_vidas

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 850
CELL_SIZE = 80
VIDAS_MAX = 3
BATERIA_MAX = 60
 
# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ------------------------------ Interfaz -----------------------------------------------
class Interfaz:
    def __init__(self):
        self.font = pygame.font.Font ( None, 36 )
        


    def dibujar_interface( self , pantalla , bateria, num_vidas ):

        self.dibujar_vidas( pantalla ,num_vidas )
        self.dibujar_bateria( pantalla ,bateria )
      


    def dibujar_vidas( self, screen , num_vidas ):
        for i in range( VIDAS_MAX ):
            if i < num_vidas:
                screen.blit( img_vidas[ 0 ], ( i * 45 + 10, 800 ) )
            else:
                screen.blit( img_vidas[ 1 ], ( i * 45 + 10, 800 ) )

    def dibujar_bateria( self, screen , costo ):
        
        num =  int ( ( costo * 15 ) / BATERIA_MAX )
        screen.blit( img_medidor[ num ], ( VIDAS_MAX * 45 + 20, 800 ) )
        
        self.dibujar_texto( screen , 'Pasos : ' + str( costo ) + ' / ' + str( BATERIA_MAX ) , VIDAS_MAX * 45 + 20 + 160 + 20 , 815  )
        

    def dibujar_texto ( self, screen , texto , posx , posy ):
        # Obtener el tamaño del texto renderizado
        pasos_txt = self.font.render( texto, True, BLACK )
        texto_rect = pasos_txt.get_rect()

        # Calcular las coordenadas de la esquina superior izquierda del rectángulo que rodea al texto
        rect_x = posx - 5  # Puedes ajustar este valor según tu preferencia
        rect_y = posy - 5  # Puedes ajustar este valor según tu preferencia

        # Llenar un rectángulo alrededor del texto con el color de fondo de la ventana
        pygame.draw.rect( screen, ( 255, 255, 255 ), ( rect_x, rect_y, texto_rect.width + 10, texto_rect.height + 10 ) )

        # Dibujar el texto
        screen.blit( pasos_txt, ( posx, posy ) )



# ------------------------------- BOTON -----------------------------------------------------

class Button:
    def __init__( self, screen, x = 0, y = 0, text = "", width = 200, height = 50, elev = 6 ):
        self.font = pygame.font.Font( None, 24 )
        self.text = self.font.render( text, True, "#ffffff" )
        self.text_rect = self.text.get_rect()

        self.bottom_rect = pygame.Rect( ( x + elev,  y + elev ), ( width, height ) )
        self.top_rect = pygame.Rect( ( x, y ), ( width, height ) )
        self.text_rect.center = self.top_rect.center

        self.hover = False
        self.pressed = False
        self.display  = screen

    def update( self ):
        
        mouse_pos = pygame.mouse.get_pos()
        if ( self.pressed ):
             self.pressed = True

        # comprobaremos si estamos encima
        elif self.top_rect.collidepoint( mouse_pos ):
            self.hover = True
            # Si presionamos mientras estamoas sobre el botón
            if pygame.mouse.get_pressed()[ 0 ]:
                self.pressed = True
           
                  
        else:
            self.pressed = False
            self.hover = False
        self.draw()

    def draw( self ):
        top_rect_color = "#141E27" if self.hover else "#F8B400"
        if not self.pressed:
            # Si no pulsamos dibujamos todo en su posición original
            pygame.draw.rect( self.display, "#666666", self.bottom_rect )
            pygame.draw.rect( self.display, top_rect_color, self.top_rect )
            self.text_rect.center = self.top_rect.center
        else:
            # Si pulsamos cambiamos la posición de dibujado abajo
            pygame.draw.rect( self.display, "#666666", self.bottom_rect )
            self.text_rect.center = self.bottom_rect.center
        
        self.display.blit( self.text, self.text_rect )
