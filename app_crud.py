import tkinter as tk
from tkinter import messagebox
import sqlite3

class FacturacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Facturación")
        self.root.geometry("600x400")

        self.init_ui()

    def init_ui(self):
        # Etiquetas y Entradas
        self.label_numero = tk.Label(self.root, text="Número:")
        self.entry_numero = tk.Entry(self.root)

        self.label_cliente = tk.Label(self.root, text="Cliente:")
        self.entry_cliente = tk.Entry(self.root)

        self.label_monto = tk.Label(self.root, text="Monto:")
        self.entry_monto = tk.Entry(self.root)

        # Botones
        self.btn_agregar = tk.Button(self.root, text="Agregar", command=self.agregar_factura)
        self.btn_actualizar = tk.Button(self.root, text="Actualizar", command=self.actualizar_factura)
        self.btn_eliminar = tk.Button(self.root, text="Eliminar", command=self.eliminar_factura)

        # Lista de facturas
        self.listbox_facturas = tk.Listbox(self.root, width=50, height=15)
        self.listbox_facturas.bind("<<ListboxSelect>>", self.mostrar_detalle_factura)

        # Diseño de la interfaz
        self.label_numero.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_numero.grid(row=0, column=1, padx=10, pady=5)

        self.label_cliente.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_cliente.grid(row=1, column=1, padx=10, pady=5)

        self.label_monto.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_monto.grid(row=2, column=1, padx=10, pady=5)

        self.btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)
        self.btn_actualizar.grid(row=4, column=0, columnspan=2, pady=5)
        self.btn_eliminar.grid(row=5, column=0, columnspan=2, pady=5)

        self.listbox_facturas.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky=tk.NW)

        # Cargar las facturas al iniciar
        self.cargar_facturas()

    def cargar_facturas(self):
        # Conectar a la base de datos
        conn = sqlite3.connect('facturas.db')
        cursor = conn.cursor()

        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT,
                cliente TEXT,
                monto REAL
            )
        ''')
        conn.commit()

        # Obtener las facturas
        cursor.execute('SELECT * FROM facturas')
        facturas = cursor.fetchall()

        # Cerrar la conexión
        conn.close()

        # Mostrar las facturas en la lista
        self.listbox_facturas.delete(0, tk.END)
        for factura in facturas:
            self.listbox_facturas.insert(tk.END, f"{factura[0]} - {factura[1]} - {factura[2]} - {factura[3]}")

    def agregar_factura(self):
        numero = self.entry_numero.get()
        cliente = self.entry_cliente.get()
        monto = self.entry_monto.get()

        try:
            monto = float(monto)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        # Conectar a la base de datos
        conn = sqlite3.connect('facturas.db')
        cursor = conn.cursor()

        # Insertar la nueva factura
        cursor.execute('INSERT INTO facturas (numero, cliente, monto) VALUES (?, ?, ?)', (numero, cliente, monto))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Actualizar la lista de facturas
        self.cargar_facturas()

        # Limpiar los campos de entrada
        self.entry_numero.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)

    def actualizar_factura(self):
        seleccion = self.listbox_facturas.curselection()

        if not seleccion:
            messagebox.showinfo("Información", "Selecciona una factura para actualizar.")
            return

        # Obtener el ID de la factura seleccionada
        factura_id = int(self.listbox_facturas.get(seleccion[0]).split()[0])

        numero = self.entry_numero.get()
        cliente = self.entry_cliente.get()
        monto = self.entry_monto.get()

        try:
            monto = float(monto)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        # Conectar a la base de datos
        conn = sqlite3.connect('facturas.db')
        cursor = conn.cursor()

        # Actualizar la factura seleccionada
        cursor.execute('UPDATE facturas SET numero=?, cliente=?, monto=? WHERE id=?', (numero, cliente, monto, factura_id))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Actualizar la lista de facturas
        self.cargar_facturas()

        # Limpiar los campos de entrada
        self.entry_numero.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)

    def eliminar_factura(self):
        seleccion = self.listbox_facturas.curselection()

        if not seleccion:
            messagebox.showinfo("Información", "Selecciona una factura para eliminar.")
            return

        # Obtener el ID de la factura seleccionada
        factura_id = int(self.listbox_facturas.get(seleccion[0]).split()[0])

        # Conectar a la base de datos
        conn = sqlite3.connect('facturas.db')
        cursor = conn.cursor()

        # Eliminar la factura seleccionada
        cursor.execute('DELETE FROM facturas WHERE id=?', (factura_id,))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Actualizar la lista de facturas
        self.cargar_facturas()

        # Limpiar los campos de entrada
        self.entry_numero.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)

    def mostrar_detalle_factura(self, event):
        seleccion = self.listbox_facturas.curselection()

        if seleccion:
            # Obtener el ID de la factura seleccionada
            factura_id = int(self.listbox_facturas.get(seleccion[0]).split()[0])

            # Conectar a la base de datos
            conn = sqlite3.connect('facturas.db')
            cursor = conn.cursor()

            # Obtener la factura seleccionada
            cursor.execute('SELECT * FROM facturas WHERE id=?', (factura_id,))
            factura = cursor.fetchone()

            # Cerrar la conexión
            conn.close()

            # Mostrar los detalles de la factura en los campos de entrada
            self.entry_numero.delete(0, tk.END)
            self.entry_cliente.delete(0, tk.END)
            self.entry_monto.delete(0, tk.END)

            self.entry_numero.insert(tk.END, factura[1])
            self.entry_cliente.insert(tk.END, factura[2])
            self.entry_monto.insert(tk.END, str(factura[3]))


if __name__ == "__main__":
    # Crear la base de datos si no existe
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            cliente TEXT,
            monto REAL
        )
    ''')
    conn.commit()
    conn.close()

    root = tk.Tk()
    app = FacturacionApp(root)
    root.mainloop()
