import sys
import pygame

import utiles


##############################################################################

pygame.mixer.init() # debe ser inicializado en cada modulo (?)

# Imagenes de fondo 


nombres_imagenes = ["menu_principal.jpg",
                    "fondo_historia.jpg",
                    "fondo_instrucciones.jpg",
                    "escena_victoria.jpg",
                    "escena_derrota.jpg",
                    "fondo_general.jpg",
                    ]

imagenes_pantallas = utiles.cargar_imagenes(nombres_imagenes)



# Sonidos

sonido_transicion_aparecer = utiles.cargar_sonido("transicion_aparecer.ogg")
sonido_transicion_desaparecer = utiles.cargar_sonido("transicion_desaparecer.ogg")
musica_victoria = utiles.cargar_sonido("victoria.ogg")
musica_menu_principal = utiles.cargar_sonido("menu_principal.ogg")
musica_derrota = utiles.cargar_sonido("derrota.ogg")
musica_instrucciones = utiles.cargar_sonido("instrucciones.ogg")





# MENU PRINCIPAL

def menu_principal(pantalla, clock):
    
    # inicio musica menu principal.
    # termina al cierre de la pantalla de historia
    
    musica_menu_principal.play(-1)
    
    k = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                tecla_presionada = pygame.key.name(event.key)
                
                if tecla_presionada == "return":     #Para pasar del menu principal a la historia
                    utiles.desaparecer(pantalla, clock, tiempo=1, sonido=sonido_transicion_desaparecer)
                    return "historia"

        #DIBUJO 
        pantalla.blit(imagenes_pantallas["menu_principal"], (0, 0))
        
        k += 1
        if k == 1:
            utiles.aparecer(pantalla, clock, 1)
            
        #ACTUALIZACION DE PANTALLA
        pygame.display.flip()
        clock.tick(60)
        
        
        
        
        
##############################################################################

# HISTORIA

def historia(pantalla, clock):
    k = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            elif event.type == pygame.KEYDOWN:
                tecla_presionada = pygame.key.name(event.key)
                if tecla_presionada == "return":
                    # Termino musica menu principal e historia
                    
                    pygame.mixer.stop()
                    
                    utiles.desaparecer(pantalla, clock, tiempo=1, sonido=sonido_transicion_desaparecer)
                    return "instrucciones"
                
        pantalla.blit(imagenes_pantallas["fondo_historia"], (0,0))
        
        k+=1
        if k == 1:
            utiles.aparecer(pantalla, clock, tiempo=1, sonido=sonido_transicion_aparecer)
            
        pygame.display.flip()
        clock.tick(60)
        
        
        
        

##############################################################################

# INSTRUCCIONES

def instrucciones(pantalla, clock):
    fuente = pygame.font.SysFont("Papyrus", 78, bold=True)
    i = 0
    while True: 
        i += 1
        texto_segundos = fuente.render(f"- {20-i//60}", True, "black")
        if i == 20*60:   #segundos para leer las instrucciones 20 seg
            utiles.desaparecer(pantalla, clock, 1)
            return "tablero"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                utiles.desaparecer(pantalla, clock, 1, sonido_transicion_desaparecer)
                return "tablero"  #para apretar cualquier letra y pasar a la siguiente pantalla
     
        # DIBUJO 
        pantalla.blit(imagenes_pantallas["fondo_instrucciones"], (0, 0))
        pantalla.blit(texto_segundos, (620, 35))
        
        if i == 1:
            utiles.aparecer(pantalla, clock, tiempo=1, delay=1.5, sonido=sonido_transicion_aparecer)
            
            # inicio musica instrucciones
            # termina al cambiar de pantalla
            
            musica_instrucciones.play()
            
        # ACTUALIZACION DE PANTALLA
        pygame.display.flip()
        clock.tick(60)





##############################################################################

# RESULTADOS

def victoria(pantalla, clock, puntuacion=100000):
    fuente = pygame.font.SysFont("Papyrus", 42, bold=True)
    texto_puntuacion = fuente.render("Puntuación:" + str(puntuacion), True, (0, 0, 0))
    
    # Inicio musica victoria
    # Se termina sola o cuando se interrumpe al salir de la pantalla de puntajes
    
    musica_victoria.play() 
    
    k = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                tecla_presionada = pygame.key.name(event.key)
                
                if tecla_presionada == "r":    #Para volver al tablero
                    utiles.desaparecer(pantalla, clock, 1, sonido_transicion_desaparecer)
                    return "tablero"
                
                elif tecla_presionada == "m":   #Para volver al menu principal
                    utiles.desaparecer(pantalla, clock, 1, sonido_transicion_desaparecer)
                    return "menu_principal"
                
        # DIBUJO 
        pantalla.blit(imagenes_pantallas["escena_victoria"], (0, 0))
        pantalla.blit(texto_puntuacion, (530, 100))
        
        k += 1
        if k == 1:
            utiles.aparecer(pantalla, clock, 1)
            
            
        # ACTUALIZACION DE PANTALLA
        
        pygame.display.flip()
        clock.tick(60)
        
        
def derrota(pantalla, clock):
    #Musica de derrota
    #Se termina sola o cuando se cambia de pantalla
    
    musica_derrota.play(-1)
    
    k = 0
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                tecla_presionada = pygame.key.name(event.key)
                
                if tecla_presionada == "r":    #Para volver al tablero
                    utiles.desaparecer(pantalla, clock, 1, sonido_transicion_desaparecer)
                    return "tablero"
                
                elif tecla_presionada == "m":    #Para volver al menu principal
                    utiles.desaparecer(pantalla, clock, 1, sonido_transicion_desaparecer)
                    return "menu_principal"
                
        # DIBUJO 
        pantalla.blit(imagenes_pantallas["escena_derrota"], (0, 0))
        
        k += 1
        if k == 1:
            utiles.aparecer(pantalla, clock, 2)
            
        # ACTUALIZACION DE PANTALLA
        
        pygame.display.flip()
        clock.tick(60)





##############################################################################

# PUNTAJES

def mejores_puntajes(pantalla, clock, puntuacion=10000, lista=[300000,200000,100000]):
    fuente = pygame.font.SysFont("Papyrus", 60, bold=True)
    fuente2= pygame.font.SysFont("Papyrus", 42, bold=True)
    #Fuente de los textos de la pantalla
    
    texto_puntuacion = fuente.render("Puntuación:" + str(puntuacion), True, (0, 0, 0))
    texto_puntuacion2= fuente2.render("Mejores puntuaciones:", True, (0, 0, 0))
    texto_puntuacion3= fuente2.render(str(lista[0]), True, (0, 0, 0))
    texto_puntuacion4= fuente2.render(str(lista[1]), True, (0, 0, 0))
    texto_puntuacion5= fuente2.render(str(lista[2]), True, (0, 0, 0))
    #Variables con los textos que se van a imprimir

    i = 0
    while True:
        i += 1
        if i == 10*60:   #Tiempo para que cambie de pantalla automaticamente
            utiles.desaparecer(pantalla, clock, 1)
            return      
        
        texto_segundos = fuente.render(f"- {10-i//60} -", True, "white")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:  
                utiles.desaparecer(pantalla, clock, 1, sonido_transicion_desaparecer)
                return

                
        # DIBUJO 
        pantalla.blit(imagenes_pantallas["fondo_general"], (0, 0))  
        pantalla.blit(texto_puntuacion, utiles.centro_topleft(texto_puntuacion, 541, 100))
        pantalla.blit(texto_puntuacion2, utiles.centro_topleft(texto_puntuacion2, 541, 180))
        pantalla.blit(texto_puntuacion3, utiles.centro_topleft(texto_puntuacion3, 541, 260))
        pantalla.blit(texto_puntuacion4, utiles.centro_topleft(texto_puntuacion4, 541, 320))
        pantalla.blit(texto_puntuacion5, utiles.centro_topleft(texto_puntuacion5, 541, 380))
        pantalla.blit(texto_segundos, utiles.centro_topleft(texto_segundos, 541, 500))
    
        if i == 1:       #Validar el timepo para que cambie automaticamente cuando se acabe
            utiles.aparecer(pantalla, clock, 1, sonido_transicion_aparecer)
        clock.tick(60)
        
        # ACTUALIZACION DE PANTALLA
        pygame.display.flip()
        




#############################################################################

# MENU PAUSA

def pausa(pantalla, clock):
    fuente_grande = pygame.font.SysFont("Papyrus", 120)
    fuente = pygame.font.SysFont("Papyrus", 56)
    #Fuente de los textos
    
    texto_pausa = fuente_grande.render("Pausa", True, "white")
    texto_reanudar = fuente.render("[P] - Reanudar", True, "white")
    texto_reiniciar = fuente.render("[R] - Reiniciar", True, "white")
    texto_menu_principal = fuente.render("[M] - Menú principal", True, "white")
    #Variables con los textos a imprimir 
    
    imagen_congelada = pygame.display.get_surface() # Consigue la ultima imagen actualizada
    
    # Genera pseudo-transparencia. 
    # la flag multiplica pixel por pixel px1*px2//256
    imagen_congelada.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_MULT) 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                tecla_presionada = pygame.key.name(event.key)
                
                if tecla_presionada == "p": #Tecla para quitar la pausa
                    return "reanuda"
                
                elif tecla_presionada == "r":   #Tecla para reiniciar la partida
                    return "reinicia"
                
                elif tecla_presionada == "m":
                    return "menu_principal"
                
        # DIBUJO 
        pantalla.blit(imagen_congelada, (0, 0))   
        pantalla.blit(texto_pausa, (370, 50))
        pantalla.blit(texto_reanudar, utiles.centro_topleft(texto_reanudar, 541, 340))
        pantalla.blit(texto_reiniciar, utiles.centro_topleft(texto_reiniciar, 541, 450))
        pantalla.blit(texto_menu_principal, utiles.centro_topleft(texto_menu_principal, 541, 560))
        
        # ACTUALIZACION DE PANTALLA
        pygame.display.flip()
        clock.tick(60)




##############################################################################
