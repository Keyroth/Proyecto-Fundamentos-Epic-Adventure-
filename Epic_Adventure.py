import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import os
import random
import threading
import winsound
import time

musica_activa = False
hilo_musica = None

def reproducir_musica(archivo_musica, contador=0):

    global musica_activa
    
    if not musica_activa:
        return
    
    try:
        #reproduce sonidos                  #Nombre de archivo   # "|"es el operador or bit a bit   
        winsound.PlaySound(archivo_musica, winsound.SND_FILENAME | winsound.SND_ASYNC)#esto hace que el codigo siga ejecutandose mientras suena 
        
        #esta funcion espera sin usar while o for
        def espera_musica(segundos_restantes):
            #la musica se detuvo o ya no queda tiempo 
            if not musica_activa or segundos_restantes <= 0:
                return #caso base 
            time.sleep(0.1)  #esta es la pausa inmediata del hilo para que no consuma CPU
            espera_musica(segundos_restantes - 0.1) #esta es la parte recursiva, y se seguira llamando hasta que se acabe el tiempo o se detenga la musica
    
        espera_musica(600.0)#los 600 segundos es el tiempo asumido de la cancion
        
        #esto genera otro hilo 
        threading.Thread(
            target=reproducir_musica,#esta es la funcion que se ejecutara en el nuevo hilo y la misma funcion 
            args=(archivo_musica, contador + 1),#el mismo archivo pero incrementa el contador en 1
            daemon=True #aqui se cerrara automaticamente cuando el programa principal acabe 
        ).start()#inicia la ejecucion del hilo esta es la llamada recursiva principal 
        
    except Exception:
        pass #si hubiese un error solo lo ignora y ya 

def iniciar_musica():
    global musica_activa, hilo_musica
    
    if not musica_activa:
        musica_activa = True#aqui enciende la musica 
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        archivo_musica = os.path.join(ruta_actual, "Musica_fondo.wav")
        #lo qeu hace es buscar y abrir la ruta de la musica 

        hilo_musica = threading.Thread(
            target=reproducir_musica,
            args=(archivo_musica, 0),
            daemon=True
        )
        hilo_musica.start()

def detener_musica():
    global musica_activa #permite modificar la variable del inicio
    musica_activa = False #aqui la apaga 
    winsound.PlaySound(None, winsound.SND_PURGE)#detiene todos los sonidos actuales


######################################
#  DATOS GLOBALES
#######################################
#esto van a ser variables tipo diccionario

datos_jugador = {
    "nombre":    "",
    "avatar":    "",
    "personajes": []#esta es lista porque se tienen que agregar 3 personajes
}#eesto es vacio porque al seleccionarlo va a sumarlo aca

personajes_ganados = []#despues de ganar unas batallas aqui se va a agregar el personaje ganado
personajes_usados_por_hollow = [] #aqui es donde se lleva el contro de que personajes utiliza el hollow para que no se repita de nuevo

puntaje_global = {
    "jugador": 0,#esta es la puntuacion del jugador 
    "hollow":  0#y esta es la del hollow
}

#los numeros son los numeros de los mundos, mas que todo para llevar un orden 
#y esta en false, porque todos tienen que estar sin derrotar al inicio
#cuando el valor este en true significa que ay fue vencido, entonces con esto controlo que el jugador solo pueda
#seguir los mundos si vencio el anterior 
mundos_vencidos = {1: False, 2: False, 3: False, 4: False, 5: False}

#aqui las posiciones del final son de los botones que tiene cada mapa 
MUNDOS = [
    {"numero": 1, "nombre": "Selva",     "fondo": "SELVA.png",      "hollow_img": "Hollow1-2.png", "x": 133, "y": 279},
    {"numero": 2, "nombre": "Zootopia",  "fondo": "ZOOLOGIOCO.png", "hollow_img": "Hollow1-2.png", "x": 298, "y": 340},
    {"numero": 3, "nombre": "Arendelle", "fondo": "ARRENDELLE.png", "hollow_img": "Hollow3.png",   "x": 456, "y": 279},
    {"numero": 4, "nombre": "Castillo",  "fondo": "CASTILLO.png",   "hollow_img": "Hollow4.png",   "x": 619, "y": 340},
    {"numero": 5, "nombre": "Desierto",  "fondo": "DESIERTO.png",   "hollow_img": "Hollow5.png",   "x": 787, "y": 279},
]

#aqui estan los avatares y sus respectivvas imagenes 
AVATARES_ARCHIVOS = {
    "BATMAN":  "Avatar_Batman_frente.png",
    "KRATOS":  "Avatar_Kratos_Frente.png",
    "NEITIRY": "Avatar_Neitiry_frente.png"
}

#####################################
#  CARGA DE PERSONAJES DESDE TXT
######################################
def cargar_personajes():
    ruta   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "personajes.txt")
    lineas = open(ruta, "r", encoding="utf-8").read().splitlines()
                        #r:abre el archivo en modo lectura con decodificacion UTF
                        #.read lee todo el contenido del archivo como un string
                        #.splitlines() divide el string en una lista de lineas

    #esta funcion procesa cada linea del archivo hasta que la lista este vacia 
    def procesar(lista, acumulador):
        if not lista:
            return acumulador#cuando no queden lineas termina la recursion
        linea = lista[0].strip() #toma el primemr elemento de la lista y con.strip elimina espacios en blanco al inicio y final 
    
        if linea:#verifica que la linea no este vacia  las ignora si lo estan 
            #p es solo el nombre que le quise dar a la variable 
            p = linea.split(",") #divide la linea en una lista usando la coma como separador 
            #y todo esto que hago con p es decirle en la posicion que se encuentra cada valor que vamos a usar 
            acumulador[p[0]] = {
                "rol": p[1], "ataque": int(p[2]),
                "defensa": int(p[3]), "vida": int(p[4]),
                "archivo": p[5]
            }
        return procesar(lista[1:], acumulador)# elimina el primer valor de la lista y pasa el diccionario acumulado 

    return procesar(lineas, {}) #{}es igual al dirrionario vacio

personajes_stats = cargar_personajes() #y esto es una variable global donde se almacenan los personajes 



######################################
#  "AYUDANTES" RECURSIVOS
######################################

"""aqui filtro para seleccionar hollows, buscar personajes vivos del jugador
osea los personajes que tienen vida  mayor a cero, y se usa para saber si quedan personajes
para pelear contra el hollow, y saber si a el lequedan personajes 
tambien la uso para buscar personajes elegibles para cambiar 
"""
def filtrar(lista, condicion, acum=None):
    if acum is None:
        acum = []
    if not lista:
        return acum
    if condicion(lista[0]):
        acum.append(lista[0])
    return filtrar(lista[1:], condicion, acum)

"""es como para comprobar que todos los elementos de una lista cumplan la condicion 
y la uso en la funcion de fin de batalla dentro de abrir mundo, devuelve true or false 
y verifica si el jugador vencio todos los mundos """
def todos(lista, condicion):
    if not lista:
        return True
    if not condicion(lista[0]):
        return False
    return todos(lista[1:], condicion)

"""busca el primer elemento que cumple una condicion y devuelve su posicion en la lista 
la uso en la funcion abrir mundo en la batalla, y encuentra el proximo personaje vivo del jugador
para que cuando el anterior muera, se cambie a este,al igual que con el personaje del hollow"""
def buscar_indice(lista, condicion, indice=0):
    if not lista:
        return -1
    if condicion(lista[0]):
        return indice
    return buscar_indice(lista[1:], condicion, indice + 1)

######################################
#  VENTANA PRINCIPAL
######################################
ventana_inicial = tk.Tk()
ventana_inicial.title("EPIC ADVENTURE")
ventana_inicial.geometry("800x600+250+80")
ventana_inicial.resizable(False, False)
ventana_inicial.configure(bg="#2c3e50")

tk.Label(ventana_inicial, text="EPIC ADVENTURE", font=("Impact", 36, "bold"),
         bg="#2c3e50", fg="#DAA520").place(relx=0.5, y=80, anchor="center")

tk.Label(ventana_inicial, text="Ingrese Su Nombre", bg="#DAA520",
         font=("Impact", 18), highlightthickness=2,
         highlightbackground="black", padx=20, pady=10
         ).place(relx=0.5, y=180, anchor="center")

nombre_jugador = tk.StringVar()#esto solo hace que se vincule a widges

def convertir_mayusculas(*args): #(*args) recibe cualquier cantidad de elementos 
    t = nombre_jugador.get()#optiene el texto actual de la variable stringvar
    if t != t.upper():
        nombre_jugador.set(t.upper())#convierte todo el texto a mayusculas en tiempo real 
    datos_jugador["nombre"] = nombre_jugador.get()#toma el texto en mayusculas
    color = "#27ae60" if nombre_jugador.get().strip() else "#555555"
    caja_nombre.config(highlightthickness=2, highlightbackground=color) #aqui se le hace el borde verde cuando ya este el nombre del jugador y si no sera gris

            #trace add es cuando cambia la variable 
nombre_jugador.trace_add('write', convertir_mayusculas)#cuando se escrube cambia el valor

caja_nombre = tk.Entry(ventana_inicial, width=35, font=("Arial", 14),
                       justify="center", textvariable=nombre_jugador,
                       highlightthickness=2, highlightbackground="#555555")
caja_nombre.place(relx=0.5, y=228, anchor="center", width=300)

frame_boton_personajes = tk.Frame(ventana_inicial, bg="#555555", padx=3, pady=3)
frame_boton_personajes.place(relx=0.5, y=320, anchor="center")

frame_boton_avatar = tk.Frame(ventana_inicial, bg="#555555", padx=3, pady=3)
frame_boton_avatar.place(relx=0.5, y=370, anchor="center")

""""aqui es odnde se actualiza el borde si falta algo"""
def actualizar_bordes():
    frame_boton_personajes.config(bg="#27ae60" if len(datos_jugador["personajes"]) == 3 else "#555555")
    frame_boton_avatar.config(bg="#27ae60" if datos_jugador["avatar"] else "#555555")
    caja_nombre.config(highlightbackground="#27ae60" if nombre_jugador.get().strip() else "#555555")

######################################
#  SELECCION DE PERSONAJES
######################################
def abrir_pesonajes():
    v = tk.Toplevel(ventana_inicial)
    v.title("Seleccion de personajes")
    v.geometry("850x600+200+50")
    v.resizable(False, False)
    v.configure(bg="#2c3e50")
    v.transient(ventana_inicial)
    v.grab_set()#aqui captura todos los elementos, mouse y teclado, y no se puede interactar con la ventana principal

    tk.Label(v, text="Selecciona Tres Personajes", font=("Impact", 24, "bold"),
             bg="#2c3e50", fg="#DAA520").pack(pady=15)

    etiqueta_conteo = tk.Label(v, text="Personajes elegidos: 0 / 3",
                                font=("Impact", 14), bg="#2c3e50", fg="white")
    etiqueta_conteo.pack(pady=5)

    #frame count es el que contiene el scroll para la lista de personajes
    frame_cont = tk.Frame(v, bg="#2c3e50")
    frame_cont.pack(fill="both", expand=True, padx=10)

    #sb solo es el nombre de la barra de scroll
    sb = tk.Scrollbar(frame_cont, orient="vertical")
    sb.pack(side="right", fill="y")

    canvas = tk.Canvas(frame_cont, bg="#2c3e50", highlightthickness=0, yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.config(command=canvas.yview) #que cuando se utilice el scroll el canvas se desplaza 

    #frame donde se pondran los personajes 
    frame_grid = tk.Frame(canvas, bg="#2c3e50")
    canvas.create_window((0, 0), window=frame_grid, anchor="nw")
    
    #esto ejecuta la funcion cada que frame cambia de tamaño por la cantidad de personajes
    frame_grid.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    #la lista de personaejes en un diccionario 
    personajes_lista = [{"nombre": n, "archivo": d["archivo"]} for n, d in personajes_stats.items()]
    ruta_base        = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")
   
    #crea los botones con las imagenes en la seleccion de personajes iniciales 
    refs_norm = []; refs_osc = []; botones = []

    #esto permite cancelar sin guardar cambiios 
    sel_temp  = list(datos_jugador["personajes"])

    """esta funcion soolo oscurese los que no estan seleccionados, decidi hacerlo asi porque en uno de mis 
    juegos favoritos implementan este metodo, para resaltar los seleccionados """
    def oscurecer(lista, i):
        if i >= len(lista): return

        if lista[i]["nombre"] not in sel_temp: #aqui dice que solo afecta a los personajes que no fueron seleccionados 
            lista[i]["boton"].config(image=lista[i]["img_osc"], state="disabled")
        oscurecer(lista, i + 1)

    def reactivar(lista, i):
        if i >= len(lista): return
        if lista[i]["nombre"] not in sel_temp: #esto afecta a personajes no seleccionados 
            lista[i]["boton"].config(image=lista[i]["img_norm"], state="normal") #aqui restaura la imagen normal, para poder hacer click
        reactivar(lista, i + 1)

    """aqui se seleccionan y se deseleccionan los personajes que se pueden usar al inicio y el idx es el 
    valor tipo entero que nos dice el indice del boton en la lista de botones"""
    def seleccionar(nombre, idx):
        if nombre in sel_temp:
            sel_temp.remove(nombre)
            #aqui vuelve al la imagen normal con efecto 3d yun borde de 2 pixeles
            botones[idx]["boton"].config(image=botones[idx]["img_norm"], relief="raised", bd=2)
            #esto actualiza el texto del contador, indicando en tiempo real 3,2,1 o 0 
            etiqueta_conteo.config(text="Personajes elegidos: " + str(len(sel_temp)) + " / 3")
            reactivar(botones, 0) #aqui se reactivan los botones, ya que al no ser 3 se puede seleccionar mas 
            return
        if len(sel_temp) >= 3: return #si ya hay tres seleccionados no se pueden seleccionar mas 
        sel_temp.append(nombre) #agrega el nombre a la lista de seleccion temporal 
        botones[idx]["boton"].config(relief="solid", bd=4) #esto solo les pone borde a los seleccionados
        #aca el contador aumenta si se seleccionan mas personajes 
        etiqueta_conteo.config(text="Personajes elegidos: " + str(len(sel_temp)) + " / 3")
        if len(sel_temp) == 3: #si son 3 seleccionados oscurece el resto de botones 
            oscurecer(botones, 0)

    def aceptar():
        if len(sel_temp) < 3: #hay menos de tres personajes seleccionados ? 
            #aqui te dice qeu tienes que seleccionar al menos 3 personajes para aceptar 
            #no te deja seleccionar menos de 3 
            av = tk.Toplevel(v); av.title("Incompleto")
            av.geometry("380x160+280+220"); av.resizable(False, False)
            av.configure(bg="#2c3e50"); av.transient(v); av.grab_set()
            tk.Label(av, text="Debes seleccionar exactamente 3 personajes.",
                     font=("Arial", 12), bg="#2c3e50", fg="white",
                     wraplength=320, justify="center").pack(pady=25, padx=20)
            tk.Button(av, text="ENTENDIDO", font=("Impact", 12), bg="#DAA520",
                      width=12, command=av.destroy).pack()
            return
        datos_jugador["personajes"] = list(sel_temp) #copia de seguridad temporal, guarda los datos globales
        actualizar_bordes() #aqui lllama la funcion de cambiar borde y lo pone en verde 
        v.destroy() #cierra la ventana 

    def crear(lista, i):
        if i >= len(lista): return
        p    = lista[i]
        fila = i // 5; col = i % 5 #divisioin entera para las filas y modulo de 5 para las columnas
        #frame contenedor para cada personaje 
        fc   = tk.Frame(frame_grid, bg="#2c3e50")
        #esto nos da la posicion en la cuadricula
        fc.grid(row=fila, column=col, padx=10, pady=5)
        tk.Label(fc, text=p["nombre"], font=("Impact", 10),
                 bg="#2c3e50", fg="#DAA520", width=10).pack()
        try:
            img = Image.open(os.path.join(ruta_base, p["archivo"])).resize((120, 130))
        except:
            img = Image.new("RGB", (120, 130), "#555555") #si hay un error en la imagen, crea una archivo gris de respaldo
    
        #reduse el brillo de la imagen un 30% haciendola ver oscura 
        img_osc  = ImageTk.PhotoImage(ImageEnhance.Brightness(img).enhance(0.3))
        img_norm = ImageTk.PhotoImage(img) #convierte la imagen normal a formato tkinter
        refs_norm.append(img_norm); refs_osc.append(img_osc) #guarda las referencias para que pyhton no las borrede la memoria
        rel = "solid" if p["nombre"] in sel_temp else "raised"
        bd  = 4       if p["nombre"] in sel_temp else 2
        btn = tk.Button(fc, image=img_norm, bg="#2c3e50", relief=rel, bd=bd, cursor="hand2",
                        command=lambda idx=i, n=p["nombre"]: seleccionar(n, idx))
        btn.pack() #coloca el boton dentro del frame
        botones.append({"nombre": p["nombre"], "boton": btn,
                        "img_norm": img_norm, "img_osc": img_osc})
        crear(lista, i + 1) #se llama recursivamente, por cada personaje

    crear(personajes_lista, 0) #comienza desde el personaje 0
    if len(sel_temp) == 3: oscurecer(botones, 0)
    #actualiza el contador con la seleccion actual
    etiqueta_conteo.config(text="Personajes elegidos: " + str(len(sel_temp)) + " / 3")
     
     #crea frame para los botones de salir y aceptar 
    fb = tk.Frame(v, bg="#2c3e50"); fb.pack(pady=10)
    tk.Button(fb, text="SALIR",   font=("Impact", 12), bg="#c0392b", fg="white",
              width=10, command=v.destroy).pack(side="left", padx=15)
    tk.Button(fb, text="ACEPTAR", font=("Impact", 12), bg="#27ae60", fg="white",
              width=10, command=aceptar).pack(side="left", padx=15)

######################################
#  SELECCION DE AVATAR
######################################
def abrir_avatar():
    av_temp = {"valor": datos_jugador["avatar"]}

    v = tk.Toplevel(ventana_inicial)
    v.title("Seleccion de Avatar"); v.geometry("700x550+300+100")
    v.resizable(False, False); v.configure(bg="#2c3e50")
    v.transient(ventana_inicial); v.grab_set()

    tk.Label(v, text="SELECCIONA TU AVATAR", font=("Impact", 24, "bold"),
             bg="#2c3e50", fg="#DAA520").pack(pady=20)

    frame_av  = tk.Frame(v, bg="#2c3e50"); frame_av.pack(pady=10)
    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")
    avatares  = [{"nombre": "BATMAN",  "archivo": "Avatar_Batman_frente.png"},
                 {"nombre": "KRATOS",  "archivo": "Avatar_Kratos_Frente.png"},
                 {"nombre": "NEITIRY", "archivo": "Avatar_Neitiry_frente.png"}]
    refs = []

    etiqueta_conf = tk.Label(v,
        text=("Avatar seleccionado: " + datos_jugador["avatar"]) if datos_jugador["avatar"] else "",
        font=("Impact", 13), bg="#2c3e50", fg="white")

    def sel_avatar(nombre):
        av_temp["valor"] = nombre
        etiqueta_conf.config(text="Avatar seleccionado: " + nombre)

    def crear_av(lista): #crea avatar
        if not lista: return
        a  = lista[0]
        fi = tk.Frame(frame_av, bg="#2c3e50"); fi.pack(side="left", padx=20)
        img = Image.open(os.path.join(ruta_base, a["archivo"])).resize((150, 180))
        itk = ImageTk.PhotoImage(img); refs.append(itk) #guarda la imagen en la lista de refs evita que python lo borre
        
        #guarda la imagen como atributo, asi python no la borra
        lbl = tk.Label(fi, image=itk, bg="#2c3e50"); lbl.pack(); lbl.image = itk
        tk.Button(fi, text=a["nombre"], font=("Impact", 13), bg="#DAA520",
                  fg="#2c3e50", width=10,
                  command=lambda n=a["nombre"]: sel_avatar(n)).pack(pady=8)
        crear_av(lista[1:])

    crear_av(avatares)
    etiqueta_conf.pack(pady=10)

    """aqui solo valida que si este seleccionado un avatar en la ventana de avatares, que no 
    pueda ocntinuar sin seleccionarlo"""
    def aceptar_av():
        if not av_temp["valor"]:
            av2 = tk.Toplevel(v); av2.title("Sin avatar")
            av2.geometry("380x160+280+220"); av2.resizable(False, False)
            av2.configure(bg="#2c3e50"); av2.transient(v); av2.grab_set()
            tk.Label(av2, text="Debes seleccionar un avatar antes de continuar.",
                     font=("Arial", 12), bg="#2c3e50", fg="white",
                     wraplength=320, justify="center").pack(pady=25, padx=20)
            tk.Button(av2, text="ENTENDIDO", font=("Impact", 12), bg="#DAA520",
                      width=12, command=av2.destroy).pack()
            return
        datos_jugador["avatar"] = av_temp["valor"]
        actualizar_bordes(); v.destroy()

    fb = tk.Frame(v, bg="#2c3e50"); fb.pack(pady=10)
    tk.Button(fb, text="SALIR",   font=("Impact", 12), bg="#c0392b", fg="white",
              width=10, command=v.destroy).pack(side="left", padx=15)
    tk.Button(fb, text="ACEPTAR", font=("Impact", 12), bg="#27ae60", fg="white",
              width=10, command=aceptar_av).pack(side="left", padx=15)

######################################
#  ABOUT
######################################
def abrir_about():
    v = tk.Toplevel(ventana_inicial); v.title("Acerca de Epic Adventure")
    v.geometry("600x500+350+150"); v.resizable(False, False)
    v.configure(bg="#2c3e50"); v.transient(ventana_inicial); v.grab_set()
    tk.Label(v, text="ACERCA DEL JUEGO", font=("Impact", 24, "bold"),
             bg="#2c3e50", fg="#DAA520").pack(pady=30)
    tk.Label(v, text="""EPIC ADVENTURE es un juego de aventuras epicas donde eres
un guardian de personajes de peliculas animadas y tendras que
luchar contra los hollows para rescatarlos.

Caracteristicas:
- Elige tres personajes iniciales
- Escoge tu avatar
- Explora los 5 mundos
- Enfrenta a los hollows en epicas batallas

BUENA SUERTE GUARDIAN""",
             font=("Arial", 12), bg="#2c3e50", fg="white", justify="left").pack(pady=20)
    tk.Button(v, text="SALIR", font=("Impact", 12), bg="#DAA520",
              width=10, command=v.destroy).place(x=20, y=450)

######################################
#  VALIDAR E INICIAR
######################################
def validar_e_iniciar():
    errores = [] #aqui guardare donde esta el error 
    if not datos_jugador["nombre"].strip():
        errores.append("- Debes ingresar tu nombre.")
        caja_nombre.config(highlightthickness=2, highlightbackground="#e74c3c")
    else:
        caja_nombre.config(highlightthickness=2, highlightbackground="#27ae60")

    if len(datos_jugador["personajes"]) < 3:
        errores.append("- Debes seleccionar exactamente 3 personajes.")
        frame_boton_personajes.config(bg="#e74c3c")
    else:
        frame_boton_personajes.config(bg="#27ae60")

    if not datos_jugador["avatar"]:
        errores.append("- Debes seleccionar un avatar.")
        frame_boton_avatar.config(bg="#e74c3c")
    else:
        frame_boton_avatar.config(bg="#27ae60")

    if errores:
        ve = tk.Toplevel(ventana_inicial); ve.title("Campos incompletos")
        ve.geometry("420x220+300+200"); ve.resizable(False, False)
        ve.configure(bg="#2c3e50"); ve.transient(ventana_inicial); ve.grab_set()
        tk.Label(ve, text="No puedes iniciar aun:", font=("Impact", 16, "bold"),
                 bg="#2c3e50", fg="#e74c3c").pack(pady=15)
        tk.Label(ve, text="\n".join(errores), font=("Arial", 12),
                 bg="#2c3e50", fg="white", justify="left").pack(pady=5, padx=20)
        tk.Button(ve, text="ENTENDIDO", font=("Impact", 12), bg="#DAA520",
                  width=12, command=ve.destroy).pack(pady=15)
        return
 
    #si la validacion esta correcta en todo caso entonces ponga la musica he inicie el juego
    iniciar_musica()
    abrir_mapa()

######################################
#  MAPA
######################################
def abrir_mapa():
    vm = tk.Toplevel(ventana_inicial)
    vm.title("Mapa - Epic Adventure"); vm.geometry("900x530+100+60")
    vm.resizable(False, False); vm.configure(bg="#2c3e50")
    vm.transient(ventana_inicial); vm.grab_set()

    ruta_base   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")
    img_mapa    = Image.open(os.path.join(ruta_base, "Mapa.png")).resize((900, 450))
    img_mapa_tk = ImageTk.PhotoImage(img_mapa)

    try:
        img_x    = Image.open(os.path.join(ruta_base, "X.png")).resize((60, 60))
        img_x_tk = ImageTk.PhotoImage(img_x)
    except:
        img_x_tk = None

    canvas = tk.Canvas(vm, width=900, height=450, highlightthickness=0)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=img_mapa_tk)
    canvas.image    = img_mapa_tk
    canvas.img_x_tk = img_x_tk

    def refrescar_mapa(lista, i):
        if i >= len(lista): return
        m = lista[i]
        if mundos_vencidos[m["numero"]] and canvas.img_x_tk:
            canvas.create_image(m["x"], m["y"], anchor="center", image=canvas.img_x_tk)
        refrescar_mapa(lista, i + 1)

    def crear_botones(lista, i):
        if i >= len(lista): return
        m   = lista[i]
        num = m["numero"]
        if mundos_vencidos[num]:
            crear_botones(lista, i + 1); return
        disponible = (num == 1) or mundos_vencidos[num - 1]
        if disponible:
            btn = tk.Button(canvas, text=str(num), font=("Impact", 18, "bold"),
                            bg="#2c3e50", fg="white",
                            activebackground="#DAA520", activeforeground="#2c3e50",
                            bd=0, highlightthickness=0, cursor="hand2",
                            command=lambda md=m: abrir_mundo(md, vm, canvas, img_mapa_tk, MUNDOS))
        else:
            btn = tk.Button(canvas, text=str(num), font=("Impact", 18, "bold"),
                            bg="#555555", fg="#888888", bd=0,
                            highlightthickness=0, state="disabled")
        canvas.create_window(m["x"], m["y"], anchor="center", window=btn)
        crear_botones(lista, i + 1)

    refrescar_mapa(MUNDOS, 0)
    crear_botones(MUNDOS, 0)

    tk.Label(vm, text="Guardian: " + datos_jugador["nombre"] +
             "   |   Puntos: " + str(puntaje_global["jugador"]),
             font=("Impact", 14), bg="#2c3e50", fg="#DAA520").pack(pady=8)

######################################
#  PANTALLA DE VICTORIA FINAL Y ANIMACION
######################################
def abrir_victoria_final(ventana_victoria):
    vf = tk.Toplevel(ventana_victoria)
    vf.title("VICTORIA FINAL")
    vf.geometry("600x500+150+80")
    vf.resizable(False, False)
    vf.configure(bg="#0f0f23")
    vf.transient(ventana_victoria)
    vf.grab_set()

    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")

    tk.Label(vf, text="¡FELICIDADES!", font=("Impact", 36, "bold"),
             bg="#0f0f23", fg="#DAA520").pack(pady=20)

    tk.Label(vf, text="Has derrotado a todos los Hollows.\n¡Las historias han sido restauradas!",
             font=("Arial", 14), bg="#0f0f23", fg="white", justify="center").pack()

    tk.Label(vf, text="Puntaje final: " + str(puntaje_global["jugador"]) + " pts",
             font=("Impact", 20), bg="#0f0f23", fg="#27ae60").pack(pady=10)

    archivo_av = AVATARES_ARCHIVOS.get(datos_jugador["avatar"], "")
    try:
        img_av    = Image.open(os.path.join(ruta_base, archivo_av)).resize((120, 150))
        img_av_tk = ImageTk.PhotoImage(img_av)
    except:
        img_av_tk = ImageTk.PhotoImage(Image.new("RGB", (120, 150), "#DAA520"))

    canvas_av = tk.Canvas(vf, width=200, height=200, bg="#0f0f23", highlightthickness=0)
    canvas_av.pack()
    id_av = canvas_av.create_image(100, 100, anchor="center", image=img_av_tk)
    canvas_av.img_av_tk = img_av_tk

    salto_estado = {"subiendo": True, "y": 100}

    def animar_salto():
        if salto_estado["subiendo"]:
            salto_estado["y"] -= 8
            if salto_estado["y"] <= 60:
                salto_estado["subiendo"] = False
        else:
            salto_estado["y"] += 8
            if salto_estado["y"] >= 100:
                salto_estado["subiendo"] = True
        canvas_av.coords(id_av, 100, salto_estado["y"])
        vf.after(40, animar_salto)

    animar_salto()

    def cerrar_juego():
        detener_musica()
        vf.destroy()
        ventana_inicial.destroy()

    tk.Button(vf, text="TERMINAR", font=("Impact", 16), bg="#DAA520",
              fg="#2c3e50", width=14, command=cerrar_juego).pack(pady=15)

######################################
#  BATALLA
######################################
def abrir_mundo(mundo, ventana_mapa, canvas_mapa, img_mapa_tk, lista_mundos):

    ruta_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")

    def hacer_copia(nombre, duenio="jugador"): #crea una copia independiente de un personaje con sus estadisticas 

        s = personajes_stats[nombre]
        return {
            "nombre":   nombre,
            "ataque":   s["ataque"],
            "defensa":  s["defensa"],
            "vida":     s["vida"],
            "vida_max": s["vida"],
            "archivo":  s["archivo"],
            "duenio":   duenio
        }
    """aqui es donde se filtran todos los personajes del juego, quedandose solo con los que no estan seleccionados 
    en el inicio del juego, los que no han sido capturados y no han sido usados como enemigos antes"""
    pool = filtrar( 
        list(personajes_stats.keys()),
        lambda n: n not in datos_jugador["personajes"]
                  and n not in personajes_ganados
                  and n not in personajes_usados_por_hollow
    )
    random.shuffle(pool) #mezcla la lista anterior
    nombres_hollow = pool[:3] #aqui selecciona los primeros 3 personajes, que seran los enemigos de esa batalla 

    def registrar_usados(lista):
        if not lista: return
        if lista[0] not in personajes_usados_por_hollow:
            personajes_usados_por_hollow.append(lista[0])
        registrar_usados(lista[1:])

    registrar_usados(nombres_hollow)

    equipo_hollow = [hacer_copia(n, "hollow") for n in nombres_hollow]

    nombres_jugador = list(datos_jugador["personajes"]) + list(personajes_ganados) #combian los personajes ganados con los 3 iniciales 
    equipo_jugador  = [hacer_copia(n, "jugador") for n in nombres_jugador]

    estado = {
        "idx_jugador":       0,
        "idx_hollow":        0,
        "turno":             "jugador",
        "batalla_terminada": False,
        "pts_batalla_j":     0,
        "pts_batalla_h":     0
    }
 
    #aqui se crea la ventana de batalla 
    vm = tk.Toplevel(ventana_mapa)
    vm.title("Mundo " + str(mundo["numero"]) + " - " + mundo["nombre"])
    vm.geometry("900x620+50+30")
    vm.resizable(False, False)
    vm.configure(bg="#1a1a2e")
    vm.transient(ventana_mapa)
    vm.grab_set()

    try:
        img_fondo    = Image.open(os.path.join(ruta_base, mundo["fondo"])).resize((900, 400))
        img_fondo_tk = ImageTk.PhotoImage(img_fondo)
    except:
        img_fondo_tk = None

    canvas_batalla = tk.Canvas(vm, width=900, height=400, highlightthickness=0, bg="#1a1a2e")
    canvas_batalla.pack()
    if img_fondo_tk:
        canvas_batalla.create_image(0, 0, anchor="nw", image=img_fondo_tk)
        canvas_batalla.img_fondo_tk = img_fondo_tk

    def cargar_img(archivo, tam):
        try:
            return ImageTk.PhotoImage(
                Image.open(os.path.join(ruta_base, archivo)).resize(tam))
        except:
            return ImageTk.PhotoImage(Image.new("RGB", tam, "#555555"))

    img_hollow_tk = cargar_img(mundo["hollow_img"], (120, 160))
    img_avatar_tk = cargar_img(AVATARES_ARCHIVOS.get(datos_jugador["avatar"], ""), (90, 130))

    cache_imgs = {}
    def get_img(nombre):
        if nombre not in cache_imgs:
            cache_imgs[nombre] = cargar_img(personajes_stats[nombre]["archivo"], (110, 140))
        return cache_imgs[nombre]

    POS = {
        "hollow":       (80,  290),
        "pers_hollow":  (220, 290),
        "pers_jugador": (640, 290),
        "avatar":       (800, 290),
    }

    def inicializar_ids_recursivo(lista_claves, indice=0, ids=None):
        if ids is None:
            ids = {}
        if indice >= len(lista_claves):
            return ids
        ids[lista_claves[indice]] = None
        return inicializar_ids_recursivo(lista_claves, indice + 1, ids)
    
    lista_imagenes = [
        "hollow_img", "pers_hollow_img", "pers_jug_img", "avatar_img",
        "barra_bg_h", "barra_hv_h", "txt_vida_h",
        "barra_bg_j", "barra_hv_j", "txt_vida_j"
    ]
    
    ids = inicializar_ids_recursivo(lista_imagenes)

    panel = tk.Frame(vm, bg="#0f0f23", height=220)
    panel.pack(fill="x")

    frame_pts = tk.Frame(panel, bg="#0f0f23")
    frame_pts.pack(fill="x", padx=20, pady=5)

    lbl_puntaje_h = tk.Label(frame_pts,
                              text="Hollow: " + str(puntaje_global["hollow"]) + " pts",
                              font=("Impact", 12), bg="#0f0f23", fg="#e74c3c")
    lbl_puntaje_h.pack(side="left")

    lbl_puntaje_j = tk.Label(frame_pts,
                              text="Guardian: " + str(puntaje_global["jugador"]) + " pts",
                              font=("Impact", 12), bg="#0f0f23", fg="#DAA520")
    lbl_puntaje_j.pack(side="right")

    log_texto = tk.Text(panel, height=4, font=("Arial", 10),
                        bg="#0a0a1a", fg="white", state="disabled",
                        wrap="word", relief="flat")
    log_texto.pack(fill="x", padx=20)

    def log(msg):
        log_texto.config(state="normal")
        log_texto.insert("end", msg + "\n")
        log_texto.see("end")
        log_texto.config(state="disabled")

    frame_botones = tk.Frame(panel, bg="#0f0f23")
    frame_botones.pack(pady=8)

    btn_atacar = tk.Button(frame_botones, text="ATACAR", font=("Impact", 16),
                           bg="#c0392b", fg="white", width=14, height=1)
    btn_atacar.pack(side="left", padx=20)

    btn_elegir = tk.Button(frame_botones, text="ELEGIR", font=("Impact", 16),
                           bg="#2980b9", fg="white", width=14, height=1)
    btn_elegir.pack(side="left", padx=20)

    def dibujar_escena():
        if ids["hollow_img"]:  canvas_batalla.delete(ids["hollow_img"])
        if ids["avatar_img"]:  canvas_batalla.delete(ids["avatar_img"])
        ids["hollow_img"] = canvas_batalla.create_image(
            POS["hollow"][0], POS["hollow"][1], anchor="center", image=img_hollow_tk)
        ids["avatar_img"] = canvas_batalla.create_image(
            POS["avatar"][0], POS["avatar"][1], anchor="center", image=img_avatar_tk)
        canvas_batalla.img_hollow_tk = img_hollow_tk
        canvas_batalla.img_avatar_tk = img_avatar_tk

        p_h    = equipo_hollow[estado["idx_hollow"]]
        img_ph = get_img(p_h["nombre"])
        if ids["pers_hollow_img"]: canvas_batalla.delete(ids["pers_hollow_img"])
        ids["pers_hollow_img"] = canvas_batalla.create_image(
            POS["pers_hollow"][0], POS["pers_hollow"][1], anchor="center", image=img_ph)

        p_j    = equipo_jugador[estado["idx_jugador"]]
        img_pj = get_img(p_j["nombre"])
        if ids["pers_jug_img"]: canvas_batalla.delete(ids["pers_jug_img"])
        ids["pers_jug_img"] = canvas_batalla.create_image(
            POS["pers_jugador"][0], POS["pers_jugador"][1], anchor="center", image=img_pj)

        dibujar_barras()

    def limpiar_ids_barras(claves, i=0):
        if i >= len(claves): return
        if ids[claves[i]]:
            canvas_batalla.delete(ids[claves[i]])
            ids[claves[i]] = None
        limpiar_ids_barras(claves, i + 1)

    def dibujar_barras():
        AW = 130; AH = 14 #aqui esta el tamaño fijo de la barra de vida 
        p_h   = equipo_hollow[estado["idx_hollow"]]
        cx_h  = POS["pers_hollow"][0]; cy_h = POS["pers_hollow"][1] - 85 #posicion de la barra del personaje del hollow
        #porsentaje de calculo de la vida del personaje del hollow 
        pct_h = max(0, p_h["vida"] / p_h["vida_max"])
        col_h = "#27ae60" if pct_h > 0.5 else "#e67e22" if pct_h > 0.25 else "#e74c3c"
        #aqui limpio las barras interiores 
        limpiar_ids_barras(["barra_bg_h", "barra_hv_h", "txt_vida_h"])
        ids["barra_bg_h"] = canvas_batalla.create_rectangle(
            cx_h-AW//2, cy_h, cx_h+AW//2, cy_h+AH, fill="#333333", outline="")
        #aqui le doy color segun el posentaje 
        ids["barra_hv_h"] = canvas_batalla.create_rectangle(
            cx_h-AW//2, cy_h, cx_h-AW//2+int(AW*pct_h), cy_h+AH, fill=col_h, outline="")
       #dibuja el texto de vida
        ids["txt_vida_h"] = canvas_batalla.create_text(
            cx_h, cy_h+AH+6,
            text=p_h["nombre"] + "  " + str(max(0, p_h["vida"])) + "/" + str(p_h["vida_max"]),
            fill="white", font=("Arial", 9, "bold"))

        p_j   = equipo_jugador[estado["idx_jugador"]]
        cx_j  = POS["pers_jugador"][0]; cy_j = POS["pers_jugador"][1] - 85
        pct_j = max(0, p_j["vida"] / p_j["vida_max"])
        col_j = "#27ae60" if pct_j > 0.5 else "#e67e22" if pct_j > 0.25 else "#e74c3c"
        limpiar_ids_barras(["barra_bg_j", "barra_hv_j", "txt_vida_j"])
        ids["barra_bg_j"] = canvas_batalla.create_rectangle(
            cx_j-AW//2, cy_j, cx_j+AW//2, cy_j+AH, fill="#333333", outline="")
        ids["barra_hv_j"] = canvas_batalla.create_rectangle(
            cx_j-AW//2, cy_j, cx_j-AW//2+int(AW*pct_j), cy_j+AH, fill=col_j, outline="")
        ids["txt_vida_j"] = canvas_batalla.create_text(
            cx_j, cy_j+AH+6,
            text=p_j["nombre"] + "  " + str(max(0, p_j["vida"])) + "/" + str(p_j["vida_max"]),
            fill="white", font=("Arial", 9, "bold"))

    def animar_ataque(atacante, callback):
        key      = "pers_jug_img"     if atacante == "jugador" else "pers_hollow_img"
        pos_orig = POS["pers_jugador"] if atacante == "jugador" else POS["pers_hollow"]
        dx       = -60 if atacante == "jugador" else 60
        pasos    = [dx//4, dx//4, dx//4, dx//4, -dx//4, -dx//4, -dx//4, -dx//4]

        def mover(i):
            if i >= len(pasos):
                canvas_batalla.coords(ids[key], pos_orig[0], pos_orig[1])
                callback(); return
            canvas_batalla.move(ids[key], pasos[i], 0)
            vm.after(40, lambda: mover(i + 1))

        mover(0)

    def calcular_daño(atacante, defensor):
        danio   = max(1, atacante["ataque"] - defensor["defensa"])
        critico = random.random() < 0.10
        if critico: danio *= 2
        return danio, critico

    def fin_batalla(gano):
        estado["batalla_terminada"] = True
        btn_atacar.config(state="disabled")
        btn_elegir.config(state="disabled")

        if gano:
            mundos_vencidos[mundo["numero"]] = True
            log("¡VICTORIA! Has derrotado al Hollow.")

            canvas_mapa.delete("all")
            canvas_mapa.create_image(0, 0, anchor="nw", image=img_mapa_tk)

            def refrescar(lista, i):
                if i >= len(lista): return
                m = lista[i]
                if mundos_vencidos[m["numero"]] and canvas_mapa.img_x_tk:
                    canvas_mapa.create_image(m["x"], m["y"],
                                             anchor="center", image=canvas_mapa.img_x_tk)
                refrescar(lista, i + 1)

            def recrear_botones(lista, i):
                if i >= len(lista): return
                m   = lista[i]; num = m["numero"]
                if mundos_vencidos[num]:
                    recrear_botones(lista, i + 1); return
                disp = (num == 1) or mundos_vencidos[num - 1]
                if disp:
                    b = tk.Button(canvas_mapa, text=str(num),
                                  font=("Impact", 18, "bold"),
                                  bg="#2c3e50", fg="white",
                                  activebackground="#DAA520", activeforeground="#2c3e50",
                                  bd=0, highlightthickness=0, cursor="hand2",
                                  command=lambda md=m: abrir_mundo(
                                      md, ventana_mapa, canvas_mapa, img_mapa_tk, lista_mundos))
                else:
                    b = tk.Button(canvas_mapa, text=str(num),
                                  font=("Impact", 18, "bold"),
                                  bg="#555555", fg="#888888",
                                  bd=0, highlightthickness=0, state="disabled")
                canvas_mapa.create_window(m["x"], m["y"], anchor="center", window=b)
                recrear_botones(lista, i + 1)

            refrescar(lista_mundos, 0)
            recrear_botones(lista_mundos, 0)

            vr = tk.Toplevel(vm); vr.title("Victoria!")
            vr.geometry("420x220+230+200"); vr.resizable(False, False)
            vr.configure(bg="#2c3e50"); vr.transient(vm); vr.grab_set()
            tk.Label(vr, text="¡HOLLOW DERROTADO!", font=("Impact", 22, "bold"),
                     bg="#2c3e50", fg="#DAA520").pack(pady=15)
            tk.Label(vr, text="Puntos esta batalla: " + str(estado["pts_batalla_j"]),
                     font=("Arial", 13), bg="#2c3e50", fg="white").pack()
            tk.Label(vr, text="Puntos totales:  " + str(puntaje_global["jugador"]),
                     font=("Impact", 14), bg="#2c3e50", fg="#27ae60").pack(pady=5)

            def cerrar():
                vr.destroy(); vm.destroy()
                if todos(list(mundos_vencidos.values()), lambda x: x):
                    abrir_victoria_final(ventana_mapa)

            tk.Button(vr, text="CONTINUAR", font=("Impact", 13), bg="#27ae60",
                      fg="white", width=14, command=cerrar).pack(pady=15)
        else:
            log("Has sido derrotado... El Hollow ganó.")
            vd = tk.Toplevel(vm); vd.title("Derrota")
            vd.geometry("420x200+230+200"); vd.resizable(False, False)
            vd.configure(bg="#2c3e50"); vd.transient(vm); vd.grab_set()
            tk.Label(vd, text="DERROTA", font=("Impact", 22, "bold"),
                     bg="#2c3e50", fg="#e74c3c").pack(pady=20)
            tk.Label(vd, text="El Hollow ha derrotado a todos tus personajes.",
                     font=("Arial", 13), bg="#2c3e50", fg="white").pack()
            tk.Button(vd, text="SALIR", font=("Impact", 13), bg="#c0392b",
                      fg="white", width=14,
                      command=lambda: [vd.destroy(), vm.destroy()]).pack(pady=15)

    def turno_hollow():
        if estado["batalla_terminada"]: return
        p_h = equipo_hollow[estado["idx_hollow"]]
        p_j = equipo_jugador[estado["idx_jugador"]]

        def ejecutar():
            danio, critico = calcular_daño(p_h, p_j)
            p_j["vida"] -= danio
            msg = "Hollow ataca con " + p_h["nombre"] + " → " + str(danio) + " daño"
            if critico: msg += " ¡CRITICO!"
            log(msg)
            dibujar_barras()

            if p_j["vida"] <= 0:
                log(p_j["nombre"] + " fue derrotado.")
                capturado = hacer_copia(p_j["nombre"], "hollow")
                equipo_hollow.append(capturado)
                equipo_jugador[estado["idx_jugador"]]["vida"] = 0
                puntaje_global["hollow"] += 1
                estado["pts_batalla_h"]  += 1
                lbl_puntaje_h.config(text="Hollow: " + str(puntaje_global["hollow"]) + " pts")

                vivos_j = filtrar(equipo_jugador, lambda p: p["vida"] > 0)
                if not vivos_j:
                    dibujar_escena(); fin_batalla(False); return
                idx = buscar_indice(equipo_jugador, lambda p: p["vida"] > 0)
                estado["idx_jugador"] = idx
                log("Tu próximo personaje es " + vivos_j[0]["nombre"] + ".")
                dibujar_escena()

            estado["turno"] = "jugador"
            btn_atacar.config(state="normal")
            btn_elegir.config(state="normal")

        animar_ataque("hollow", lambda: vm.after(300, ejecutar))

    def accion_atacar():
        if estado["batalla_terminada"] or estado["turno"] != "jugador": return
        btn_atacar.config(state="disabled")
        btn_elegir.config(state="disabled")

        p_j = equipo_jugador[estado["idx_jugador"]]
        p_h = equipo_hollow[estado["idx_hollow"]]

        def despues():
            danio, critico = calcular_daño(p_j, p_h)
            p_h["vida"] -= danio
            msg = p_j["nombre"] + " ataca → " + str(danio) + " daño"
            if critico: msg += " ¡CRITICO!"
            log(msg)
            dibujar_barras()

            if p_h["vida"] <= 0:
                log(p_h["nombre"] + " del Hollow fue derrotado.")

                capturado = hacer_copia(p_h["nombre"], "jugador")
                equipo_jugador.append(capturado)
                equipo_hollow[estado["idx_hollow"]]["vida"] = 0

                if p_h["nombre"] not in personajes_ganados:
                    personajes_ganados.append(p_h["nombre"])

                puntaje_global["jugador"]  += 1
                estado["pts_batalla_j"]    += 1
                lbl_puntaje_j.config(text="Guardian: " + str(puntaje_global["jugador"]) + " pts")
                log("¡Capturaste a " + p_h["nombre"] + "! Ahora es tuyo para siempre.")

                vivos_h = filtrar(equipo_hollow,
                                  lambda p: p["vida"] > 0 and p["duenio"] == "hollow")
                if not vivos_h:
                    dibujar_escena(); fin_batalla(True); return
                idx = buscar_indice(equipo_hollow,
                                    lambda p: p["vida"] > 0 and p["duenio"] == "hollow")
                estado["idx_hollow"] = idx
                log("El Hollow envía a " + vivos_h[0]["nombre"] + ".")
                dibujar_escena()
                estado["turno"] = "hollow"
                vm.after(600, turno_hollow)
                return

            dibujar_escena()
            estado["turno"] = "hollow"
            vm.after(600, turno_hollow)

        animar_ataque("jugador", despues)

    def accion_elegir():
        if estado["batalla_terminada"]: return

        vivos = filtrar(
            list(enumerate(equipo_jugador)),
            lambda t: t[1]["vida"] > 0 and t[0] != estado["idx_jugador"]
        )

        if not vivos:
            log("No tienes otros personajes disponibles.")
            return

        ve = tk.Toplevel(vm)
        ve.title("Elegir personaje")
        ve.geometry("680x350+160+170")  # Ventana más ancha para el scroll horizontal
        ve.resizable(False, False)
        ve.configure(bg="#2c3e50")
        ve.transient(vm)
        ve.grab_set()

        tk.Label(ve, text="ELIGE TU PERSONAJE", font=("Impact", 18, "bold"),
                 bg="#2c3e50", fg="#DAA520").pack(pady=10)

        # Contenedor con scroll horizontal
        frame_cards_container = tk.Frame(ve, bg="#2c3e50")
        frame_cards_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar horizontal
        scroll_h = tk.Scrollbar(frame_cards_container, orient="horizontal")
        scroll_h.pack(side="bottom", fill="x")

        # Canvas que contendrá los personajes (scroll horizontal)
        canvas_cards = tk.Canvas(frame_cards_container, bg="#2c3e50",
                                 highlightthickness=0,
                                 xscrollcommand=scroll_h.set)
        canvas_cards.pack(side="top", fill="both", expand=True)

        scroll_h.config(command=canvas_cards.xview)

        # Frame interno donde se colocarán las cards de personajes
        frame_interno = tk.Frame(canvas_cards, bg="#2c3e50")
        canvas_cards.create_window((0, 0), window=frame_interno, anchor="nw")

        # Actualizar el área de scroll cuando cambie el tamaño del frame interno
        def actualizar_scroll(event):
            canvas_cards.configure(scrollregion=canvas_cards.bbox("all"))
        frame_interno.bind("<Configure>", actualizar_scroll)

        # Scroll con la rueda del mouse (soporta horizontal con Shift + rueda)
        def scroll_horizontal(event):
            if event.state & 0x0001:  # Shift presionado
                canvas_cards.xview_scroll(-1 * int(event.delta / 120), "units")
        canvas_cards.bind("<MouseWheel>", scroll_horizontal)

        refs_e = []

        #se crean las card de todos los personajes menos del seleccionado
        """se crea con la imagen del personaje, el nombre, la vida actual y el daño maximo que va 
        a hacer al otro personaje"""
        def crear_cards(lista, col):
            if not lista: return
            idx_eq, p = lista[0]
            fc = tk.Frame(frame_interno, bg="#1a1a2e", padx=6, pady=6,
                          highlightthickness=1, highlightbackground="#DAA520")
            fc.grid(row=0, column=col, padx=8, pady=5, sticky="n")

            try:
                img2 = Image.open(os.path.join(ruta_base, p["archivo"])).resize((80, 90))
                itk2 = ImageTk.PhotoImage(img2)
            except:
                itk2 = ImageTk.PhotoImage(Image.new("RGB", (80, 90), "#555"))
            refs_e.append(itk2)

            tk.Label(fc, image=itk2, bg="#1a1a2e").pack()
            tk.Label(fc, text=p["nombre"], font=("Impact", 10),
                     bg="#1a1a2e", fg="#DAA520").pack()
            pct      = max(0, p["vida"] / p["vida_max"])
            col_vida = "#27ae60" if pct > 0.5 else "#e67e22" if pct > 0.25 else "#e74c3c"
            tk.Label(fc, text="HP: " + str(max(0, p["vida"])) + "/" + str(p["vida_max"]),
                     font=("Arial", 8), bg="#1a1a2e", fg=col_vida).pack()
            atk_real = max(1, p["ataque"] - equipo_hollow[estado["idx_hollow"]]["defensa"])
            tk.Label(fc, text="Daño: " + str(atk_real) + " (ATK " + str(p["ataque"]) + ")",
                     font=("Arial", 8), bg="#1a1a2e", fg="#aaaaaa").pack()

            def elegir(i=idx_eq, nombre=p["nombre"]):
                estado["idx_jugador"] = i
                log("Cambiaste a " + nombre + ". (sin gastar turno)")
                dibujar_escena()
                ve.destroy()

            tk.Button(fc, text="ELEGIR", font=("Impact", 9),
                      bg="#DAA520", fg="#2c3e50", width=8,
                      command=elegir).pack(pady=4)

            crear_cards(lista[1:], col + 1)

        crear_cards(vivos, 0)

        tk.Button(ve, text="CANCELAR", font=("Impact", 11), bg="#c0392b",
                  fg="white", width=12, command=ve.destroy).pack(pady=8)

    btn_atacar.config(command=accion_atacar)
    btn_elegir.config(command=accion_elegir)

    dibujar_escena()
    log("¡Batalla iniciada! Es tu turno, Guardian.")
    log(nombres_jugador[0] + " vs " + nombres_hollow[0])



# #############################################
#  BOTONES VENTANA PRINCIPAL
# #############################################
tk.Button(frame_boton_personajes, text="Personajes", font=("Impact", 14),
          bg="#DAA520", width=20, height=1,
          command=abrir_pesonajes).pack()

tk.Button(frame_boton_avatar, text="Avatar", font=("Impact", 14),
          bg="#DAA520", width=20, height=1,
          command=abrir_avatar).pack()

tk.Button(ventana_inicial, text="Iniciar", font=("Impact", 14),
          bg="#DAA520", width=20, height=1,
          command=validar_e_iniciar).place(relx=0.5, y=420, anchor="center")

tk.Button(ventana_inicial, text="About", font=("Impact", 14),
          bg="#DAA520", width=20, height=1,
          command=abrir_about).place(relx=0.5, y=470, anchor="center")

ventana_inicial.mainloop()