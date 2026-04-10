import psycopg2

class Supermercado:
    def __init__(self):
        try:
            self.conexion = psycopg2.connect(
                dbname="kiosco",
                user="postgres",
                password="admin123",
                host="localhost",
                port="5432"
            )
            self.cursor = self.conexion.cursor()
            print("🐘 ¡Conectado a la base de datos PostgreSQL con éxito!")
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")

    def agregar_producto(self, nombre, cantidad, precio_costo):
        nombre_clean = nombre.lower().strip()
        sql = """
            INSERT INTO productos (nombre, cantidad, precio_costo) 
            VALUES (%s, %s, %s)
            ON CONFLICT (nombre) 
            DO UPDATE SET 
                cantidad = productos.cantidad + EXCLUDED.cantidad,
                precio_costo = EXCLUDED.precio_costo;
        """
        try:
            self.cursor.execute(sql, (nombre_clean, cantidad, precio_costo))
            self.conexion.commit() 
        except Exception as e:
            print(f"⚠️ Error al guardar el producto: {e}")
            self.conexion.rollback()

    def obtener_todos(self):
        try:
            self.cursor.execute("SELECT nombre, cantidad, precio_costo FROM productos;")
            filas = self.cursor.fetchall()
            inventario = {}
            for fila in filas:
                inventario[fila[0]] = {"cantidad": fila[1], "costo": fila[2]}
            return inventario
        except Exception as e:
            print(f"⚠️ Error leyendo la base de datos: {e}")
            self.conexion.rollback() 
            return {}

    def eliminar_producto(self, nombre):
        nombre_clean = nombre.lower().strip()
        try:
            self.cursor.execute("DELETE FROM productos WHERE nombre = %s;", (nombre_clean,))
            self.conexion.commit() 
            return True
        except Exception as e:
            print(f"⚠️ Error al eliminar el producto: {e}")
            self.conexion.rollback() 
            return False

    def vender_producto(self, nombre, cantidad_vendida):
        nombre_clean = nombre.lower().strip()
        try:
            self.cursor.execute("SELECT cantidad FROM productos WHERE nombre = %s;", (nombre_clean,))
            resultado = self.cursor.fetchone()
            if resultado:
                stock_actual = resultado[0]
                if stock_actual >= cantidad_vendida:
                    nuevo_stock = stock_actual - cantidad_vendida
                    self.cursor.execute("UPDATE productos SET cantidad = %s WHERE nombre = %s;", (nuevo_stock, nombre_clean))
                    self.conexion.commit()
                    return f"✅ Vendidos {cantidad_vendida} de '{nombre.title()}'. Quedan: {nuevo_stock}"
                else:
                    return f"❌ No hay stock suficiente. Solo quedan {stock_actual} de '{nombre.title()}'."
            else:
                return f"❌ El producto '{nombre.title()}' no existe."
        except Exception as e:
            print(f"⚠️ Error al vender el producto: {e}")
            self.conexion.rollback()
            return f"❌ Error técnico al vender."