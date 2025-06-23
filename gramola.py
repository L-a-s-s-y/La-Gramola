import pyglet

class Gramola:

    #Inicializador de la clase.
    def __init__(self):
        self.gramola = pyglet.media.Player() #Carga el reproductor
        self.vol = 0.5 #Voluen inicial
        self.__TIEMPO_SALTO = 5 #Tiempo de avance

    #Elimina la canción anterior de memoria y carga una nueva. 
    def play(self, track):
        self.limplia_el_reproductor ()
        self.gramola = pyglet.media.Player()
        try:
            self.fuente = pyglet.media.load(track)
        except:
            return False
        
        self.gramola.queue(self.fuente)
        self.gramola.play()
        self.gramola.volume = self.vol
        return True
    
    #Elimina la canción que hubiese en memoria en ese momento.
    def limplia_el_reproductor(self):
        #self.gramola.seek(0)
        self.gramola.pause()
        self.gramola.delete()

    #Igual que la anterior, se usa para un caso expecífico
    def parar(self):
        self.gramola.seek(0)
        self.gramola.pause()
        self.gramola.delete()
    
    #Modifica el volumen del reproductor.
    def volumen(self, volumen):
        self.gramola.volume = volumen/10
        self.vol= volumen/10
    
    #Pausa el reproductor
    def pausa(self):
        self.gramola.pause()
    
    #Reanuda el reproductor
    def reanudar(self):
        self.gramola.play()
    
    #Silencia el reproductor.
    def silenciar(self):
        self.gramola.volume = 0.0
    
    #Vuelve a dar volumen al reproductor
    def quitar_silenciar(self, volumen):
        self.gramola.volume = volumen
    
    
    #Detiene el reproductor
    def stop(self):
        self.limplia_el_reproductor()    
       
    #Avanza 5 segundos la reproducción
    def avanzar(self):
        tiempo = self.gramola.time + self.__TIEMPO_SALTO
        try:
            if self.fuente.duration > tiempo:
                self.gramola.seek(tiempo)
            else:
                self.gramola.seek(self.fuente.duration)
        except AttributeError:
            pass
    
    #Retrocede 5 segundos la reproducción
    def retroceder(self):
        tiempo = self.gramola.time - self.__TIEMPO_SALTO
        if tiempo > 0:
            self.gramola.seek(tiempo)
        else:
            self.gramola.seek(0)
    
    #Calcula cuánto tiempo se ha reproducido de la canción el cada momento
    def tiempo_reproducido(self):
        minutos = int(self.gramola.time / 60)
        segundos = int(self.gramola.time % 60)
        duracion = "{0:02d}:{1:02d}".format(minutos, segundos)
        return duracion
    
    #Calcula la duración total de la canción
    def duracion(self):
        minutos = int(self.fuente.duration / 60)
        segundos = int(self.fuente.duration % 60)
        duracion = "  de {0:02d}:{1:02d}".format(minutos, segundos)
        return duracion
    
    #Informa si se está reproduciendo una canción en el momento
    def se_esta_reproduciendo(self):        
        try:
            tiempo_reproducido = int(self.gramola.time)
            se_esta_reproduciendo  =  tiempo_reproducido < int(self.fuente.duration)
        except:
            se_esta_reproduciendo = False
        return se_esta_reproduciendo
        
    
            
        
    