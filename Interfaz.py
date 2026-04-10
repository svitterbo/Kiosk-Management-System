import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

URL_SERVIDOR = "http://127.0.0.1:5000/api/inventario"

def actualizar_pantalla():
    lista_productos.delete(0, tk.END)
    try:
        margen_actual = float(entry_margen.get())
    except ValueError:
        margen_actual = 40.0
    try:
        respuesta = requests.get(URL_SERVIDOR)
        inventario_nube = respuesta.json()
        if not inventario_nube:
            lista_productos.insert(tk.END, "El inventario está vacío.")
        for nombre, datos in inventario_nube.items():
            costo = datos['costo']
            cantidad = datos['cantidad']
            precio_final = costo + (costo * (margen_actual / 100))
            texto = f"{nombre.title()} | Stock: {cantidad} | Costo: ${costo} | VENTA: ${precio_final:.2f}"
            lista_productos.insert(tk.END, texto)
    except Exception as e:
        print(f"⚠️ Error técnico de conexión: {e}") 
        messagebox.showerror("Error de Conexión", "No se pudo conectar con el servidor. ¿Está encendido?")

def boton_agregar_click():
    nombre = entry_nombre.get()
    cantidad = entry_cantidad.get()
    costo = entry_costo.get()
    if not nombre or not cantidad or not costo:
        messagebox.showwarning("Atención", "Por favor, llená todos los campos.")
        return
    datos_a_enviar = {"nombre": nombre, "cantidad": int(cantidad), "costo": float(costo)}
    res = requests.post("http://127.0.0.1:5000/api/agregar", json=datos_a_enviar)
    if res.status_code == 200:
        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_costo.delete(0, tk.END)
        actualizar_pantalla()
    else:
        messagebox.showerror("Error", "El servidor rechazó los datos.")

def boton_eliminar_click():
    seleccion = lista_productos.curselection()
    if not seleccion:
        messagebox.showwarning("Atención", "Primero hacé clic en un producto de la lista.")
        return
    texto_seleccionado = lista_productos.get(seleccion[0])
    nombre_producto = texto_seleccionado.split("|")[0].strip().lower()
    respuesta = messagebox.askyesno("Confirmar", f"¿Estás recontra seguro de eliminar '{nombre_producto.title()}'?")
    if respuesta:
        url = f"http://127.0.0.1:5000/api/eliminar/{nombre_producto}"
        res = requests.delete(url)
        if res.status_code == 200:
            actualizar_pantalla() 
        else:
            messagebox.showerror("Error", "El servidor no pudo eliminar el producto.")

def boton_vender_click():
    seleccion = lista_productos.curselection()
    if not seleccion:
        messagebox.showwarning("Atención", "Primero hacé clic en un producto de la lista para venderlo.")
        return
    texto_seleccionado = lista_productos.get(seleccion[0])
    nombre_producto = texto_seleccionado.split("|")[0].strip().lower()
    cantidad_a_vender = simpledialog.askinteger("Caja Registradora", f"¿Cuántas unidades de '{nombre_producto.title()}' vas a vender?", minvalue=1)
    if cantidad_a_vender:
        datos_a_enviar = {"nombre": nombre_producto, "cantidad": cantidad_a_vender}
        res = requests.post("http://127.0.0.1:5000/api/vender", json=datos_a_enviar)
        if res.status_code == 200:
            respuesta_json = res.json()
            messagebox.showinfo("Éxito", respuesta_json['mensaje'])
            actualizar_pantalla() 
        else:
            respuesta_json = res.json()
            messagebox.showerror("Error de Venta", respuesta_json.get('error', "No se pudo vender."))

ventana = tk.Tk()
ventana.title("Sistema de Gestión - Mi Kiosco (CONECTADO A LA NUBE)")
ventana.geometry("480x600")
ventana.config(padx=20, pady=20)

tk.Label(ventana, text="Gestión de Inventario (Kiosco)", font=("Arial", 16, "bold")).pack(pady=10)

frame_margen = tk.Frame(ventana)
frame_margen.pack(pady=10)
tk.Label(frame_margen, text="Margen de Ganancia (%): ", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
entry_margen = tk.Entry(frame_margen, width=8)
entry_margen.insert(0, "40") 
entry_margen.pack(side=tk.LEFT)
tk.Button(frame_margen, text="Recalcular", bg="orange", command=actualizar_pantalla).pack(side=tk.LEFT, padx=10)

lista_productos = tk.Listbox(ventana, width=60, height=12)
lista_productos.pack(pady=10)

tk.Label(ventana, text="Nombre del Producto:").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()
tk.Label(ventana, text="Cantidad (Stock):").pack()
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()
tk.Label(ventana, text="Precio de Costo ($):").pack()
entry_costo = tk.Entry(ventana)
entry_costo.pack()

tk.Button(ventana, text="Agregar Producto", bg="green", fg="white", font=("Arial", 10, "bold"), command=boton_agregar_click).pack(pady=20)
tk.Button(ventana, text="Eliminar Producto Seleccionado", bg="red", fg="white", font=("Arial", 10, "bold"), command=boton_eliminar_click).pack(pady=5)
tk.Button(ventana, text="Registrar Venta (Restar Stock)", bg="blue", fg="white", font=("Arial", 10, "bold"), command=boton_vender_click).pack(pady=5)

actualizar_pantalla()
ventana.mainloop()