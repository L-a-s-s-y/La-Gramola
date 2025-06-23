#Construye el entorno gráfico

#Modulos necesarios
import tkinter as tk #GUI básico.
import tkinter.filedialog #Utilidades de lectura y escritura de archivos, manejo del árbol de directorios.
import tkinter.messagebox #Ventanas de alerta.
import tkinter.ttk as ttk #Versión moderna de tkinter. Aporta mejoras estéticas y widgets especiales.
import os #Controles del SO.
import Pmw #Ventanas Emergentes

''' 
    Estructura:
        -> GUI: app_music_v3.py
        -> EEDD: tracks.py
        -> Modulo reproductor: gramola.py
'''

#Importa la estructura de datos y el reproductor. AVISO: deben estar en el mismo directorio.
import tracks
import gramola

#Guarda en una variable la ruta absoluta del directorio donde se encuentran las imágenes.
carpeta_imagenes = os.path.abspath(os.path.join(os.path.dirname(__file__), 'imagenes'))

class App_Music:
    #Window es la ventana principal sobre la que se construye todo.
    def __init__(self, window, tracks, gramola):
        self.window = window
        self.tracks = tracks
        self.gramola = gramola
        #Pausado estará a True si se ha pulsado el botón pausa, false en caso contrario (aún hay que afinarlo).
        self.pausado = False
        #Mute estará a true si el volumen está a 0, false en caso contrario
        self.mute=False
        self.window.title("La Gramola")
        try:
            self.window.iconbitmap(os.path.join(carpeta_imagenes, "ICONO.ico"))
        except:
            pass
        self.crea_widget()        
        
    #Crea cada uno de los componentes de la ventana.
    def crea_widget(self):
        self.bocadillo=Pmw.Balloon(self.window)
        self.crea_visor_merceses()
        self.crea_formulario()
        self.crea_lista()
        self.crea_botones()
        self.crea_menu()
        self.crea_menu_contextual()
    
    def crea_visor_merceses(self):
        #Se toma la ventana principal y se crea un marco donde se colocan las cosas.
        frame = ttk.LabelFrame(self.window, text="Visor LCD")
        fila = 2
        #Carga las imágenes en formato que puede ser utilizado por el TKinter    
        imagen_visor = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"fondo_frame.png"))
        self.corchea = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"corchea1.png"))
        self.imagen_album = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"album.png"))
        self.imagen_grupo = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"microfono.png"))
        self.imagen_tiempo = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"reloj.png"))

        #Crea un canvas, en el que se pueden poner texto, imagnenes, se puede dibujar, etc.
        #Frame es el widget padre donde se coloca (obligatorio).
        self.canvas = tk.Canvas(frame, width=400, height=200)
        self.canvas.image=imagen_visor  
        #Indica donde irá el canvas      
        self.canvas.grid(row=1, column=0, sticky="sw")
         #Coloca la imagen de fondo en el canvas
        self.console = self.canvas.create_image(0,10, anchor=tk.NW, image=imagen_visor)
        #Coloca el icono del tiempo en el canvas
        self.canvas.create_image(50, 75, image=self.imagen_tiempo)
        #Coloca el texto del tiempo del canvas
        self.tiempo = self.canvas.create_text(75, 75, anchor=tk.W, fill = "yellow", text="00:00", font=("Candara", 12))
        self.duracion_track = self.canvas.create_text(115, 75, anchor=tk.W, fill = "yellow", text=" de  00:00", font=("Candara", 12))
        #Coloca la imagen de la canción   
        self.canvas.create_image(50, 100, image=self.corchea)
        #Coloca el texto con el nombre de la canción
        self.nombre_track = self.canvas.create_text(75, 100, anchor=tk.W, fill = "yellow", text = "Nada reproduciéndose en este momento", font=("Candara", 12))
        #Coloca la imagen de album
        self.canvas.create_image(50, 125, image=self.imagen_album)
        #Coloca el texto con el nombre del grupo
        self.canvas_album = self.canvas.create_text(75, 125, anchor=tk.W, fill = "yellow", text = "Album", font=("Candara", 12))
        
        self.canvas.create_image(50, 150, image=self.imagen_grupo)
        self.canvas_grupo = self.canvas.create_text(75, 150, anchor=tk.W, fill = "yellow", text = "Grupo", font=("Candara", 12))
        
        #Coloca el marco (colocando todo lo anterior)
        frame.grid(row=fila, column=0, sticky="sw")
        
    def crea_botones(self):
        frame = tk.Frame(self.window)
        frame2 = tk.Frame(self.window)        
        icono_track_anterior = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"track_anterior.png"))
        icono_retroceder = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"retroceder.png"))
        self.icono_play = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"play.png"))
        self.icono_reanudar = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"play_rojo.png"))
        icono_stop = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"stop.png"))
        icono_pausa = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"pausa.png"))
        icono_avanzar = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"avanzar.png"))
        icono_track_siguiente = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"track_siguiente.png"))
        self.icono_mute = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"mute.png"))
        self.icono_unmute = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"unmute.png"))
        
        #Para los botones es neceario asignarles la imagen en la declaración y manualmente, sino no funciona :(
        boton_track_anterior = tk.Button(frame, image= icono_track_anterior, borderwidth=0, padx=0, command=self.on_track_anterior)
        boton_track_anterior.image=icono_track_anterior
        
        boton_retroceder = tk.Button(frame, image= icono_retroceder, borderwidth=0, padx=0, command=self.on_retroceder)
        boton_retroceder.image=icono_retroceder
        self.boton_play = tk.Button(frame, image= self.icono_play, borderwidth=0, padx=0, command=self.on_play)
        #self.boton_play.image=self.icono_play
        boton_stop = tk.Button(frame, image= icono_stop, borderwidth=0, padx=0, command=self.on_stop)
        boton_stop.image=icono_stop
        boton_pausa = tk.Button(frame, image= icono_pausa, borderwidth=0, padx=0, command=self.on_pausa)
        boton_pausa.image=icono_pausa
        boton_avanzar = tk.Button(frame, image=icono_avanzar, borderwidth=0, padx=0,command=self.on_avanzar)
        boton_avanzar.image=icono_avanzar
        boton_track_siguiente = tk.Button(frame, image= icono_track_siguiente, borderwidth=0, padx=0, command=self.on_track_siguiente)
        boton_track_siguiente.image=icono_track_siguiente
        self.boton_mute = tk.Button(frame2, image= self.icono_mute, borderwidth=0, padx=0, command=self.on_mute)
        
        self.escala_volumen = tk.Scale(frame2, from_=0, to=10, resolution=0.5, bd=4, sliderlength=15, orient=tk.HORIZONTAL, command=self.on_escala_volumen)
        tk.Label(frame2, text= "Volumen").grid(row=3, column=1, padx=0, sticky="ns")
        
        boton_track_anterior.grid(row=3, column=1, sticky="w")
        boton_retroceder.grid(row=3, column=2, sticky="w")
        self.boton_play.grid(row=3, column=3, sticky="w")
        boton_stop.grid(row=3, column=4, sticky="w")
        boton_pausa.grid(row=3, column=5, sticky="w")
        boton_avanzar.grid(row=3, column=6, sticky="w")
        boton_track_siguiente.grid(row=3, column=7, sticky="w")
        self.escala_volumen.grid(row=3, column=2, sticky="w")
        self.boton_mute.grid(row=3, column=0, sticky="w")
        
        frame.grid(row=4, column=0, sticky="w", pady=4, padx=5)
        frame2.grid(row=4, column=1, sticky="w")
        
        self.escala_volumen.set(5)
        
    def crea_lista(self):
        self.titulo_lista= tk.Label(self.window, text="Play List: ")
        frame = ttk.LabelFrame(self.window, text="play list", labelwidget=self.titulo_lista)
        fila = 1
        
        #Las dimensiones está en número de caracteres
        self.lista = tk.Listbox(frame, activestyle='none', cursor='hand2',
                                   bg='#1C3D7D', fg='#A0B9E9', selectmode=tk.EXTENDED, width=55,  height=20)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.lista.bind("<Double-Button-1>", self.on_play_list)        
        self.lista.bind("<Button-3>", self.mostrar_menu_contextual)
        scroll_bar = tk.Scrollbar(frame)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.BOTH)
        #Hay que asociar la lista y el scrollbar mutuamente
        self.lista.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=self.lista.yview)
        
        frame.grid(
            row = fila, 
            column= 1, 
            rowspan=10, #Se extiende 10 filas hacia abajo (o hasta que llegue al final)
            sticky="wn", #En relación al centro, en qué posición se coloca (en este caso al norte)
            padx=2, #Paddings varios.
            pady=4
        )
        
        
    def crea_menu(self):
        frame = tk.Frame(self.window)
        frame2 = tk.Frame(self.window)
        fila = 0
        icono_add_archivo = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"add_fichero.gif"))
        icono_borrar_archivo = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"borrar_archivo.gif"))
        icono_add_directorio = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"add_directorio.gif"))
        icono_borrar_lista = tk.PhotoImage(file=os.path.join(carpeta_imagenes,"borrar_lista.gif"))
                
        boton_add_archivo = tk.Button(frame, image=icono_add_archivo, borderwidth=0, padx=4, command=self.on_add_archivo)        
        boton_add_archivo.image=icono_add_archivo
        self.bocadillo.bind(boton_add_archivo, "Añadir canción a la lista actual")
        boton_borrar_archivo = tk.Button(frame, text="Eliminar Archivo",image=icono_borrar_archivo, borderwidth=0, padx=4,   command=self.on_borrar_archivo)        
        boton_borrar_archivo.image=icono_borrar_archivo
        self.bocadillo.bind(boton_borrar_archivo, "Eliminar canción(es) seleccionada(s)")
        boton_add_directorio = tk.Button(frame, image=icono_add_directorio, borderwidth=0, padx=0, text="Añadir Directorio", command=self.on_add_directorio)        
        boton_add_directorio.image=icono_add_directorio
        self.bocadillo.bind(boton_add_directorio, "Añadir canciones")
        boton_borrar_lista = tk.Button(frame, image=icono_borrar_lista, borderwidth=0, padx=0, text="Borrar Lista", command=self.on_borrar_lista)        
        boton_borrar_lista.image=icono_borrar_lista
        self.bocadillo.bind(boton_borrar_lista, "Eliminar lista actual")
        
        boton_archivar_lista = ttk.Button(frame2, text="Guardar Lista", command=self.on_guardar_lista)
        boton_cargar_lista = ttk.Button(frame2, text="Cargar Lista", command=self.on_cargar_lista)
                
        boton_add_archivo.grid(row=fila, column=1)
        boton_borrar_archivo.grid(row=fila,column=2)
        boton_add_directorio.grid(row=fila,column=3)
        boton_borrar_lista.grid(row=fila,column=4)
        
        boton_archivar_lista.grid(row=fila, column=0)
        boton_cargar_lista.grid(row=fila,column=1)
                
        frame.grid(row=fila, sticky="w", padx=5)
        frame2.grid(row=fila, column=1, sticky="w")
    
        
    def crea_formulario(self):
        #Para recoger y editar datos de los widget se necesitan tipos propiors de tkinter
        self.titulo = tk.StringVar()
        self.grupo = tk.StringVar()
        self.album = tk.StringVar()
        self.genero= tk.StringVar()
        self.editando=tk.BooleanVar()
        self.editando.set(False)
        
        frame = ttk.LabelFrame(self.window, text="Editor")
        
        tk.Checkbutton(frame, text = "Marcar para Editar", variable=self.editando, command=self.on_editar).grid(row=0, column=0)
        tk.Label(frame, text = "Título").grid(row=1, column=0)
        self.entrada_titulo = ttk.Entry(frame, textvariable=self.titulo)
        self.entrada_titulo.grid(row=1, column=1)
        tk.Label(frame, text= "Grupo").grid(row=2, column=0)
        self.entrada_grupo = ttk.Entry(frame, textvariable=self.grupo)
        self.entrada_grupo.grid(row=2, column=1)
        tk.Label(frame, text= "Álbum").grid(row= 3, column=0)
        self.entrada_album = ttk.Entry(frame, textvariable=self.album)
        self.entrada_album.grid(row=3, column=1, sticky="e")
        tk.Label(frame, text="Genero").grid(row=4, column=0)
        self.entrada_genero = ttk.Entry(frame, textvariable=self.genero)
        self.entrada_genero.grid(row=4, column=1)
        
        self.boton_guardar_formulario= ttk.Button(frame, text="Guardar Datos", command=self.on_guardar_datos)
        self.boton_guardar_formulario.grid(row=4, column=2,  padx=10)
        
        frame.grid(row=1, sticky="w", columnspan=10)
        self.desactivar_formulario()
    
    def crea_menu_contextual(self):
        self.menu_contextual = tk.Menu(self.lista, tearoff=0)
        self.menu_contextual.add_command(label="Añadir Favorito", command=self.on_favorito)
        self.menu_contextual.add_command(label="Quitar Favorito", command=self.on_quitar_favorito)
        
        self.menu_valoración = tk.Menu(self.lista, tearoff=0)
        self.menu_valoración.add_command(label="1 Estrella", command= lambda x=1:self.on_valoración(x))
        self.menu_valoración.add_command(label="2 Estrella", command= lambda x=2:self.on_valoración(x))
        self.menu_valoración.add_command(label="3 Estrella", command= lambda x=3:self.on_valoración(x))
        self.menu_valoración.add_command(label="4 Estrella", command= lambda x=4:self.on_valoración(x))
        self.menu_valoración.add_command(label="5 Estrella", command= lambda x=5:self.on_valoración(x))
        self.menu_contextual.add_cascade(label= "Valoración", menu= (self.menu_valoración))
        
    

#Funciones que se activan cuando sucede un evento    
    
    #Activa o desactiva el formulario y controla la información que se inserta en los cuadros de texto.
    def on_editar(self):
        if self.editando.get():
            self.activar_formulario()
            indice = self.lista.curselection()
            if indice != ():
                indice = self.lista.curselection()[0]
                self.entrada_titulo.delete(0, tk.END)
                self.entrada_album.delete(0, tk.END)
                self.entrada_grupo.delete(0, tk.END)
                self.entrada_genero.delete(0, tk.END)
                self.entrada_grupo.insert(0, self.tracks.grupo(indice))
                self.entrada_album.insert(0, self.tracks.album(indice))
                self.entrada_titulo.insert(0, self.tracks.titulo(indice))
                self.entrada_genero.insert(0, self.tracks.genero(indice))            
        else:
            self.desactivar_formulario()
        
    #Se dispara cuando se accede al menú contextual y se pulsa en "Añadir favorito".
    def on_favorito(self):
        indice = self.lista.curselection()
        for i in indice:
            self.lista.itemconfigure(i, fg="DarkOrange")
            self.tracks.favorito(i)
    
    #Se dispara cuando se accede al menú contextual y se pulsa en "Quitar favorito".
    def on_quitar_favorito(self):
        if self.tracks.nombre_lista()=="favoritos":
            #Informa de que solo se pueden quitar favoritos dentro de la propia lista de favoritos mediante el botón de eliminar elemento de la lista
            tkinter.messagebox.showinfo("Favoritos", "Para borrar un favorito en la lista de favoritos utilice borrar elemento de la playlist")
            return
                    
        indice = self.lista.curselection()
        for i in indice:            
            self.lista.itemconfigure(i, fg='#A0B9E9')
            self.tracks.quitar_favorito(i)  
        
    #Se dispara cuando se accede al menú contextual y se pulsa en "Valoración favorito". Se tomará el valor elegido por el usuario.
    def on_valoración(self, num_estrellas):
        indice = self.lista.curselection()
        for i in indice:
            self.tracks.valoracion(i,num_estrellas)
        
        self.lista.delete(0, tk.END)
        for i in range(0, len(self.tracks.playlist)):
             self.lista.insert(tk.END, self.tracks.titulo(i))
             if self.tracks.es_favorito(i):
                 self.lista.itemconfigure(i,fg="DarkOrange")
    
    #Se activa cuando se pulsa en el botón "Silenciar/No Silenciar" y activará una función u otra.
    def on_mute(self):
        if not self.mute:
            self.gramola.silenciar()
            self.escala_volumen.set(0.0)
            self.boton_mute.configure(image=self.icono_unmute)
            self.mute = True
        else:
            self.gramola.volumen(5)
            self.escala_volumen.set(5)
            self.boton_mute.configure(image=self.icono_mute)
            self.mute = False
        
    #Se activa cuando se pulsa el botón "Guardar datos". Guarda los metadatos del archivo seleccionado.     
    def on_guardar_datos(self):
        indice = self.lista.curselection()
        if indice == ():
            #Mensaje de que no hay ninguno seleccionado (suele quitarse la selección de la canción seleccionada cuando se marca editar).
            tkinter.messagebox.showerror("Error", "Debes tener seleccionado un track de la lista")
        else:
            indice = self.lista.curselection()[0]
        indice = self.lista.curselection()[0]
        titulo = self.titulo.get()
        grupo = self.grupo.get()
        album= self.album.get()
        genero = self.genero.get()
        
        self.tracks.actualizar_track(indice, titulo, grupo, album, genero)
        self.lista.delete(0,tk.END)
        for i in range(0, len(self.tracks.playlist)):
            self.lista.insert(tk.END, self.tracks.titulo(i))
            if self.tracks.es_favorito(i):
                self.lista.itemconfigure(i,fg="DarkOrange")
       
    #Se activa cuando se pulsa el botón de "retroceder canción". Si es la primera canción no hará nada.
    def on_track_anterior(self):
        indice = self.lista.curselection()[0]
        if (indice-1) >= 0:
            self.lista.selection_clear(indice)
            indice -= 1
            self.lista.select_set(indice )
            self.reproduce_track(indice)            
        else:
            self.reproduce_track(indice)
      
    #Si está pausada la reproducción la reanudará. En caso contrario carga de nuevo la canción. Asociado al botón de play.
    def on_play(self):
             
        if not self.pausado:
            indice = self.lista.curselection()            
            if indice == ():
                return
            self.reproduce_track(indice[0])
            
        else:
            self.gramola.reanudar()
            self.pausado = False
            self.boton_play.configure(image=self.icono_play)
            indice = self.lista.curselection()            
            if indice == ():
                return
            self.actualizar_datos(indice[0])

    #Detiene la reproducción y marca la información como si nada se estuviese reproduciendo. Asociado al botón stop.
    def on_stop(self):
        self.gramola.parar()
        self.canvas.itemconfig(self.nombre_track, text="No hay nada reproduciéndose")
        self.canvas.itemconfig(self.tiempo, text="00:00")
        self.canvas.itemconfig(self.duracion_track, text=" de  00:00")
        self.canvas.itemconfig(self.canvas_grupo, text="Albúm")
        self.canvas.itemconfig(self.canvas_album, text="Grupo")
        self.pausado = False
        self.boton_play.configure(image=self.icono_play)
     
    #Pausa la reproducción de la canción actual. Asociado al botón pausa.
    def on_pausa(self):
        self.pausado = True
        self.boton_play.configure(image=self.icono_reanudar)
        self.gramola.pausa()
    
    #Avanza 5 segundos la reproducción. Asociado al botón avanzar reproducción.
    def on_avanzar(self):
        self.gramola.avanzar()
        if self.mute:
            self.on_mute()

    #Retrocede 5 segundos la reproducción. Asociado al botón retroceder reproducción.
    def on_retroceder(self):
        self.gramola.retroceder()
        if self.mute:
            self.on_mute()

    #Pasa a reproducir la siguiente canción en la lista de reproducción. Asociado al botón siguiente canción.
    #Si está reproduciendo la última y se pulsa vuelve a empezar.
    def on_track_siguiente(self):
        indice = self.lista.curselection()[0]
        if (indice+1) < self.lista.size():
            self.lista.selection_clear(indice)
            indice += 1
            self.lista.select_set(indice )
            self.reproduce_track(indice)
            
        else:
            self.lista.selection_clear(indice)            
            self.lista.select_set(0)
            self.reproduce_track(0)
    
    #Si se hace doble click sobre una canción de la lista de reproducción se dispara.
    #Reproduce la canción sobre la que se hace doble click.
    def on_play_list(self, event):
        indice = self.lista.curselection()
        self.reproduce_track(indice[0])           

    #Asociado al botón "+", abre el explorador de archivos y permite añadir UN ÚNICO archivo a la lista de reproducción actual.
    #Sólo muestra archivos que puede reproducir.
    def on_add_archivo(self):
        archivo_audio = tkinter.filedialog.askopenfilename(filetypes=[(
            'Todos', '.mp3 .wav .ogg .flac'), ('archivos .mp3 ', '.mp3'), ('archivos .wav', '.wav'), ('archivos .ogg', '.ogg'), ('archivos .flac', '.flac'),])
        if archivo_audio:            
            self.tracks.add_track(archivo_audio)            
            self.lista.insert(tk.END, self.tracks.titulo(self.lista.size()))
      
    #Asociado al botón "-", permite eliminar los ARCHIVOS SELECCIONADOS de la lista de reproducción actual.
    def on_borrar_archivo(self):
        try:
            indices = self.lista.curselection()
            for indice in reversed(indices):
                self.lista.delete(indice)
                self.tracks.eliminar_track(indice)
        except IndexError:
            pass

    #Asociado al botón "Carpeta", abre el explorador de archivos y permite añadir VARIOS archivos a la lista de reproducción actual.
    #Sólo muestra archivos que puede reproducir.
    def on_add_directorio(self):
        conjunto_archivos_audio = tkinter.filedialog.askopenfilenames(filetypes=[(
            'Todos', '.mp3 .wav .ogg .flac'), ('archivos .mp3 ', '.mp3'), ('archivos .wav', '.wav'), ('archivos .ogg', '.ogg'), ('archivos .flac', '.flac'),])
        
        if conjunto_archivos_audio:
                for archivo_audio in conjunto_archivos_audio:
                    self.tracks.add_track(archivo_audio)
                    
                self.lista.delete(0,tk.END)
                for i in range(0, len(self.tracks.playlist)):
                    self.lista.insert(tk.END, self.tracks.titulo(i))
                   
                    if self.tracks.es_favorito(i):
                        self.lista.itemconfigure(i,fg="DarkOrange")
                      
    #Asociado al botón "Carpeta tachada". Elimina la lista de reproducción actual (si es una lista cargada no la elimina del almacenamiento).
    def on_borrar_lista(self):
        self.tracks.borrar_playlist()
        self.lista.delete(0,tk.END)
        self.titulo_lista.configure(text="Play List: ")
    
    #Asociado al botón "Guardar lista", guarda la lista de reproducción actual.
    #Se abre el explorador de archivos y se permite elegir el directorio de destino y el nombre de la lista (permite sobreescibir).
    def on_guardar_lista(self):
        carpeta_listas = os.path.abspath(os.path.join(os.path.dirname(__file__), 'listas'))
        archivo_lista = tkinter.filedialog.asksaveasfilename(initialdir= carpeta_listas)
        if archivo_lista:
            self.tracks.grabar_lista(archivo_lista)
        self.titulo_lista.configure(text="Play List: "+self.tracks.nombre_lista())
        
    #Abre el explorador de archivos y permite cargar la lista de reproducción seleccionada. Asociado al botón cargar lista.
    def on_cargar_lista(self):
        carpeta_listas = os.path.abspath(os.path.join(os.path.dirname(__file__), 'listas'))
        archivo_lista = tkinter.filedialog.askopenfilename(initialdir=carpeta_listas)
        if archivo_lista:
            self.on_borrar_lista()
            self.tracks.cargar_lista(archivo_lista)
        
        for i in range(0, len(self.tracks.playlist)):
             self.lista.insert(tk.END, self.tracks.titulo(i))
             if self.tracks.es_favorito(i):
                 self.lista.itemconfigure(i,fg="DarkOrange")
                 
        self.titulo_lista.configure(text="Play List: "+self.tracks.nombre_lista())
        
    #Asociada a la escala de volumen. Controla dicha escala.
    def on_escala_volumen(self, event):
        self.gramola.volumen(self.escala_volumen.get())
        if self.escala_volumen.get() > 0:
            self.boton_mute.configure(image=self.icono_mute)
            self.mute = False
        else:
            self.boton_mute.configure(image=self.icono_unmute)
            self.mute = True
        
    

#Funciones

    #Despliega el menú contextual
    def mostrar_menu_contextual(self, event):
        self.menu_contextual.tk_popup(event.x_root, event.y_root)
    
    #Desactiva la posibilidad de alterar los campos del formulario de edicicón de metadatos. Se marcan en gris.
    def desactivar_formulario(self):
        self.entrada_album.configure(state="disable")
        self.entrada_grupo.configure(state="disable")
        self.entrada_titulo.configure(state="disable")
        self.entrada_genero.configure(state="disable")
        self.boton_guardar_formulario.configure(state="disable")        
    
    #Activa la posibilidad de alterar los campos del formulario de edición de metadatos.
    def activar_formulario(self):
        self.entrada_album.configure(state="enable")
        self.entrada_grupo.configure(state="enable")
        self.entrada_titulo.configure(state="enable")
        self.entrada_genero.configure(state="enable")
        self.boton_guardar_formulario.configure(state="enable")        
            
    #Actualiza la información de la canción que se está reproduciendo en este momento (y del formulario).
    def actualizar_datos(self, indice):
        self.canvas.itemconfig(self.nombre_track, text=self.tracks.titulo(indice))
        self.canvas.itemconfig(self.duracion_track, text=self.gramola.duracion())
        self.canvas.itemconfig(self.canvas_grupo, text=self.tracks.grupo(indice))
        self.canvas.itemconfig(self.canvas_album, text=self.tracks.album(indice))
        self.activar_formulario()
        self.entrada_titulo.delete(0, tk.END)
        self.entrada_album.delete(0, tk.END)
        self.entrada_grupo.delete(0, tk.END)
        self.entrada_genero.delete(0, tk.END)
        self.entrada_grupo.insert(0, self.tracks.grupo(indice))
        self.entrada_album.insert(0, self.tracks.album(indice))
        self.entrada_titulo.insert(0, self.tracks.titulo(indice))
        self.entrada_genero.insert(0, self.tracks.genero(indice))
        self.desactivar_formulario()
        
    #Supervisa y actualiza la reproducción de la canción actual, controlando cuando debe pasar a la siguiente.
    def vigila_reproduccion(self):
        tiempo_reproducido = self.gramola.tiempo_reproducido()
        self.canvas.itemconfig(self.tiempo, text=tiempo_reproducido)
        if self.gramola.se_esta_reproduciendo():
            self.window.after(1000, self.vigila_reproduccion)
        else:    
            self.on_track_siguiente()
    
    #Trata de reproducir el elemento de la lista de reproducción actual que esté señalado.
    def reproduce_track(self, indice):
        if not  self.gramola.play(self.tracks.cancion(indice)):
                #Si no se puede reproducir se avisa de que es posible que no exista el archivo.
                tkinter.messagebox.showerror("Error", "Probablemente el fichero no exista:\nFichero: "+self.tracks.playlist[indice]["fichero"])
                self.on_stop()
                return
        self.actualizar_datos(indice)
        self.vigila_reproduccion()
        if self.pausado:
            self.pausado = False
            self.boton_play.configure(image=self.icono_play)   
        if self.mute:
            self.on_mute()

if __name__ == '__main__':
    window = tk.Tk()
    gramola = gramola.Gramola()
    tracks = tracks.Tracks()
    app = App_Music(window, tracks, gramola)
    window.mainloop()
    