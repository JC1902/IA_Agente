import pygame

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 850
CELL_SIZE = 80
VIDAS_MAX = 3
BATERIA_MAX = 15 

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Interfaz:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.button_text = self.font.render("Iniciar!", True, BLACK)
        self.btn_Inciar = self.button_text.get_rect(center=(WIDTH/2, HEIGHT/2))

        self.img_vidas = [pygame.image.load(f'interfaz/vida_{i}.png') for i in range(2)]

        self.img_medidor = [
            pygame.transform.rotate(
                pygame.transform.scale(
                    pygame.image.load(f'interfaz/medidor/bateria_{i}.png'),
                    (int(CELL_SIZE / 3 * 2), CELL_SIZE * 2)
                ),
                90  
            )
            for i in range(16)
        ]

    def dibujar_interface(self , pantalla , bateria, num_vidas, btn_Ini_Visible):

        self.dibujar_vidas(pantalla ,num_vidas)
        self.dibujar_bateria(pantalla ,bateria)

        if btn_Ini_Visible:
            pantalla.blit(self.button_text, self.btn_Inciar)


    def dibujar_vidas(self, screen , num_vidas):
        for i in range(VIDAS_MAX):
            if i < num_vidas:
                screen.blit( self.img_vidas[0], (i * 30 + 10, 815))
            else:
                screen.blit( self.img_vidas[1], (i * 30 + 10, 815))

    def dibujar_bateria( self, screen , bateria):
        screen.blit( self.img_medidor[BATERIA_MAX - bateria], (VIDAS_MAX * 30 + 20, 800))


