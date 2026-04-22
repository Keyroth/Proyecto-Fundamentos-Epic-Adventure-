import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os  # Se agrega os para construir rutas que funcionen en cualquier computadora


# aqui guardo los datos del jugador
datos_jugador = {
    "nombre": "",
    "avatar": "",
    "personajes": []
}

###########################################################################
# Aqui guardo las estadisticas de cada personaje                          #
# Cada personaje tiene: rol, ataque, defensa y vida                       #
# Los roles son: "Ataque", "Defensa" o "Balanceado"                       #
# Personajes de Ataque:     ataque 20-30 | defensa 10-20 | vida 80-100   #
# Personajes de Defensa:    ataque 10-20 | defensa 20-30 | vida 100-200  #
# Personajes Balanceados:   ataque 20-30 | defensa 20-30 | vida 100-150  #
###########################################################################
personajes_stats = {

    # PERSONAJES DE ATAQUE
    "HERCULES": {"rol": "Ataque",     "ataque": 30, "defensa": 12, "vida": 100},
    "GENIO":    {"rol": "Ataque",     "ataque": 28, "defensa": 15, "vida": 90},
    "SIMBA":    {"rol": "Ataque",     "ataque": 26, "defensa": 14, "vida": 95},
    "SPIRIT":   {"rol": "Ataque",     "ataque": 25, "defensa": 10, "vida": 85},
    "TARZAN":   {"rol": "Ataque",     "ataque": 27, "defensa": 13, "vida": 88},
    "BAMBI":    {"rol": "Ataque",     "ataque": 20, "defensa": 11, "vida": 80},

    # PERSONAJES DE DEFENSA
    "BESTIA":   {"rol": "Defensa",    "ataque": 15, "defensa": 28, "vida": 180},
    "BEIMAX":   {"rol": "Defensa",    "ataque": 10, "defensa": 30, "vida": 200},
    "RAPUNZEL": {"rol": "Defensa",    "ataque": 12, "defensa": 25, "vida": 150},
    "REY":      {"rol": "Defensa",    "ataque": 14, "defensa": 22, "vida": 130},
    "OLAF":     {"rol": "Defensa",    "ataque": 10, "defensa": 20, "vida": 120},
    "LUMIER":   {"rol": "Defensa",    "ataque": 11, "defensa": 24, "vida": 140},

    # PERSONAJES BALANCEADOS
    "ARIEL":    {"rol": "Balanceado", "ataque": 22, "defensa": 22, "vida": 110},
    "JACK":     {"rol": "Balanceado", "ataque": 25, "defensa": 24, "vida": 120},
    "ARROYO":   {"rol": "Balanceado", "ataque": 23, "defensa": 21, "vida": 115},
    "HEYHEY":   {"rol": "Balanceado", "ataque": 26, "defensa": 23, "vida": 130},
    "JUDIT":    {"rol": "Balanceado", "ataque": 24, "defensa": 25, "vida": 125},
    "BOLT":     {"rol": "Balanceado", "ataque": 20, "defensa": 20, "vida": 100}
}

###########################################################################
####Aqui creo la ventana incial donde se controlara el inicio del juego####
###########################################################################

ventana_inicial = tk.Tk()
ventana_inicial.title("EPIC ADVENTURE")
ventana_inicial.geometry("800x600+250+80")
ventana_inicial.resizable(False, False)
ventana_inicial.configure(bg="#2c3e50")

titulo = tk.Label(
    ventana_inicial, 
    text="EPIC ADVENTURE", 
    font=("Impact", 36, "bold"),
    bg="#2c3e50",
    fg="#DAA520"
)
titulo.place(relx=0.5, y=80, anchor="center")  

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

nombre_jugador = tk.StringVar()

#aqui simplemente convierto lo que entra en el entry y lo hago en mayuscula
def convertir_mayusculas(*args):
    texto = nombre_jugador.get()
    if texto != texto.upper():
        nombre_jugador.set(texto.upper())
    datos_jugador["nombre"] = nombre_jugador.get()

#esto hace que se vaya convirtiendo en mayuscula conforme lo vaya escribiendo
nombre_jugador.trace_add('write', convertir_mayusculas)

caja_nombre = tk.Entry(
    ventana_inicial, 
    width=35,
    font=("Arial", 14),
    justify="center",
    textvariable=nombre_jugador
)
caja_nombre.place(relx=0.5, y=228, anchor="center", width=300)


###########################################################################
####              VENTANA DE SELECCION DE PERSONAJES                   ####
###########################################################################

def abrir_pesonajes():

    ventana_personajes = tk.Toplevel(ventana_inicial)
    ventana_personajes.title("Seleccion de personajes")
    ventana_personajes.geometry("850x600+200+50")
    ventana_personajes.resizable(False, False)
    ventana_personajes.configure(bg="#2c3e50")    

    ventana_personajes.transient(ventana_inicial)
    ventana_personajes.grab_set()

    # Título
    titulo_personajes = tk.Label(
        ventana_personajes,
        text="Selecciona Tres Personajes",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )    
    titulo_personajes.pack(pady=15)

    # aqui cuento cuantos personajes ha seleccionado nada mas
    etiqueta_conteo = tk.Label(
        ventana_personajes,
        text="Personajes elegidos: 0 / 3",
        font=("Impact", 14),
        bg="#2c3e50",
        fg="white"
    )
    etiqueta_conteo.pack(pady=5)

    ###########################################################################                                        
    # me di cuenta que para el scroll ocupo estas tres cosas                     
    # frame                 
    # canvas  
    # scrollbar         
    ###########################################################################

    # este es el frame
    frame_contenedor = tk.Frame(ventana_personajes, bg="#2c3e50")
    frame_contenedor.pack(fill="both", expand=True, padx=10)

    # Scrollbar 
    scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Canvas y se conecta al scrollbar con el parametro yscrollcommand
    canvas = tk.Canvas(
        frame_contenedor,
        bg="#2c3e50",
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )
    canvas.pack(side="left", fill="both", expand=True)

    # Se conecta el scrollbar al canvas para que muevan juntos
    scrollbar.config(command=canvas.yview)

    # Frame interior que vive dentro del canvas y contiene la cuadricula
    frame_cuadricula = tk.Frame(canvas, bg="#2c3e50")

    # Se inserta el frame de la cuadricula, dentro del canvas como una ventana interna
    # anchor="n" lo ancla en la parte superior centrado
    canvas.create_window(
        (0, 0),
        window=frame_cuadricula,
        anchor="nw"
    )

    # Funcion que actualiza la region de scroll cuando cambia el tamaño del contenido
    # Se ejecuta automaticamente 
    def actualizar_scroll(event):
        # Se le dice al canvas cuanta area total tiene para bajar y subir 
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Se vincula la funcion al evento de cambio de tamaño del frame interior
    frame_cuadricula.bind("<Configure>", actualizar_scroll)

    # Funcion que permite usar la rueda del mouse para hacerlo para arriba y abajo con el mouse
    def scroll_con_mouse(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Se vincula la rueda del mouse al canvas
    canvas.bind("<MouseWheel>", scroll_con_mouse)

    # Lista de los 18 personajes con sus archivos reales
    personajes = [
        {"nombre": "ARIEL",      "archivo": "Ariel.png"},
        {"nombre": "ARROYO",     "archivo": "Arroyo.png"},
        {"nombre": "BAMBI",      "archivo": "Bambi.png"},
        {"nombre": "BEIMAX",     "archivo": "Beimax.png"},
        {"nombre": "BESTIA",     "archivo": "Bestia.png"},
        {"nombre": "BOLT",       "archivo": "Bolt.png"},
        {"nombre": "GENIO",      "archivo": "Genio.png"},
        {"nombre": "HERCULES",   "archivo": "Hercules.png"},
        {"nombre": "HEYHEY",     "archivo": "Heyhey.png"},
        {"nombre": "JACK",       "archivo": "Jack.png"},
        {"nombre": "JUDIT",      "archivo": "Judit.png"},
        {"nombre": "LUMIER",     "archivo": "Lumier.png"},
        {"nombre": "OLAF",       "archivo": "Olaf.png"},
        {"nombre": "RAPUNZEL",   "archivo": "Rapunzel.png"},
        {"nombre": "REY",        "archivo": "Rey.png"},
        {"nombre": "SIMBA",      "archivo": "Simba.png"},
        {"nombre": "SPIRIT",     "archivo": "Spirit.png"},
        {"nombre": "TARZAN",     "archivo": "Tarzan.png"}
    ]

    # CAMBIO 2: ruta_base ahora usa os para buscar la carpeta Imagenes
    # al lado del archivo .py sin importar en que computadora se corra
    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")

    referencias_imagenes  = []
    referencias_oscuras   = []
    botones_personajes    = []
    seleccionados_local   = []

    ###########################################################################
    # Oscurece los botones no seleccionados, lo hice con recursividad en cola##
    ###########################################################################

    #lo que hago es oscurecer como en los juegos los personajes que no seleccione 
    def oscurecer_no_seleccionados(lista_botones, indice):

        # este es mi caso base, porque si el indice supera la lista, la recursion termina
        if indice >= len(lista_botones):
            return

        nombre_boton = lista_botones[indice]["nombre"]

        if nombre_boton not in seleccionados_local:
            lista_botones[indice]["boton"].config(
                image=lista_botones[indice]["imagen_oscura"],
                state="disabled"
            )

        # esta es la llamada recursiva
        oscurecer_no_seleccionados(lista_botones, indice + 1)

    ###########################################################################
    # Reactiva los botones al pulsarlos otra vez                              #
    ###########################################################################
    def reactivar_botones(lista_botones, indice):

        # este es mi caso base
        if indice >= len(lista_botones):
            return

        nombre_boton = lista_botones[indice]["nombre"]

        if nombre_boton not in seleccionados_local:
            lista_botones[indice]["boton"].config(
                image=lista_botones[indice]["imagen_normal"],
                state="normal"
            )

        reactivar_botones(lista_botones, indice + 1)

    ###########################################################################
    # Maneja la seleccion y deseleccion de personajes                         #
    ###########################################################################
    def seleccionar_personaje(nombre, indice):

        if nombre in seleccionados_local:
            seleccionados_local.remove(nombre)

            botones_personajes[indice]["boton"].config(
                image=botones_personajes[indice]["imagen_normal"],
                relief="raised",
                bd=2
            )

            etiqueta_conteo.config(
                text="Personajes elegidos: " + str(len(seleccionados_local)) + " / 3"
            )

            reactivar_botones(botones_personajes, 0)
            datos_jugador["personajes"] = list(seleccionados_local)
            return

        if len(seleccionados_local) >= 3:
            return

        seleccionados_local.append(nombre)

        botones_personajes[indice]["boton"].config(
            relief="solid",
            bd=4
        )

        etiqueta_conteo.config(
            text="Personajes elegidos: " + str(len(seleccionados_local)) + " / 3"
        )

        if len(seleccionados_local) == 3:
            oscurecer_no_seleccionados(botones_personajes, 0)

        datos_jugador["personajes"] = list(seleccionados_local)

    ###########################################################################
    #aqui use recursividad pero en pila para crear los cuadros de personajes  #
    ###########################################################################
    def crear_personajes_recursivo(lista_personajes, indice):

        # mi caso base aca es si el indice llega al final, la recursion termina
        if indice >= len(lista_personajes):
            return

        personaje_actual = lista_personajes[indice]

        fila    = indice // 5
        columna = indice  % 5

        # Se crea un frame individual para cada personaje que agrupa
        # el nombre arriba, la imagen en el medio y el boton es la imagen misma
        frame_celda = tk.Frame(frame_cuadricula, bg="#2c3e50")
        frame_celda.grid(row=fila, column=columna, padx=10, pady=5)

        # Etiqueta con el nombre del personaje encima de la imagen
        # width=10 hace que todos los nombres tengan el mismo ancho
        # y se vean simetricos en la cuadricula
        etiqueta_nombre_personaje = tk.Label(
            frame_celda,
            text=personaje_actual["nombre"],
            font=("Impact", 10),
            bg="#2c3e50",
            fg="#DAA520",
            width=10
        )
        etiqueta_nombre_personaje.pack()

        # est etry fue algo que me encanto usar porque solo trata de correr
        #el codigo y si encuentra algo que falla, no se rompe, solo brinca al except
        try:
            #abre las imagenes desde la carpeta 
            imagen_original = Image.open(os.path.join(ruta_base, personaje_actual["archivo"]))
            #y aqui solo le redimenciono su tamaño
            imagen_original = imagen_original.resize((120, 130))
        except:
            #Crea un cuadro gris del mismo tamaño como reemplazo visual para que la cuadricula
            #no quede con huecos aunque falte la imagen
            imagen_original = Image.new("RGB", (120, 130), color="#555555")

        #Crea una herramienta de brillo sobre la imagen. Todavía no hace nada,
        #solo la prepara para poder modificarla
        enhancer          = ImageEnhance.Brightness(imagen_original)
        #Aplica el brillo reducido al 30%, produciendo la version oscura de la imagen que se usará cuando el 
        #personaje ya no esté disponible para seleccionar
        imagen_oscura_pil = enhancer.enhance(0.3)

        #aqui solo lo convierto para que tkinter lo pueda mostrar
        imagen_normal_tk = ImageTk.PhotoImage(imagen_original)
        imagen_oscura_tk = ImageTk.PhotoImage(imagen_oscura_pil)

        #Guarda la imagen normal en la lista de referencias para que Python no 
        #la elimine de memoria y desaparezca de la pantalla
        referencias_imagenes.append(imagen_normal_tk)
        referencias_oscuras.append(imagen_oscura_tk)

        #creo el boton de la cuadricula de cada personaje
        # el boton ahora va dentro del frame_celda para quedar debajo del nombre
        boton = tk.Button(
            frame_celda,
            image=imagen_normal_tk,
            bg="#2c3e50",
            relief="raised",
            bd=2,
            cursor="hand2",
            command=lambda i=indice, n=personaje_actual["nombre"]: seleccionar_personaje(n, i)
        )
        boton.pack()

        botones_personajes.append({
            "nombre":        personaje_actual["nombre"],
            "boton":         boton,
            "imagen_normal": imagen_normal_tk,
            "imagen_oscura": imagen_oscura_tk
        })

        #se procesa el siguiente personaje
        crear_personajes_recursivo(lista_personajes, indice + 1)

    # Se lanza la recursion desde el indice 0
    crear_personajes_recursivo(personajes, 0)

    # Boton SALIR fijo en la parte inferiorde abaji, fuera del area que baja y sube
    boton_salir = tk.Button(
        ventana_personajes,
        text="SALIR",
        font=("Impact", 12),
        bg="#DAA520",
        width=10,
        height=1,
        command=ventana_personajes.destroy
    )
    boton_salir.pack(pady=10)


###########################################################################
####              VENTANA DE SELECCION DE AVATAR                       ####
###########################################################################

def abrir_avatar():
    #Crea una variable especial de tkinter para guardar texto, y la inicializa vacía.
    #Guardará el nombre del avatar que el jugador elija
    avatar_seleccionado = tk.StringVar()
    avatar_seleccionado.set("")

    #esta es la función que se ejecuta cuando el jugador presiona el botón de un avatar. 
    #Hace tres cosas: guarda el nombre en la variable local, lo guarda en el diccionario global 
    #para usarlo después, y actualiza el texto de confirmación en pantalla.
    def seleccionar_avatar(nombre):
        avatar_seleccionado.set(nombre)
        datos_jugador["avatar"] = nombre
        etiqueta_confirmacion.config(text="Avatar seleccionado: " + nombre)

    #esto simplemente hace la ventana
    ventana_avatar = tk.Toplevel(ventana_inicial)
    ventana_avatar.title("Seleccion de Avatar")
    ventana_avatar.geometry("700x550+300+100")
    ventana_avatar.resizable(False, False)
    ventana_avatar.configure(bg="#2c3e50")

    ventana_avatar.transient(ventana_inicial)
    ventana_avatar.grab_set()

    #titulo
    titulo_avatar = tk.Label(
        ventana_avatar,
        text="SELECCIONA TU AVATAR",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )
    titulo_avatar.pack(pady=20)

    #esta es la caja que contiene los avatares a elegir
    frame_avatares = tk.Frame(ventana_avatar, bg="#2c3e50")
    frame_avatares.pack(pady=10)

    # CAMBIO 3: ruta_base ahora usa os para buscar la carpeta Imagenes
    # al lado del archivo .py sin importar en que computadora se corra
    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")

    avatares = [
        {"nombre": "BATMAN",  "archivo": "Avatar_Batman_frente.png"},
        {"nombre": "KRATOS",  "archivo": "Avatar_Kratos_Frente.png"},
        {"nombre": "NEITIRY", "archivo": "Avatar_Neitiry_frente.png"}
    ]

    #aqui se guardaran las imagenes en memoria para que python no las
    #elimine
    referencias_imagenes = []

    #Esta Función recursiva crea los avatares uno por uno. 
    # El caso base detiene la recursión cuando ya no quedan avatares en la lista.
    def crear_avatares_recursivo(lista_avatares):

        if len(lista_avatares) == 0:
            return

        avatar_actual  = lista_avatares[0]
        resto_avatares = lista_avatares[1:]

        frame_individual = tk.Frame(frame_avatares, bg="#2c3e50")
        frame_individual.pack(side="left", padx=20)#Crea una caja individual para este avatar dentro del frame general. side="left" hace que cada avatar se coloque a la derecha del anterior

        imagen    = Image.open(os.path.join(ruta_base, avatar_actual["archivo"]))
        imagen    = imagen.resize((150, 180))
        imagen_tk = ImageTk.PhotoImage(imagen)

        referencias_imagenes.append(imagen_tk)

        etiqueta_imagen = tk.Label(
            frame_individual,
            image=imagen_tk,
            bg="#2c3e50"
        )
        etiqueta_imagen.pack()
        etiqueta_imagen.image = imagen_tk

        boton_nombre = tk.Button(
            frame_individual,
            text=avatar_actual["nombre"],
            font=("Impact", 13),
            bg="#DAA520",
            fg="#2c3e50",
            width=10,
            height=1,
            command=lambda n=avatar_actual["nombre"]: seleccionar_avatar(n)
        )
        boton_nombre.pack(pady=8)

        #Aqui esta la llamada recursiva
        crear_avatares_recursivo(resto_avatares)

    #la otra llamada recursiva
    crear_avatares_recursivo(avatares)

    etiqueta_confirmacion = tk.Label(
        ventana_avatar,
        text="",
        font=("Impact", 13),
        bg="#2c3e50",
        fg="white"
    )
    etiqueta_confirmacion.pack(pady=10)

    boton_salir = tk.Button(
        ventana_avatar,
        text="SALIR",
        font=("Impact", 12),
        bg="#DAA520",
        width=10,
        height=1,
        command=ventana_avatar.destroy
    )
    boton_salir.place(x=20, y=490)


###########################################################################
####                     VENTANA ABOUT                                 ####
###########################################################################

def abrir_about():
    ventana_about = tk.Toplevel(ventana_inicial)
    ventana_about.title("Acerca de Epic Adventure")
    ventana_about.geometry("600x500+350+150")
    ventana_about.resizable(False, False)
    ventana_about.configure(bg="#2c3e50")

    ventana_about.transient(ventana_inicial)
    ventana_about.grab_set()
    
    titulo_about = tk.Label(
        ventana_about,
        text="ACERCA DEL JUEGO",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )
    titulo_about.pack(pady=30)
    
    texto_info = """EPIC ADVENTURE es un juego de aventuras
epicas donde eres un guardian de personajes de peliculas animadas y 
tendras que luchar contra los hollows, para rescatarlos, una ves hayas 
derrotado a un enemigo,el personaje pasara a ser parte de tu equipo para 
ayudarte en tu aventura y rescatar a los demas.

Caracteristicas:
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
    
    boton_salir = tk.Button(
        ventana_about,
        text="SALIR",
        font=("Impact", 12),
        bg="#DAA520",
        width=10,
        height=1,
        command=ventana_about.destroy
    )
    boton_salir.place(x=20, y=450)


###########################################################################
####               Botones de la ventana principal                     ####
###########################################################################

boton1 = tk.Button(
    ventana_inicial, 
    text="Personajes", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_pesonajes
)
boton1.place(relx=0.5, y=320, anchor="center")

boton2 = tk.Button(
    ventana_inicial, 
    text="Avatar", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_avatar
)
boton2.place(relx=0.5, y=370, anchor="center")

boton3 = tk.Button(
    ventana_inicial, 
    text="Iniciar", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton3.place(relx=0.5, y=420, anchor="center")

boton4 = tk.Button(
    ventana_inicial, 
    text="About", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_about
)
boton4.place(relx=0.5, y=470, anchor="center")

ventana_inicial.mainloop()