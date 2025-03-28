import sqlite3


class SqlLite:
    def __init__(self, db_name):
        self.data_base = db_name

    def _connect(self):
        try:
            conn = sqlite3.connect(self.data_base)
            return conn
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
            return None

    def _disconnect(self, conn):
        try:
            conn.close()
            print("Database connection closed successfully")
            return True
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
            return None

    """def execute_query(self, query):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Query executed successfully")
            return True
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            self._disconnect(conn)"""

    def execute_query(self, query, params=None):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            self._disconnect(conn)

    def fetch_query(self, query):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            self._disconnect(conn)

    def create_table(self, table_name, columns):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            cursor.execute(query)
            conn.commit()
            print("Table created successfully")
            return True
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            self._disconnect(conn)


if __name__ == "__main__":
    # Example usage
    # Crear una instancia de la clase SqlLite con el nombre de la base de datos
    db = SqlLite("mi_base_de_datos.db")

    # Ejemplo 1: Crear una tabla
    # Definimos el nombre de la tabla y sus columnas
    tabla = "empleados"
    columnas = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        puesto TEXT,
        salario REAL
    """
    db.create_table(tabla, columnas)

    # Ejemplo 2: Insertar datos en la tabla
    query_insert = "INSERT INTO empleados (nombre, puesto, salario) VALUES ('Ana Gómez', 'Desarrolladora', 5500.50)"
    db.execute_query(query_insert)

    # Ejemplo 3: Actualizar datos en la tabla
    query_update = "UPDATE empleados SET salario = 6000.00 WHERE nombre = 'Ana Gómez'"
    db.execute_query(query_update)

    # Ejemplo 4: Consultar datos
    query_select = "SELECT * FROM empleados"
    resultados = db.fetch_query(query_select)

    # Mostrar los resultados
    print("Resultados de la consulta SELECT:")
    for fila in resultados:
        print(fila)

    # Ejemplo 5: Eliminar un registro
    query_delete = "DELETE FROM empleados WHERE nombre = 'Ana Gómez'"
    db.execute_query(query_delete)


