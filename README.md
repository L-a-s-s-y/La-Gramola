# La Gramola

Un sencillo reproductor de música hecho con python y ffmpeg.

Permite crear, guardar y cargar listas de reproducción.

GUI minimalista mediante TKinter.

## Imports necesarios
- [Pmw](https://pypi.org/project/Pmw/) sirve para los mensajes emergentes.
- [json](https://docs.python.org/3/library/json.html) para gestionar las listas guardadas.
- [eyed3](https://pypi.org/project/eyeD3/) para gestionar metadatos.
- [pyglet](https://pypi.org/project/pyglet/) que se encarga de la reproducción del audio.

## Software adicional
- [Tkinter](https://wiki.python.org/moin/TkInter) para la GUI. No se instala con pip. Se debe hacer manualmente para cada SO.
- [FFmpeg](https://ffmpeg.org/) como base para que pyglet pueda reproducir los archivos de audio.