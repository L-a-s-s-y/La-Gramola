import os
import json
import eyed3

class Tracks:

    #Inicializador de tracks
    def __init__(self):
        self.playlist = []
        self.nombre_playlist=""
        carpeta_listas = os.path.abspath(os.path.join(os.path.dirname(__file__), 'listas'))
        self.archivo_favoritos=os.path.join(carpeta_listas, "favoritos")
        try:
            with open(self.archivo_favoritos, 'r') as fichero:
                self.playlist_favoritos = json.load(fichero)
        except:
            self.playlist_favoritos=[]
        
    #Carga el archivo de audio
    def add_track(self, archivo_audio):
        cancion = {
            "fichero":None, 
            "titulo":None, 
            "grupo":"", 
            "album":"", 
            "duracion":0, 
            "genero":"", 
            "tipo_fichero":None, 
            "favorito": False,
            "valoracion":0, 
            "portada":None
        }
        archivo_audio_path, archivo_audio_nombre = os.path.split(archivo_audio)
        auxiliar = archivo_audio_nombre.split('.')
        cancion["tipo_fichero"] = auxiliar[-1]
        if auxiliar[-1]=="mp3":
            datos = eyed3.load(archivo_audio)
            cancion["titulo"] = datos.tag.title
            cancion["grupo"] = datos.tag.artist
            cancion["album"] = datos.tag.album
            aux = str(datos.tag.genre).split(')')
            cancion["genero"] = aux[-1]                    
        else:
            cancion["titulo"] = " ".join(auxiliar[0:(len(auxiliar)-1)]) 
               
        cancion["fichero"] = archivo_audio
        lista_archivos = os.listdir(archivo_audio_path)  
        for archivos in lista_archivos:
            if archivos.endswith(".jpg"):
                cancion['portada']=archivos
                break
        
        for favorita in self.playlist_favoritos:
            if cancion["fichero"] == favorita["fichero"]:
                cancion["favorito"]=True               
                break
            else:
                cancion["favorito"]=False
        self.playlist.append(cancion)
        
    #Actualiza la info de una canción
    def actualizar_track(self, indice, titulo, grupo, album, genero):
        self.playlist[indice]["titulo"]=titulo
        self.playlist[indice]["grupo"]= grupo
        self.playlist[indice]["album"]=album
        self.playlist[indice]["genero"]= genero
        if self.nombre_playlist:
            self.grabar_lista(self.nombre_playlist)
        
    #Retoruna la canción indicada
    def cancion(self, indice):
        return self.playlist[indice]["fichero"]
    
    #Retorna la duración como String
    def duracion(self, indice):
        minutos = int(self.playlist[indice]["duracion"] / 60)
        segundos = int(self.playlist[indice]["duracion"] % 60)
        duracion = "  de {0:02d}:{1:02d}".format(minutos, segundos)
        return duracion
    
    #Retorna el título y la valoración como un String.
    def titulo(self, indice):
        estrella = "\u2606"
        estrellas = estrella*(self.playlist[indice]["valoracion"])
        titulo = self.playlist[indice]["titulo"]+"    "+estrellas
        return titulo
    
    #Retorna el álbum de la canción indicada.
    def album(self, indice):
        return self.playlist[indice]["album"]
    
    #Retorna el grupo de la canción indicada.
    def grupo(self, indice):
        return self.playlist[indice]["grupo"]
    
    #Retorna el género de la canción indicada
    def genero(self, indice):
        return self.playlist[indice]["genero"]
    
    #Marca una canción como favorito.
    def favorito(self, indice):
        if self.es_favorito(indice):
            return
        self.playlist[indice]["favorito"]=True
        self.almacena_en_favoritos(self.playlist[indice])
        if self.nombre_playlist:
            self.grabar_lista(self.nombre_playlist)
    
    #Quita el favorito de una canción
    def quitar_favorito(self, indice):
        if not self.es_favorito(indice):
            return          
        self.elimina_en_favolitos(self.playlist[indice])
        self.playlist[indice]["favorito"]=False
        
    #Retorna si una canción es favorita
    def es_favorito(self, indice):
        return self.playlist[indice]["favorito"]
    
    #Asigna una valoración a la cación indicada
    def valoracion(self, indice, valoracion):
        self.playlist[indice]["valoracion"]=valoracion
    
    #Guarda una canción en la playlist favoritos
    def almacena_en_favoritos(self, cancion):                
        self.playlist_favoritos.append(cancion)
        with open(self.archivo_favoritos, 'w') as fichero:
            json.dump(self.playlist_favoritos, fichero)
             
    #Elimina una canción de la lista de favoritos
    def elimina_en_favolitos(self, cancion):        
        self.playlist_favoritos.remove(cancion)
        with open(self.archivo_favoritos, 'w') as fichero:
            json.dump(self.playlist_favoritos, fichero)
      
    #Limpia la lista de reproducción actual.
    def borrar_playlist(self):
        self.playlist.clear()
        self.nombre_playlist=""
    
    #Determina si una lista de reproducción está guardada
    def esta_guardada(self):
        if self.lista_guardada==None:
            return False
        else:
            return True
    
    #Guarda la lista de reproducción actual.
    def grabar_lista(self, archivo_actual):     
        with open(archivo_actual, 'w') as fichero:
            json.dump(self.playlist, fichero)
           
        self.nombre_playlist =archivo_actual
       
    #Carga una lista de reproducción
    def cargar_lista(self, archivo_actual):
        with open(archivo_actual, 'r') as fichero:
            self.playlist = json.load(fichero)
        self.nombre_playlist =archivo_actual
        ficheros =[x["fichero"] for x in self.playlist_favoritos]
       
        for cancion in self.playlist:
            if cancion["fichero"] in ficheros:
                cancion["favorito"] = True
            else:
                cancion["favorito"]= False
        
        with open(archivo_actual, 'w') as fichero:
            json.dump(self.playlist, fichero)
        
    #Pasa a la siguiente canción de la lista de reproducción actual.
    def siguiente_track(self, indice):
        return self.playlist[indice]
    
    #Elimina el track indicado de la lista de reproducción actual.
    def eliminar_track(self, indice):
        del self.playlist[indice]
        if self.nombre_lista()=="favoritos":            
            self.grabar_lista(self.nombre_playlist)
            with open(self.archivo_favoritos, 'r') as fichero:
                self.playlist_favoritos = json.load(fichero)
    
    #Retorna el nombre de la lista de reproducción.
    def nombre_lista(self):
        auxiliar, nombre_playlist = os.path.split(self.nombre_playlist)
        return nombre_playlist
        
    
   