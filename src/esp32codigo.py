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
import time
import select
import sys
import _thread
from machine import Pin, SPI
from ili9341 import Display, color565
# +-------------------------------------------------------------------------------
# |       DEFINICION Y DESARROLLO DE CLASES O FUNCIONES DE PROGRAMADOR            |
# +-------------------------------------------------------------------------------
class MonitorCajas:
    def __init__(self):
        # Colores
        self.rojo    = color565(255, 0, 0)
        self.verde   = color565(0, 255, 0)
        self.negro   = color565(0, 0, 0)
        self.blanco  = color565(255, 255, 255)

        # Posiciones fijas para 4 cuadrantes
        self.pos = [(60, 80), (180, 80), (60, 240), (180, 240)]

        # Estado inicial
        self.estado = [False, False, False, False]

        # Inicializa pantalla
        spi = SPI(1, baudrate=10000000, sck=Pin(18), mosi=Pin(23))
        self.tft = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(17),
                           width=240, height=320, rotation=0)
        self.tft.clear(self.blanco)

    def actualizar_estado(self, nuevos):
        if len(nuevos) == 4:
            self.estado = nuevos

    def dibujar(self):
        for i in range(4):
            x, y = self.pos[i]
            color = self.rojo if self.estado[i] else self.verde
            texto_estado = "Atiende" if self.estado[i] else "Libre"
            texto_caja = f"Caja {i+1}"

            self.tft.fill_circle(x, y, 25, color)
            self.tft.draw_text8x8(x - 20, y + 30, texto_estado, self.negro, self.blanco)
            self.tft.draw_text8x8(x - 20, y - 50, texto_caja, self.negro, self.blanco)

    def dibujar_loop(self):
        while True:
            self.dibujar()
            time.sleep(0.2)

def leer_serial_loop(monitor):
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            try:
                linea = sys.stdin.readline().strip()
                if linea.startswith("CAJAS:"):
                    partes = linea[6:].split(",")
                    if len(partes) == 4:
                        estados = [bool(int(p)) for p in partes]
                        monitor.actualizar_estado(estados)
            except Exception as e:
                print(" Error al leer:", e)
        time.sleep(0.05)

# ===============================================================================
# ||                                                                            ||
# ||        P R O G R A M A / F U N C I O N    P R I N C I P A L                ||
# ||                                                                            ||
# ===============================================================================

monitor = MonitorCajas()

_thread.start_new_thread(monitor.dibujar_loop, ())
_thread.start_new_thread(leer_serial_loop, (monitor,))

