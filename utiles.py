import sys
import pygame

# Módulo de útilidades para el programa en general.
# Aquí hay funciones que pueden ser importadas desde cualquier otro modulo

def cargar_imagenes(lista_nombres):
    
    # Carga las imagenes entregadas en lista_nombres
    # Devuelve un diccionario con cada imagen cargada
    
    imagenes = {}
    
    for nombre_archivo in lista_nombres:
        
        # |=  <-  union
        # .rsplit(".", 1)  <-  separa un string en el primer punto que encuentre, empezando por la derecha
        
        imagenes |= {nombre_archivo.rsplit(".", 1)[0]: pygame.image.load("imagenes/" + nombre_archivo)}
    
    return imagenes       



def cargar_sonido(nombres):
    
    # nombres -> string - lista
    # Carga los sonidos entregados en nombres
    # Devuelve una lista/objeto con cada sonido cargado
    
    if isinstance(nombres, list): # si se entrego una lista
        sonidos = []
        
        for nombre_archivo in nombres:
            sonidos.append(pygame.mixer.Sound("sonidos/" + nombre_archivo))
            
        return sonidos
    
    
    else: # si es un string
        return pygame.mixer.Sound("sonidos/" + nombres)



def coordenadas(posicion):
    
    #Devuelve la posición en coordenadas para la pantalla del juego (en px) 
    
    x, y = posicion
    
    return x*65, y*65



def centro_topleft(surf, x, y):
    
    # Recibe las coordenadas centrales de algún objeto Surface de pygame
    # Devuelve las coordenadas de la esquina superior-izquierda
    
    w, h = surf.get_size()
    
    return (x - w//2, y - h//2)



def aparecer(pantalla, clock, tiempo=1, sonido=None, delay=0):
    
    # realiza una transicion de pantalla: circulo expandiendose
    
    surf = pygame.Surface((1083, 650), flags=pygame.SRCALPHA) # mascara oscura
    imagen_congelada = pantalla.copy() # imagen inmediatamente anterior a la transicion
    
    radio = 0
    cambio = 632/(60*tiempo) # cambio necesario para que la transicion dure el tiempo dado
    espera = delay*60 # espera antes de comenzar la animacion
    
    # Efecto de sonido
    
    if (not sonido is None) and delay == 0:
        sonido.play()
    
    # Bucle que dura el tiempo dado
    
    for i in range(int((tiempo + delay)*60)):
        espera = max(espera - 1, 0) # descuento de la espera
        
        if (not sonido is None) and espera == 1:
            sonido.play()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Boton de salida presionado
                pygame.quit()
                sys.exit()
                
                
        # DIBUJO
        
        # Relleno de la mascara, fondo negro sin transparencia mas un círculo transparente
        
        surf.fill((0, 0, 0, 255))
        pygame.draw.circle(surf, (0,0,0,0), (1083//2, 650//2), int(radio))
        
        
        # dibujado de pantallas con la máscara encima
        
        pantalla.blit(imagen_congelada, (0, 0))
        pantalla.blit(surf, (0, 0))
        
        
        # Refrezco de pantalla
        
        pygame.display.flip()
        clock.tick(60)
        
        # si la espera es 0, comienza la animacion
        
        if espera == 0:
            radio = min(radio + cambio, 632) # actualizacion del radio


        
def desaparecer(pantalla, clock, tiempo=1, sonido=None, delay=0):
    
    # realiza una transicion de pantalla: circulo contrayendose
    
    surf = pygame.Surface((1083, 650), flags=pygame.SRCALPHA)
    imagen_congelada = pantalla.copy()
    
    radio = 632 # Radio mas pequeño fuera de pantalla
    cambio = 632/(60*tiempo) # cambio necesario para que la transicion dure el tiempo dado
    
    # Efecto de sonido
    
    if not sonido is None:
        sonido.play()
    
    # Bucle que dura el tiempo dado
    
    for i in range(int((tiempo+delay)*60)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Boton de salida presionado
                pygame.quit()
                sys.exit()
                
        # DIBUJO
        
        # Relleno de la mascara, fondo negro sin transparencia mas un círculo transparente
        
        surf.fill((0, 0, 0, 255))
        pygame.draw.circle(surf, (0,0,0,0), (541, 325), int(radio))
        
        
        # dibujado de pantallas con la máscara encima
        
        pantalla.blit(imagen_congelada, (0, 0))
        pantalla.blit(surf, (0, 0))
        
        
        # Refrezco de pantalla
        
        pygame.display.flip()
        clock.tick(60)
        
        radio = max(radio - cambio, 0) # actualizacion del radio
    
        
        