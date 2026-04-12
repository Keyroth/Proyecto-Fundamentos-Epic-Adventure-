import tkinter as tk

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
titulo.place(relx=0.5, y=80, anchor="center")  # relx=0.5 centra horizontalmente

# ========== ETIQUETA "Ingrese Su Nombre" (más arriba) ==========
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
etiqueta_nombre.place(relx=0.5, y=180, anchor="center")  # Centrada, más arriba

# ========== ENTRY PEGADO DEBAJO DE LA ETIQUETA ==========
caja_nombre = tk.Entry(
    ventana_inicial, 
    width=35,
    font=("Arial", 14),
    justify="center"
)
caja_nombre.place(relx=0.5, y=240, anchor="center", width=300)

# ========== ETIQUETA PARA RESULTADO ==========
resultado = tk.Label(
    ventana_inicial, 
    text="", 
    font=("Arial", 14), 
    bg="#2c3e50", 
    fg="white"
)
resultado.place(relx=0.5, y=550, anchor="center")

# ========== 4 BOTONES VERTICALES DEBAJO DEL ENTRY ==========
# Botón 1
boton1 = tk.Button(
    ventana_inicial, 
    text="Personajes", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton1.place(relx=0.5, y=320, anchor="center")

# Botón 2
boton2 = tk.Button(
    ventana_inicial, 
    text="Avatar", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton2.place(relx=0.5, y=370, anchor="center")

# Botón 3
boton3 = tk.Button(
    ventana_inicial, 
    text="Iniciar", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton3.place(relx=0.5, y=420, anchor="center")

# Botón 4
boton4 = tk.Button(
    ventana_inicial, 
    text="About", 
    font=("Impact", 14),
    bg="#DAA520",
    width=20,
    height=1
)
boton4.place(relx=0.5, y=470, anchor="center")

ventana_inicial.mainloop()