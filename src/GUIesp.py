# ############################################################################
# **    Proyecto       : Practica 5.3 Aplicacion de la programacion concurrente
# **    Herramienta    : Visual Studio Code
# **    Fecha/Hora     : 19/06/2025
# **
# **   By             : Hector Jimenez
# **   contact        : hjimenezm2101@alumno.ipn.mx
#  #############################################################################

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :                       Librerias / Bibliotecas / Modulos                      |
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import tkinter as tk
import threading
import queue
import time
import random
import csv
import serial
# +-------------------------------------------------------------------------------
# |       DEFINICION Y DESARROLLO DE CLASES O FUNCIONES DE PROGRAMADOR            |
# +-------------------------------------------------------------------------------


class Cliente:
    contador = 0

    def __init__(self):
        Cliente.contador += 1
        self.id = Cliente.contador
        self.objetos = random.randint(1, 50)
        self.precio_unitario = round(random.uniform(5, 100), 2)
        self.total = round(self.objetos * self.precio_unitario, 2)
        self.tiempo_atencion = round(self.objetos * 0.2, 2)


class Supermercado:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Supermercado + ESP32 TFT")

        self.total_clientes = 0
        self.max_cajas = 4
        self.simulacion_activa = False

        self.cola = queue.Queue()
        self.lock = threading.Lock()
        self.sem = None
        self.atendidos = 0
        self.ingreso_total = 0
        self.registro = []
        self.hilos_cajas = []
        self.estado_cajas = [False]*4


        self.crear_interfaz()

    def crear_interfaz(self):
        frame = tk.Frame(self.ventana)
        frame.pack(pady=10)

        tk.Label(frame, text="Clientes:").grid(row=0, column=0)
        self.entry_clientes = tk.Entry(frame, width=5)
        self.entry_clientes.insert(0, "20")
        self.entry_clientes.grid(row=0, column=1)

        tk.Label(frame, text="Máx. cajas:").grid(row=0, column=2)
        self.entry_cajas = tk.Entry(frame, width=5)
        self.entry_cajas.insert(0, "4")
        self.entry_cajas.grid(row=0, column=3)

        self.btn_iniciar = tk.Button(frame, text="Iniciar", command=self.iniciar_simulacion)
        self.btn_iniciar.grid(row=0, column=4, padx=10)

        self.btn_detener = tk.Button(frame, text="Detener", command=self.detener_simulacion, state="disabled")
        self.btn_detener.grid(row=0, column=5)

        self.resumen_var = tk.StringVar()
        self.resumen_var.set("Atendidos: 0 | Ingreso: $0.00")
        tk.Label(self.ventana, textvariable=self.resumen_var, font=("Arial", 12)).pack(pady=5)

        self.log_text = tk.Text(self.ventana, height=20)
        self.log_text.pack(padx=10, pady=5)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def actualizar_resumen(self):
        self.resumen_var.set(f"Atendidos: {self.atendidos} | Ingreso: ${self.ingreso_total:.2f}")

    def enviar_a_esp32(self):
        if ser and ser.is_open:
            try:
                cajas_str = ",".join(['1' if ocupado else '0' for ocupado in self.estado_cajas])
                ser.write(f"CAJAS:{cajas_str}\n".encode())
            except Exception as e:
                self.log(f"Error al enviar al ESP32: {e}")


    def iniciar_simulacion(self):
        try:
            self.total_clientes = int(self.entry_clientes.get())
            self.max_cajas = int(self.entry_cajas.get())
        except ValueError:
            self.log("Ingresa valores válidos.")
            return

        self.simulacion_activa = True
        self.btn_iniciar.config(state="disabled")
        self.btn_detener.config(state="normal")
        self.sem = threading.Semaphore(self.max_cajas)
        self.atendidos = 0
        self.ingreso_total = 0
        self.registro.clear()
        self.estado_cajas = [False]*4
        self.log("Simulación iniciada.")
        self.actualizar_resumen()


        threading.Thread(target=self.generar_clientes, daemon=True).start()


        for i in range(4):
            t = threading.Thread(target=self.caja, args=(i,), daemon=True)
            t.start()
            self.hilos_cajas.append(t)

    def generar_clientes(self):
        for i in range(self.total_clientes):
            if not self.simulacion_activa:
                break
            time.sleep(random.uniform(0, 2))
            cliente = Cliente()
            self.cola.put(cliente)
            self.log(f"Llega Cliente-{cliente.id} con {cliente.objetos} obj.")
        self.cola.join()
        self.simulacion_activa = False
        self.finalizar_simulacion()

    def caja(self, i):
        while self.simulacion_activa or not self.cola.empty():
            try:
                cliente = self.cola.get(timeout=1)
            except queue.Empty:
                continue

            if not self.sem.acquire(timeout=2):
                continue

            try:
                self.estado_cajas[i] = True
                self.enviar_a_esp32()
                self.log(f"[Caja-{i+1}] Atendiendo Cliente-{cliente.id}")

                self.enviar_a_esp32()
                time.sleep(cliente.tiempo_atencion)

                self.atendidos += 1
                self.ingreso_total += cliente.total
                self.actualizar_resumen()
                self.log(f"[Caja-{i+1}] Terminó Cliente-{cliente.id} | ${cliente.total:.2f}")

                self.registro.append({
                    "Cliente": cliente.id,
                    "Caja": i+1,
                    "Objetos": cliente.objetos,
                    "Precio por objeto": cliente.precio_unitario,
                    "Total pagado": cliente.total,
                    "Tiempo atención (s)": cliente.tiempo_atencion
                })

            finally:
                self.estado_cajas[i] = False
                self.enviar_a_esp32()
                self.sem.release()
                self.cola.task_done()

    def detener_simulacion(self):
        self.simulacion_activa = False
        self.btn_iniciar.config(state="normal")
        self.btn_detener.config(state="disabled")
        self.log("Simulación detenida.")


    def finalizar_simulacion(self):
        self.btn_iniciar.config(state="normal")
        self.btn_detener.config(state="disabled")
        self.log("Todos los clientes fueron atendidos.")
        self.guardar_csv()

    def guardar_csv(self):
        try:
            with open("registro_supermercado.csv", "w", newline="") as CSV:
                campos = ["Cliente", "Caja", "Objetos", "Precio por objeto", "Total pagado", "Tiempo atención (s)"]
                writer = csv.DictWriter(CSV, fieldnames=campos)
                writer.writeheader()
                for fila in self.registro:
                    writer.writerow(fila)
            self.log(" Datos guardados en csv")
        except Exception as e:
            self.log(f" Error al guardar CSV: {e}")

# ===============================================================================
# ||                                                                            ||
# ||        P R O G R A M A / F U N C I O N    P R I N C I P A L                ||
# ||                                                                            ||
# ===============================================================================
if __name__ == "__main__":

    puerto_esp32 = "COM7"
    baudrate = 115200

    try:
        ser = serial.Serial(puerto_esp32, baudrate, timeout=1)
        print(f"Conectado al ESP32 por {puerto_esp32}")
    except:
        ser = None
        print("No se pudo conectar al ESP32")
    ventana = tk.Tk()
    supermercado = Supermercado(ventana)
    ventana.mainloop()