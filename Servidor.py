from flask import Flask, jsonify, request
from Supermercado import Supermercado

app = Flask(__name__)
mi_super = Supermercado()

@app.route('/')
def inicio():
    return "🟢 ¡El servidor del Kiosco (Conectado a BD) está funcionando!"

@app.route('/api/inventario')
def obtener_inventario():
    datos = mi_super.obtener_todos()
    return jsonify(datos)

@app.route('/api/agregar', methods=['POST'])
def agregar_al_inventario():
    nuevo_producto = request.json
    mi_super.agregar_producto(
        nuevo_producto['nombre'], 
        nuevo_producto['cantidad'], 
        nuevo_producto['costo']
    )
    return jsonify({"mensaje": "✅ Producto guardado en la Base de Datos"})

@app.route('/api/eliminar/<nombre_producto>', methods=['DELETE'])
def eliminar_del_inventario(nombre_producto):
    exito = mi_super.eliminar_producto(nombre_producto)
    if exito:
        return jsonify({"mensaje": "🗑️ Producto eliminado"})
    else:
        return jsonify({"error": "Hubo un problema al eliminar"}), 500

@app.route('/api/vender', methods=['POST'])
def vender_del_inventario():
    datos = request.json
    nombre = datos['nombre']
    cantidad = datos['cantidad']
    mensaje = mi_super.vender_producto(nombre, cantidad)
    if "❌" in mensaje:
        return jsonify({"error": mensaje}), 400
    else:
        return jsonify({"mensaje": mensaje})

if __name__ == '__main__':
    print("🚀 Encendiendo servidor en la nube local...")
    app.run(debug=True, port=5000)