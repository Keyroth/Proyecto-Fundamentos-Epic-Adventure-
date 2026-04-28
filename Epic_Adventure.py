import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os


# aqui guardo los datos del jugador
datos_jugador = {
    "nombre": "",
    "avatar": "",
    "personajes": []
}

###########################################################################
# Cargo los personajes desde el archivo personajes.txt                    #
# Cada linea del formato: NOMBRE,rol,ataque,defensa,vida,archivo_imagen   #
###########################################################################

def cargar_personajes():
    personajes_stats = {}
    ruta_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "personajes.txt")

    with open(ruta_txt, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            partes      = linea.split(",")
            nombre      = partes[0]
            rol         = partes[1]
            ataque      = int(partes[2])
            defensa     = int(partes[3])
            vida        = int(partes[4])
            archivo_img = partes[5]

            personajes_stats[nombre] = {
                "rol":     rol,
                "ataque":  ataque,
                "defensa": defensa,
                "vida":    vida,
                "archivo": archivo_img
            }

    return personajes_stats

personajes_stats = cargar_personajes()

###########################################################################
####Aqui creo la ventana inicial donde se controlara el inicio del juego###
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

# aqui simplemente convierto lo que entra en el entry y lo hago en mayuscula
# y ademas actualizo el borde del entry segun si tiene contenido o no
def convertir_mayusculas(*args):
    texto = nombre_jugador.get()
    if texto != texto.upper():
        nombre_jugador.set(texto.upper())
    datos_jugador["nombre"] = nombre_jugador.get()

    if nombre_jugador.get().strip() != "":
        caja_nombre.config(highlightthickness=2, highlightbackground="#27ae60")
    else:
        caja_nombre.config(highlightthickness=2, highlightbackground="#555555")

nombre_jugador.trace_add('write', convertir_mayusculas)

caja_nombre = tk.Entry(
    ventana_inicial,
    width=35,
    font=("Arial", 14),
    justify="center",
    textvariable=nombre_jugador,
    highlightthickness=2,
    highlightbackground="#555555"
)
caja_nombre.place(relx=0.5, y=228, anchor="center", width=300)

###########################################################################
# Frames con borde de color para los botones de Personajes y Avatar       #
# El borde empieza gris, se pone rojo si falta, verde si ya acepto        #
###########################################################################

frame_boton_personajes = tk.Frame(
    ventana_inicial,
    bg="#555555",
    padx=3,
    pady=3
)
frame_boton_personajes.place(relx=0.5, y=320, anchor="center")

frame_boton_avatar = tk.Frame(
    ventana_inicial,
    bg="#555555",
    padx=3,
    pady=3
)
frame_boton_avatar.place(relx=0.5, y=370, anchor="center")

###########################################################################
# Actualiza el color de los bordes segun el estado actual de seleccion    #
###########################################################################

def actualizar_bordes():
    if len(datos_jugador["personajes"]) == 3:
        frame_boton_personajes.config(bg="#27ae60")
    else:
        frame_boton_personajes.config(bg="#555555")

    if datos_jugador["avatar"] != "":
        frame_boton_avatar.config(bg="#27ae60")
    else:
        frame_boton_avatar.config(bg="#555555")

    if nombre_jugador.get().strip() != "":
        caja_nombre.config(highlightbackground="#27ae60")
    else:
        caja_nombre.config(highlightbackground="#555555")


###########################################################################
####              VENTANA DE SELECCION DE PERSONAJES                   ####
###########################################################################

def abrir_pesonajes():

    # Guardo una copia temporal de lo que ya habia seleccionado
    # para poder cancelar sin perder nada
    seleccionados_temporal = list(datos_jugador["personajes"])

    ventana_personajes = tk.Toplevel(ventana_inicial)
    ventana_personajes.title("Seleccion de personajes")
    ventana_personajes.geometry("850x600+200+50")
    ventana_personajes.resizable(False, False)
    ventana_personajes.configure(bg="#2c3e50")

    ventana_personajes.transient(ventana_inicial)
    ventana_personajes.grab_set()

    titulo_personajes = tk.Label(
        ventana_personajes,
        text="Selecciona Tres Personajes",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )
    titulo_personajes.pack(pady=15)

    etiqueta_conteo = tk.Label(
        ventana_personajes,
        text="Personajes elegidos: " + str(len(seleccionados_temporal)) + " / 3",
        font=("Impact", 14),
        bg="#2c3e50",
        fg="white"
    )
    etiqueta_conteo.pack(pady=5)

    frame_contenedor = tk.Frame(ventana_personajes, bg="#2c3e50")
    frame_contenedor.pack(fill="both", expand=True, padx=10)

    scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    canvas = tk.Canvas(
        frame_contenedor,
        bg="#2c3e50",
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=canvas.yview)

    frame_cuadricula = tk.Frame(canvas, bg="#2c3e50")

    canvas.create_window(
        (0, 0),
        window=frame_cuadricula,
        anchor="nw"
    )

    def actualizar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_cuadricula.bind("<Configure>", actualizar_scroll)

    def scroll_con_mouse(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<MouseWheel>", scroll_con_mouse)

    # Lista construida desde el txt
    personajes = [
        {"nombre": nombre, "archivo": datos["archivo"]}
        for nombre, datos in personajes_stats.items()
    ]

    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")

    referencias_imagenes = []
    referencias_oscuras  = []
    botones_personajes   = []

    # seleccionados_local es la seleccion de trabajo dentro de esta ventana
    seleccionados_local  = list(seleccionados_temporal)

    ###########################################################################
    # Oscurece los botones no seleccionados con recursividad en cola          #
    ###########################################################################

    def oscurecer_no_seleccionados(lista_botones, indice):
        if indice >= len(lista_botones):
            return
        nombre_boton = lista_botones[indice]["nombre"]
        if nombre_boton not in seleccionados_local:
            lista_botones[indice]["boton"].config(
                image=lista_botones[indice]["imagen_oscura"],
                state="disabled"
            )
        oscurecer_no_seleccionados(lista_botones, indice + 1)

    ###########################################################################
    # Reactiva los botones con recursividad                                   #
    ###########################################################################

    def reactivar_botones(lista_botones, indice):
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
    # NO guarda en datos_jugador todavia, solo trabaja en seleccionados_local #
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

    ###########################################################################
    # Recursividad en pila para crear los cuadros de personajes               #
    ###########################################################################

    def crear_personajes_recursivo(lista_personajes, indice):
        if indice >= len(lista_personajes):
            return

        personaje_actual = lista_personajes[indice]
        fila    = indice // 5
        columna = indice  % 5

        frame_celda = tk.Frame(frame_cuadricula, bg="#2c3e50")
        frame_celda.grid(row=fila, column=columna, padx=10, pady=5)

        etiqueta_nombre_personaje = tk.Label(
            frame_celda,
            text=personaje_actual["nombre"],
            font=("Impact", 10),
            bg="#2c3e50",
            fg="#DAA520",
            width=10
        )
        etiqueta_nombre_personaje.pack()

        try:
            imagen_original = Image.open(os.path.join(ruta_base, personaje_actual["archivo"]))
            imagen_original = imagen_original.resize((120, 130))
        except:
            imagen_original = Image.new("RGB", (120, 130), color="#555555")

        enhancer          = ImageEnhance.Brightness(imagen_original)
        imagen_oscura_pil = enhancer.enhance(0.3)

        imagen_normal_tk = ImageTk.PhotoImage(imagen_original)
        imagen_oscura_tk = ImageTk.PhotoImage(imagen_oscura_pil)

        referencias_imagenes.append(imagen_normal_tk)
        referencias_oscuras.append(imagen_oscura_tk)

        # Si el personaje ya estaba en la seleccion anterior lo muestra resaltado
        relief_inicial = "solid" if personaje_actual["nombre"] in seleccionados_local else "raised"
        bd_inicial     = 4       if personaje_actual["nombre"] in seleccionados_local else 2

        boton = tk.Button(
            frame_celda,
            image=imagen_normal_tk,
            bg="#2c3e50",
            relief=relief_inicial,
            bd=bd_inicial,
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

        crear_personajes_recursivo(lista_personajes, indice + 1)

    crear_personajes_recursivo(personajes, 0)

    # Si ya tenia 3 seleccionados al abrir, oscurece los demas
    if len(seleccionados_local) == 3:
        oscurecer_no_seleccionados(botones_personajes, 0)

    ###########################################################################
    # Boton ACEPTAR: guarda la seleccion en datos_jugador y cierra            #
    ###########################################################################

    def aceptar_personajes():
        if len(seleccionados_local) != 3:
            ventana_aviso = tk.Toplevel(ventana_personajes)
            ventana_aviso.title("Seleccion incompleta")
            ventana_aviso.geometry("380x160+280+220")
            ventana_aviso.resizable(False, False)
            ventana_aviso.configure(bg="#2c3e50")
            ventana_aviso.transient(ventana_personajes)
            ventana_aviso.grab_set()

            tk.Label(
                ventana_aviso,
                text="Debes elegir exactamente 3 personajes.",
                font=("Arial", 12),
                bg="#2c3e50",
                fg="white",
                wraplength=320,
                justify="center"
            ).pack(pady=25)

            tk.Button(
                ventana_aviso,
                text="ENTENDIDO",
                font=("Impact", 12),
                bg="#DAA520",
                width=12,
                command=ventana_aviso.destroy
            ).pack()

            return

        # Si tiene exactamente 3 guarda y cierra
        datos_jugador["personajes"] = list(seleccionados_local)
        actualizar_bordes()
        ventana_personajes.destroy()

    ###########################################################################
    # Boton SALIR: descarta cambios y regresa sin guardar nada                #
    ###########################################################################

    def salir_sin_guardar():
        # No toca datos_jugador, simplemente cierra
        ventana_personajes.destroy()

    # Frame que contiene los dos botones juntos en la parte inferior
    frame_botones_inferior = tk.Frame(ventana_personajes, bg="#2c3e50")
    frame_botones_inferior.pack(pady=10)

    boton_salir = tk.Button(
        frame_botones_inferior,
        text="SALIR",
        font=("Impact", 12),
        bg="#c0392b",
        fg="white",
        width=10,
        height=1,
        command=salir_sin_guardar
    )
    boton_salir.pack(side="left", padx=10)

    boton_aceptar = tk.Button(
        frame_botones_inferior,
        text="ACEPTAR",
        font=("Impact", 12),
        bg="#27ae60",
        fg="white",
        width=10,
        height=1,
        command=aceptar_personajes
    )
    boton_aceptar.pack(side="left", padx=10)


###########################################################################
####              VENTANA DE SELECCION DE AVATAR                       ####
###########################################################################

def abrir_avatar():

    # Guardo el avatar actual para poder cancelar sin perder nada
    avatar_temporal = datos_jugador["avatar"]

    # Variable local de trabajo, no toca datos_jugador hasta que se acepte
    avatar_seleccionado_local = tk.StringVar()
    avatar_seleccionado_local.set(avatar_temporal)

    def seleccionar_avatar(nombre):
        avatar_seleccionado_local.set(nombre)
        etiqueta_confirmacion.config(text="Avatar seleccionado: " + nombre)

    ventana_avatar = tk.Toplevel(ventana_inicial)
    ventana_avatar.title("Seleccion de Avatar")
    ventana_avatar.geometry("700x550+300+100")
    ventana_avatar.resizable(False, False)
    ventana_avatar.configure(bg="#2c3e50")

    ventana_avatar.transient(ventana_inicial)
    ventana_avatar.grab_set()

    titulo_avatar = tk.Label(
        ventana_avatar,
        text="SELECCIONA TU AVATAR",
        font=("Impact", 24, "bold"),
        bg="#2c3e50",
        fg="#DAA520"
    )
    titulo_avatar.pack(pady=20)

    frame_avatares = tk.Frame(ventana_avatar, bg="#2c3e50")
    frame_avatares.pack(pady=10)

    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")

    avatares = [
        {"nombre": "BATMAN",  "archivo": "Avatar_Batman_frente.png"},
        {"nombre": "KRATOS",  "archivo": "Avatar_Kratos_Frente.png"},
        {"nombre": "NEITIRY", "archivo": "Avatar_Neitiry_frente.png"}
    ]

    referencias_imagenes = []

    def crear_avatares_recursivo(lista_avatares):
        if len(lista_avatares) == 0:
            return

        avatar_actual  = lista_avatares[0]
        resto_avatares = lista_avatares[1:]

        frame_individual = tk.Frame(frame_avatares, bg="#2c3e50")
        frame_individual.pack(side="left", padx=20)

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

        crear_avatares_recursivo(resto_avatares)

    crear_avatares_recursivo(avatares)

    # Muestra el avatar ya seleccionado si habia uno antes
    texto_confirmacion = ""
    if avatar_temporal != "":
        texto_confirmacion = "Avatar seleccionado: " + avatar_temporal

    etiqueta_confirmacion = tk.Label(
        ventana_avatar,
        text=texto_confirmacion,
        font=("Impact", 13),
        bg="#2c3e50",
        fg="white"
    )
    etiqueta_confirmacion.pack(pady=10)

    ###########################################################################
    # Boton ACEPTAR: guarda el avatar en datos_jugador y cierra               #
    ###########################################################################

    def aceptar_avatar():
        if avatar_seleccionado_local.get() == "":
            ventana_aviso = tk.Toplevel(ventana_avatar)
            ventana_aviso.title("Sin avatar")
            ventana_aviso.geometry("360x160+320+230")
            ventana_aviso.resizable(False, False)
            ventana_aviso.configure(bg="#2c3e50")
            ventana_aviso.transient(ventana_avatar)
            ventana_aviso.grab_set()

            tk.Label(
                ventana_aviso,
                text="Debes seleccionar un avatar antes de aceptar.",
                font=("Arial", 12),
                bg="#2c3e50",
                fg="white",
                wraplength=300,
                justify="center"
            ).pack(pady=25)

            tk.Button(
                ventana_aviso,
                text="ENTENDIDO",
                font=("Impact", 12),
                bg="#DAA520",
                width=12,
                command=ventana_aviso.destroy
            ).pack()

            return

        # Si tiene avatar seleccionado guarda y cierra
        datos_jugador["avatar"] = avatar_seleccionado_local.get()
        actualizar_bordes()
        ventana_avatar.destroy()

    ###########################################################################
    # Boton SALIR: descarta cambios y regresa sin guardar nada                #
    ###########################################################################

    def salir_sin_guardar():
        # No toca datos_jugador, simplemente cierra
        ventana_avatar.destroy()

    # Frame que contiene los dos botones juntos en la parte inferior
    frame_botones_inferior = tk.Frame(ventana_avatar, bg="#2c3e50")
    frame_botones_inferior.pack(pady=5)

    boton_salir = tk.Button(
        frame_botones_inferior,
        text="SALIR",
        font=("Impact", 12),
        bg="#c0392b",
        fg="white",
        width=10,
        height=1,
        command=salir_sin_guardar
    )
    boton_salir.pack(side="left", padx=10)

    boton_aceptar = tk.Button(
        frame_botones_inferior,
        text="ACEPTAR",
        font=("Impact", 12),
        bg="#27ae60",
        fg="white",
        width=10,
        height=1,
        command=aceptar_avatar
    )
    boton_aceptar.pack(side="left", padx=10)


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
derrotado a un enemigo, el personaje pasara a ser parte de tu equipo para 
ayudarte en tu aventura y rescatar a los demas.

Caracteristicas:
- Elige tres personajes iniciales
- Escoge tu avatar
- Explora los 5 mundos
- Enfrenta a los hollows en epicas batallas


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
####          VALIDACION AL PRESIONAR INICIAR                          ####
###########################################################################

def validar_e_iniciar():

    errores = []

    # Verifico el nombre
    if datos_jugador["nombre"].strip() == "":
        errores.append("- Debes ingresar tu nombre.")
        caja_nombre.config(highlightthickness=2, highlightbackground="#e74c3c")
    else:
        caja_nombre.config(highlightthickness=2, highlightbackground="#27ae60")

    # Verifico los personajes
    if len(datos_jugador["personajes"]) < 3:
        errores.append("- Debes seleccionar exactamente 3 personajes.")
        frame_boton_personajes.config(bg="#e74c3c")
    else:
        frame_boton_personajes.config(bg="#27ae60")

    # Verifico el avatar
    if datos_jugador["avatar"] == "":
        errores.append("- Debes seleccionar un avatar.")
        frame_boton_avatar.config(bg="#e74c3c")
    else:
        frame_boton_avatar.config(bg="#27ae60")

    # Si hay errores muestro la ventana con los mensajes
    if len(errores) > 0:
        ventana_error = tk.Toplevel(ventana_inicial)
        ventana_error.title("Campos incompletos")
        ventana_error.geometry("420x220+300+200")
        ventana_error.resizable(False, False)
        ventana_error.configure(bg="#2c3e50")
        ventana_error.transient(ventana_inicial)
        ventana_error.grab_set()

        tk.Label(
            ventana_error,
            text="No puedes iniciar aun:",
            font=("Impact", 16, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        ).pack(pady=15)

        tk.Label(
            ventana_error,
            text="\n".join(errores),
            font=("Arial", 12),
            bg="#2c3e50",
            fg="white",
            justify="left"
        ).pack(pady=5, padx=20)

        tk.Button(
            ventana_error,
            text="ENTENDIDO",
            font=("Impact", 12),
            bg="#DAA520",
            width=12,
            command=ventana_error.destroy
        ).pack(pady=15)

        return

    # Si todo esta bien, aqui se navega al mapa (se implementa en Fase 3)
    print("Todo listo. Jugador:", datos_jugador)


###########################################################################
####               Botones de la ventana principal                     ####
###########################################################################

boton1 = tk.Button(
    frame_boton_personajes,
    text="Personajes",
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_pesonajes
)
boton1.pack()

boton2 = tk.Button(
    frame_boton_avatar,
    text="Avatar",
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=abrir_avatar
)
boton2.pack()

boton3 = tk.Button(
    ventana_inicial,
    text="Iniciar",
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1,
    command=validar_e_iniciar
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