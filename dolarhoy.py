import requests
from bs4 import BeautifulSoup
import tkinter as tk
import threading
import time

class CotizacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cotizaciones de Dólar")
        self.root.configure(bg="#f0f0f0")

        self.tipos_de_dolar = []
        self.precios_compra_venta = []
        self.precios_compra_venta_anterior = []

        self.ultima_actualizacion = None

        self.encabezados = ["Tipo de Dólar", "Compra", "Venta", ""]
        self.crear_encabezados()

        self.actualizar_button = tk.Button(root, text="Actualizar", command=self.actualizar_datos, bg="#007bff", fg="white", relief=tk.RIDGE, bd=2, padx=8, pady=2, borderwidth=0, border=0, highlightthickness=0)
        self.actualizar_button.grid(row=1, column=3, pady=(10, 0), padx=10, sticky="ne")

        self.fecha_hora_label = tk.Label(self.root, text="", font=("Helvetica", 10), bg="#f0f0f0", anchor="ne")
        self.fecha_hora_label.grid(row=0, column=3, padx=10, pady=5, sticky="ne")

        self.historial_label = tk.Label(self.root, text="", font=("Helvetica", 10), bg="#f0f0f0", anchor="sw", justify="left")
        self.historial_label.grid(row=9, column=0, columnspan=4, padx=10, pady=(5, 2), sticky="sw")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.actualizar_datos()
        self.actualizar_datos_auto()
        self.actualizar_fecha_hora_actual()

    def crear_encabezados(self):
        for col, encabezado in enumerate(self.encabezados):
            label = tk.Label(self.root, text=encabezado, font=("Helvetica", 12, "bold"), bg="#f0f0f0")
            label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    def obtener_datos(self):
        url = "https://www.dolarhoy.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        tipo_dolar = soup.find_all("a", class_="title")
        self.tipos_de_dolar = [dolar.text for dolar in tipo_dolar]

        precio_compra_venta = soup.find_all("div", class_="val")
        self.precios_compra_venta = [precios.text for precios in precio_compra_venta]

    def mostrar_datos(self):
        for i, tipo in enumerate(self.tipos_de_dolar):
            tk.Label(self.root, text=tipo, bg="#f0f0f0").grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")

            compra = self.precios_compra_venta[i * 2]
            venta = self.precios_compra_venta[i * 2 + 1] if len(self.precios_compra_venta) > i * 2 + 1 else ""

            self.mostrar_precio(i, 1, compra)
            self.mostrar_precio(i, 2, venta)

            self.mostrar_indicador(i, 1, compra, "compra")
            self.mostrar_indicador(i, 2, venta, "venta")

    def mostrar_precio(self, fila, columna, precio):
        tk.Label(self.root, text=precio, bg="#f0f0f0").grid(row=fila + 2, column=columna, padx=10, pady=5, sticky="e")

    def mostrar_indicador(self, fila, columna, precio, tipo):
        if tipo == "compra":
            anterior = self.precios_compra_venta_anterior[fila * 2] if len(self.precios_compra_venta_anterior) > fila * 2 else ""
        else:
            anterior = self.precios_compra_venta_anterior[fila * 2 + 1] if len(self.precios_compra_venta_anterior) > fila * 2 + 1 else ""

        if anterior and precio:
            if precio > anterior:
                indicador = "↑ (+{:.2f}%)".format(((precio - anterior) / anterior) * 100)
                color = "green"
            elif precio < anterior:
                indicador = "↓ (-{:.2f}%)".format(((anterior - precio) / anterior) * 100)
                color = "red"
            else:
                indicador = ""
                color = "black"
        else:
            indicador = ""
            color = "black"

        tk.Label(self.root, text=indicador, bg="#f0f0f0", fg=color).grid(row=fila + 2, column=columna + 1, padx=(0, 10), pady=5, sticky="w")

    def actualizar_datos(self):
        self.precios_compra_venta_anterior = self.precios_compra_venta.copy()
        self.obtener_datos()
        self.mostrar_datos()

        self.ultima_actualizacion = time.strftime("%d/%m/%Y %H:%M:%S")
        self.mostrar_ultima_actualizacion()

    def actualizar_datos_auto(self):
        self.actualizar_datos()
        self.root.after(15 * 60 * 1000, self.actualizar_datos_auto)  # Actualizar cada 15 minutos

    def actualizar_fecha_hora_actual(self):
        fecha_hora_actual = time.strftime("%d/%m/%Y %H:%M:%S")
        self.fecha_hora_label.config(text="Fecha y Hora Actual: " + fecha_hora_actual)
        self.root.after(1000, self.actualizar_fecha_hora_actual)  # Actualizar cada segundo

    def mostrar_ultima_actualizacion(self):
        if self.ultima_actualizacion is not None:
            self.historial_label.config(text="Última Actualización: " + self.ultima_actualizacion)

if __name__ == "__main__":
    root = tk.Tk()
    app = CotizacionApp(root)
    root.mainloop()
