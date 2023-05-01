import sys
import pygame
import random

import utiles
from pantallas import pausa


##############################################################################

pygame.mixer.init()

##############################################################################

# Dialogos 
# Lista con dialogos y su tiempo de duración

dialogos_orig = [("Hola!", 3),
                 ("Soy Qbertito!", 5),
                 ("Ayudame a limpiar", 5),
                 ("Quiero terminar ya!", 5),
                 ("Para volver a casa", 5),
                 ("Y ver a mi perro\nSteroid", 6),
                 ("", 2),
                 ("¿Puedo contarte de\nél?", 6),
                 ("Lo tengo desde\npequeño", 6),
                 ("Lo encontre matando\nun zombie...", 7),
                 ("... a puño limpio.", 8),
                 ("¡Es muy fuerte!", 6),
                 ("Incluso lo pillé\npeleando...", 7),
                 ("con 1.000.000 de\nzombies", 7),
                 ("Le costó dos días\nacabar", 7),
                 ("Todavía está\ncansado.", 7),
                 ("Ahora está cuidando\nla casa.", 7),
                 ("Tengo que verlo\npronto!!!", 10e10),
                 ]

# Carga de imágenes 
nombres_imagenes = ["fondo_tablero.jpg",
                    "qbertito.png",
                    "zombie.png",
                    "piso_normal.jpeg",
                    "piso_sucio.png",
                    "covid.png",
                    "botella.png",
                    ]

imagenes_tablero = utiles.cargar_imagenes(nombres_imagenes)



# Carga de sonidos

nombres_sonidos_zombie = ["zombie1.ogg",
                          "zombie2.ogg",
                          "zombie3.ogg",
                          "zombie4.ogg",
                          ]

sonidos_zombie = utiles.cargar_sonido(nombres_sonidos_zombie)
sonido_transicion_aparecer = utiles.cargar_sonido("transicion_aparecer.ogg")
sonido_muerte = utiles.cargar_sonido("sonido_muerte.ogg")
musica_tablero = utiles.cargar_sonido("tablero.ogg")
musica_pausa = utiles.cargar_sonido("pausa.ogg")



# Funciones generales

def dialogo_qbertito(texto, fuente):
    
    # Convierte los dialogos de string a Surface, centrando el texto
    # Centra los textos de 1 linea
    # Combina y centra los textos de 2 lineas
    # Pygame no soporta el \n
    
    textos = texto.split("\n") # Separa el texto cada vez que encuentra un salto de linea
    surf = pygame.Surface((250, 80), flags=pygame.SRCALPHA)
    
    alturas = [[40], [21, 59]] # alturas de textos de 1 y 2 lineas, respectivamente
    a = len(textos)-1 # indice para alturas
    
    for n, t in enumerate(textos):
        tex = fuente.render(t, True, (0, 0, 0, 255))
        h = alturas[a][n]
        surf.blit(tex, utiles.centro_topleft(tex, 125, h)) # coloca correctamente los textos
        
    
    return surf
    

def generar_tablero():
    
    # Genera un tablero de 10x10
    
    estado_tablero   = [] # Lista de listas que contienen el estado de cada cuadrado del tablero
    for i in range(10):
        filas = []
        
        for j in range(10):
            filas.append(False) #False: cuadrado desactivado; True: cuadrado activado
            
        estado_tablero.append(filas)
        
    estado_tablero[0][0] = True # Posición inicial marcada
    
    return estado_tablero



def marcar_cuadrado(estado_tablero, posicion):
    
    # Activa o desactiva el cuadrado donde el jugador pasa
    
    x, y = posicion
    estado_tablero[x][y] = not estado_tablero[x][y] # Inversión de booleanos
    
    return estado_tablero



def generar_obstaculos(estado_tablero):
    
    # Genera 3 obstaculos de 1, 2 y 3 cuadrados; devuelve una lista que contiene la posicion en 
    # el tablero de cada cuadrado
    
    obstaculos = [] #lista con la posicion de los obstaculos
    
    for i in range(3): 
        # CUADRADO CENTRAL
        obstaculo_c = [random.randint(2, 8), random.randint(2, 8)] # Posicion aleatoria
        
        while obstaculo_c in obstaculos: # Validación que ningún cuadrado aparezca encima de otro
            obstaculo_c = [random.randint(2, 8), random.randint(2, 8)]
            
        obstaculos.append(obstaculo_c)
        
        # CUADRADOS PERIFERICOS (solo para largos 2 y 3)
        for j in range(i):
            obstaculo_p = obstaculo_c[:] # copiamos solo el contenido de la lista
            obstaculo_p[random.randint(0, 1)] += random.choice([-1, 1]) # el cuadrado aparece en una posicion aleatoria adyacente al cuadrado central (prob. 0.25 cada posición)
            
            while obstaculo_p in obstaculos: # Validación que el cuadrado no aparezca sobre otro
                obstaculo_p = obstaculo_c[:]
                obstaculo_p[random.randint(0, 1)] += random.choice([-1, 1])
                
            obstaculos.append(obstaculo_p)
    
    # Por defecto la posicion de los obstáculos debe estar activada
    for posx, posy in obstaculos:
        estado_tablero[posx][posy] = True
        
    return obstaculos, estado_tablero



def verifica_posicion(posicion, obstaculos):
    
    # Verifica que el jugador no está en un obstáculo
    
    if posicion in obstaculos:
        return False
    
    return True





# Generación & dinámica de enemigos

def generar_enemigos(obstaculos, numero_enemigos=2):
    
    # genera enemigos (2 por defecto) con posicion aleatoria en el tablero
    
    posiciones_prohibidas = obstaculos + [[0, 0], [1, 0], [0, 1], [1, 1]] # posiciones protegidas
    enemigos = []
    
    for i in range(numero_enemigos):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        
        while [x, y] in posiciones_prohibidas: # validacion: el enemigo no esta en un obstaculo o en una posicion protegida
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            
        posiciones_prohibidas.append([x, y]) # protegemos la posicion del enemigo, así no se sobreponen
        enemigos.append([x, y])
    
    return enemigos



def mover_enemigos(enemigos, obstaculos):
    
    # Mueve a los enemigos en el tablero.
    # Para evitar bucles infinitos con enemigos atrapados, itera solo en los 4 movimientos posibles (aleatoriamente)
    # Así, un enemigo bloqueado queda en su misma ubicacion.
    
    posiciones_prohibidas = obstaculos + [[0, 0], [1, 0], [0, 1], [1, 1]]
    #posiciones_prohibidas.append([0, 0]) # posiciones especificas donde no pueden moverse los enemigos
    posibles_movimientos = [(0, -1), (0, 1), (1, -1), (1, 1)] # ( indice: vertical-horizontal , sentido de la direccion)
    
    for i, enemigo in enumerate(enemigos): # iteramos por cada enemigo y su respectiva posicion (i) en la lista
        posicion_anterior = enemigo[:] 
        
        random.shuffle(posibles_movimientos) # barajamos la lista, con tal de mantener un movimiento aleatorio
        
        for indice, movimiento in posibles_movimientos:
            enemigo[indice] += movimiento # realizacion del movimiento
            
            if enemigo[0] < 0 or enemigo[1] < 0 or enemigo[0] > 9 or enemigo[1] > 9: # esta dentro del tablero
                enemigo[:] = posicion_anterior[:]
            
            elif enemigo in posiciones_prohibidas: # no esta en un obstaculo o en la posicion protegida
                enemigo[:] = posicion_anterior[:]
                
            elif enemigo in enemigos[:i]: # no se sobrepone con un enemigo que ya se movio
                enemigo[:] = posicion_anterior[:]
                
            elif enemigo in enemigos[i+1:]: # no se sobrepone con algun otro enemigo, que tal vez este bloqueado
                enemigo[:] = posicion_anterior[:]
                
            else: # posicion disponible, deja de buscar
                break
        
    return enemigos
            

    


# Función principal

def main(pantalla, clock):
    
    # Implementa las mecánicas del juego con todas sus reglas.
    #  - Cada vez que qbertito se mueve, el puntaje disminuye en 100
    #  - Cada vez que un zombie toca a qbertito, pierde una vida y el puntaje disminuye en 1000
    #  - El puntaje minimo es 100
    # Devuelve la próxima pantalla a mostrar
    
    
    # Inicializacion de la Surface dinamica de qbertito
    
    qbertito = imagenes_tablero["qbertito"].copy()
    ultima_transicion = ""
    proximo_sonido_zombie = random.randint(1, 5)*60
    proximo_dialogo = 0
    dialogos = iter(dialogos_orig) # genera un iterador, para ir secuencialmente
    
    # Inicializacion y creación de fuentes
    
    fuente = pygame.font.SysFont("Papyrus", 42, bold=True)
    fuente2 = pygame.font.SysFont("Papyrus", 24, bold=True)
    
    texto_puntuacion = fuente.render("Puntuación", True, "black")
    texto_pausa = fuente.render("[P] - Pausa", True, "black")
    
    
    # Inicialización de tablero y posiciones de cada objeto
    
    posicion_jugador = [0, 0] # Posicion inicial jugador
    estado_tablero = generar_tablero()
    obstaculos, estado_tablero = generar_obstaculos(estado_tablero) # Inicializacion de la lista de obstaculos
    enemigos = generar_enemigos(obstaculos)
    
    #ultimas_transiciones_zombies = ["" for _ in range(len(enemigos))]
    
    
    # Inicialización de vida y puntaje
    vidas = 3 
    puntaje = 100000 
    
    
    # musica
    
    musica_tablero.play(-1)
    
    
    # Bucle por cada cuadro (60 fps)
    k = 0 # contador
    while True: 
        
        # Eventos de pygame & dinámicas del juego
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Boton de salida presionado
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN: # Boton de movimiento presionado
                tecla_presionada = pygame.key.name(event.key)
                posicion_anterior = posicion_jugador[:]
                
                # Botones de movimiento
                
                if tecla_presionada == "w" and posicion_jugador[1]>0: # ARRIBA
                    posicion_jugador[1] -= 1
                    
                if tecla_presionada == "s" and posicion_jugador[1]<9: # ABAJO
                    posicion_jugador[1] += 1
                    
                    
                if tecla_presionada == "a" and posicion_jugador[0]>0: # IZQUIERDA
                    posicion_jugador[0] -= 1
                    
                    if ultima_transicion != "a": # Cambio en la direccion de qbertito
                        qbertito = pygame.transform.flip(qbertito, True, False)
                        ultima_transicion = "a"
                        
                    
                if tecla_presionada == "d" and posicion_jugador[0]<9: # DERECHA
                    posicion_jugador[0] += 1
                    
                    if ultima_transicion != "d": # Cambio en la direccion de qbertito
                        qbertito = pygame.transform.flip(qbertito, True, False)
                        ultima_transicion = "d"
                    
                    
                # Boton de pausa
                
                if tecla_presionada == "p": 
                    
                    # Inicio de musica pausa
                    
                    pygame.mixer.pause()
                    
                    musica_pausa.play(-1)
                    
                    comando = pausa(pantalla, clock) # llama al menu pausa
                    
                    # Fin de musica pausa
                    
                    musica_pausa.stop()
                    
                    if comando == "reinicia": # verifica si se presiona [R]
                    
                        # Reasignamos las variables y listas de posiciones a su estado inicial
                        
                        dialogos = iter(dialogos_orig)
                        proximo_dialogo = 0
                        qbertito = imagenes_tablero["qbertito"].copy()
                        ultima_transicion = ""
                        proximo_sonido_zombie = random.randint(1, 5)*60
                        posicion_jugador = [0, 0]
                        estado_tablero = generar_tablero()
                        obstaculos, estado_tablero = generar_obstaculos(estado_tablero)
                        enemigos = generar_enemigos(obstaculos) 
                        
                        vidas = 3 
                        puntaje = 100000 
                        
                        pygame.mixer.stop() # cortamos cualquier sonido que se esté reproduciendo
                        
                        # reiniciamos la musica
                        
                        musica_tablero.play(-1)
                        
                        k = 0
                        
                        
                        # Cortamos el bucle para que no se cuente el movimiento
                        
                        break
                    
                    
                    elif comando == "menu_principal": # verifica si se presiona M
                        return "menu_principal", 0
                    
                    
                    pygame.mixer.unpause()
                    
                        
                        
                # Si el jugador realiza un movimiento válido
 
                if verifica_posicion(posicion_jugador, obstaculos) and posicion_jugador != posicion_anterior: 
                    
                    puntaje -= 100 # Disminucion por movimiento
                    
                    
                    # El jugador toca a un enemigo
                    
                    if posicion_jugador in enemigos:
                        puntaje -= 1000
                        vidas -= 1
                        posicion_jugador[:] = [0, 0]
                        
                        # Efecto de sonido
                        sonido_muerte.play()
                        
                        
                    # actualización de posiciones y tablero
                        
                    marcar_cuadrado(estado_tablero, posicion_jugador) # Activamos o desactivamos la posicion a la que se movio el jugador
                    enemigos = mover_enemigos(enemigos, obstaculos)
                    
                    
                    # Un enemigo toca al jugador
                    
                    if posicion_jugador in enemigos:
                        puntaje -= 1000
                        vidas -= 1
                        posicion_jugador[:] = [0, 0]
                        marcar_cuadrado(estado_tablero, posicion_jugador)
                        
                        # Efecto de sonido
                        sonido_muerte.play()
                    
                    
                    # Validacion de derrota
                    if vidas < 1:
                        return "derrota", 0
                   
                    
                    # Limitación de puntaje
                    
                    puntaje = max(puntaje, 100)
                    
                    
                # Movimiento invalido
                
                else:
                    # qbertito no se mueve
                    posicion_jugador[:] = posicion_anterior[:]

        
        # Validacion de victoria
        # Verifica que cada cuadro está activado
        
        victoria = True
        
        for fila in estado_tablero:
            for estado in fila:
                
                if not estado: # Un cuadrado está desactivado
                    victoria = False
                    
        if victoria:
            return "victoria", puntaje
        
        
        # Sonidos de zombies
        
        if k == proximo_sonido_zombie:
            pygame.mixer.Sound.play(random.choice(sonidos_zombie))
            proximo_sonido_zombie = k + random.randint(3, 10)*60
        
        
        # Imagen numero vidas y puntuacion
        
        imagen_puntuacion = fuente.render(str(puntaje), True, "black")
        
        # Creación de Surface base con flag de transparencia
        imagen_vidas = pygame.Surface((70*vidas, 70), flags=pygame.SRCALPHA)
        
        for i in range(vidas): # Relleno de Surface con imagenes segun el numero de vidas
            imagen_vidas.blit(imagenes_tablero["botella"], (70*i, 0))
            
        
        # Dialogos de Qbertito
        if k == proximo_dialogo:
            dialogo_actual, tiempo_espera_dialogo = next(dialogos)
            surf_dialogo_actual = dialogo_qbertito(dialogo_actual, fuente2)
            
            proximo_dialogo = k + tiempo_espera_dialogo*60
            
            
        
        # DIBUJO
        
        # Fondo del tablero
        
        #pantalla.fill("black")
        pantalla.blit(imagenes_tablero["fondo_tablero"], (0, 0))
        
        
        # Dibujado de cada estado del tablero
        
        for i in range(10): # Posicion x tablero
            for j in range(10): # Posicion y tablero
            
                # Cuadrado activado
                
                if estado_tablero[i][j]:
                    pantalla.blit(imagenes_tablero["piso_normal"], utiles.coordenadas([i, j]))
                
                
                # Cuadrado desactivado
                
                else: 
                    pantalla.blit(imagenes_tablero["piso_sucio"], utiles.coordenadas([i, j]))


        # Dibujado de obstáculos 
        
        for posicionObstaculo in obstaculos:
            pantalla.blit(imagenes_tablero["covid"], utiles.coordenadas(posicionObstaculo))
         
            
        # Dibujado del jugador
        pantalla.blit(qbertito, utiles.coordenadas(posicion_jugador))


        # Dibujado de los enemigos
        
        for posicion_enemigo in enemigos:
            pantalla.blit(imagenes_tablero["zombie"], utiles.coordenadas(posicion_enemigo))
        
        
        # Dibujado de textos y vidas
        
        
        pantalla.blit(imagen_vidas, utiles.centro_topleft(imagen_vidas, 870, 350))
        pantalla.blit(texto_puntuacion, utiles.centro_topleft(texto_puntuacion, 870, 440))
        pantalla.blit(imagen_puntuacion, utiles.centro_topleft(imagen_puntuacion, 870, 490))
        pantalla.blit(texto_pausa, (760, 540))
        
        pantalla.blit(surf_dialogo_actual, utiles.centro_topleft(surf_dialogo_actual, 880, 78))
        
        
        # Transicion: aparicion
        
        k += 1
        if k == 1:
            utiles.aparecer(pantalla, clock, tiempo=1, sonido=sonido_transicion_aparecer)
            
            
            
        # ACTUALIZACION PANTALLA
        
        pygame.display.flip()
        clock.tick(60) # limite 60 fps
        
        
        
        
##############################################################################
    
# TABLERO (PROGRAMA PRINCIPAL)

if __name__ == "__main__":
    posicion_jugador = [0, 0] # Posicion del jugador en el tablero
    pygame.init()
    pygame.mixer.init()
    pantalla = pygame.display.set_mode((650*5//3, 650))
    clock = pygame.time.Clock()
        
    try:
        main(pantalla, clock)
    finally:
        pygame.quit()
