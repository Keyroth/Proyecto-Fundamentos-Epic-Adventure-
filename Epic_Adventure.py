import tkinter as tk

###########################################################################
####Aqui creo la ventana incial donde se controlara el inicio del juego####
###########################################################################

ventana_inicial = tk.Tk()
ventana_inicial.title("EPIC ADVENTURE")
ventana_inicial.geometry("800x600+250+80")
ventana_inicial.resizable(False, False)
ventana_inicial.configure(bg="#2c3e50")

# TÍTULO
titulo = tk.Label(
    ventana_inicial, 
    text="EPIC ADVENTURE", 
    font=("Impact", 36, "bold"),
    bg="#2c3e50",
    fg="#DAA520"
)
titulo.place(relx=0.5, y=80, anchor="center")  

#ETIQUETA para Ingresar el Nombre
etiqueta_nombre = tk.Label(
    ventana_inicial, 
    text="Ingrese Su Nombre", 
    bg="#DAA520", 
    font=("Impact", 18),
    highlightthickness=2,
    highlightbackground="black",
    padx=20,
    pady=10
)
etiqueta_nombre.place(relx=0.5, y=180, anchor="center") 


# Variable para ir guardand oel nombre en mayusculas 
nombre_jugador = tk.StringVar()

# Función que convierte a mayúsculas automáticamente se este escribiendo 
def convertir_mayusculas(*args):
    texto = nombre_jugador.get()
    if texto != texto.upper():
        nombre_jugador.set(texto.upper())

nombre_jugador.trace('w', convertir_mayusculas) #la w es solo un modo que especifica cuando la funcion de callback debe ejecutarse 
                                                #osea se ejecuta cada vez que surge un cambio en la variable 


#ENTRY para poder poner el nombre 
caja_nombre = tk.Entry(
    ventana_inicial, 
    width=35,
    font=("Arial", 14),
    justify="center",
    textvariable=nombre_jugador
)
caja_nombre.place(relx=0.5, y=228, anchor="center", width=300)

def abrir_pesonajes():
    ventana_personajes = tk.Toplevel(ventana_inicial)
    ventana_personajes.title("Seleccion de personajes")
    ventana_personajes.geometry("600x500+350+150")
    ventana_personajes.resizable(False, False)
    ventana_personajes.configure(bg="#2c3e50")    

    ventana_personajes.transient(ventana_inicial)#con esto lo mantengo por encima de la principal, y si la ventana principal se cierra esta se cerrara 
    ventana_personajes.grab_set()#y con esto hago que la ventana sea modal  osea que si se usa esta no se pueda interactuar con la principal 
    
    titulo_personajes = tk.Label(
        ventana_personajes,
        text="Selecciona Tres Personajes",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )    
    titulo_personajes.pack(pady=30)

    # Botón Salir
    boton_salir = tk.Button(
        ventana_personajes,
        text="SALIR",
        font=("Impact", 12),
        bg="#DAA520",
        width=10,
        height=1,
        command=ventana_personajes.destroy  # Cierra la ventana About
    )
    boton_salir.place(x=20, y=450)  # Posición abajo a la izquierda





    
# esta funcion me permite abrir la ventana de sobre 
def abrir_about():
    # Crear la ventana About
    ventana_about = tk.Toplevel(ventana_inicial)
    ventana_about.title("Acerca de Epic Adventure")
    ventana_about.geometry("600x500+350+150")
    ventana_about.resizable(False, False)
    ventana_about.configure(bg="#2c3e50")
     
    ventana_about.transient(ventana_inicial)#con esto lo mantengo por encima de la principal, y si la ventana principal se cierra esta se cerrara 
    ventana_about.grab_set()#y con esto hago que la ventana sea modal  osea que si se usa esta no se pueda interactuar con la principal 
    
    # Título de la ventana About
    titulo_about = tk.Label(
        ventana_about,
        text="ACERCA DEL JUEGO",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )
    titulo_about.pack(pady=30)
    
    # Texto informativo del juego
    texto_info = """EPIC ADVENTURE es un juego de aventuras
épicas donde eres un guardian de personajes de peliculas animadas y 
tendras que luchar contra los hollows, para rescatarlos, una ves hayas 
derrotado a un enemigo,el personaje pasara a ser parte de tu equipo para 
ayudarte en tu aventura y rescatar a los demas.

Características:
-Elige tres personajes iniciales 
-Escoje tu avatar 
-Explora los 5 mundos 
-Enfrenta a los hollows en epicas batallas


BUENA SUERTE GUARDIAN"""
    
    etiqueta_info = tk.Label(
        ventana_about,
        text=texto_info,
        font=("Arial", 12),
        bg="#2c3e50",
        fg="white",
        justify="left"
    )
    etiqueta_info.pack(pady=20)
    
    # Botón Salir
    boton_salir = tk.Button(
        ventana_about,
        text="SALIR",
        font=("Impact", 12),
        bg="#DAA520",
        width=10,
        height=1,
        command=ventana_about.destroy  # Cierra la ventana About
    )
    boton_salir.place(x=20, y=450)  # Posición abajo a la izquierda





# aqui tengo los 4 botones en la ventana principal 

# Botón para seleccionar los personajes
boton1 = tk.Button(
    ventana_inicial, 
    text="Personajes", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_pesonajes #esto es para que salga la ventana de seleccionar los personajes 
)
boton1.place(relx=0.5, y=320, anchor="center")

# Botón para seleccionar el avatar 
boton2 = tk.Button(
    ventana_inicial, 
    text="Avatar", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton2.place(relx=0.5, y=370, anchor="center")

# Botón para iciar el juego 
boton3 = tk.Button(
    ventana_inicial, 
    text="Iniciar", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton3.place(relx=0.5, y=420, anchor="center")

# Botón sobre que trata el juego 
boton4 = tk.Button(
    ventana_inicial, 
    text="About", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_about #esto es para conectar el boton a la funcion 
)
boton4.place(relx=0.5, y=470, anchor="center")

ventana_inicial.mainloop()

