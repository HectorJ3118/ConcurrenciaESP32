# ConcurrenciaESP32
Este es el repositorio del proyecto que mezcla el uso de un esp32 con una GUI en python 
```markdown
# 🛒 Proyecto de Simulación de Supermercado con ESP32 y Concurrencia

Este proyecto simula la atención de clientes en un supermercado con múltiples cajas. Usa **concurrencia con hilos (threads)** en Python y comunicación **serial con un ESP32** que visualiza en una pantalla TFT el estado de las cajas (ocupadas o libres).

## 🚀 Tecnologías utilizadas

- Python 3.10+
- `tkinter` para interfaz gráfica
- `threading`, `queue` y `semaphore` para concurrencia
- `pyserial` para comunicación con ESP32
- MicroPython en el ESP32
- Pantalla TFT SPI (controlador ILI9341)

## 📦 Estructura del proyecto

```
ProyectoESP32/
├── proyecto.py           # Código principal con GUI y lógica concurrente
├── ili9341.py            # Librería para control de la pantalla TFT
├── registro_supermercado.csv   # Archivo generado con el registro de atención
├── README.md
```

## 🧠 ¿Qué hace el sistema?

- Genera clientes con cantidad de objetos aleatoria.
- Usa múltiples hilos para simular cajas atendiendo a los clientes.
- Actualiza el estado de las cajas en tiempo real.
- Se comunica con un ESP32 para mostrar en una pantalla TFT:
  - Cuáles cajas están ocupadas
  - Cuáles están libres
  - El número de cada caja
- Guarda el resumen de atención en un archivo `.csv`.

## 📋 Requisitos

- Python ≥ 3.10
- ESP32 con MicroPython instalado
- Librería `pyserial` instalada:
  ```bash
  pip install pyserial
  ```

## 🔌 Conexión ESP32

1. Asegúrate de conocer el **puerto COM** en el que está conectado tu ESP32.
2. Cámbialo en el archivo `proyecto.py` en la línea:

   ```python
   puerto_esp32 = "COM7"
   ```

3. En el ESP32 debe estar cargado el script que usa `ili9341.py` y dibuja círculos según los datos recibidos por serial.

## 🖥️ Cómo usar

1. Ejecuta `proyecto.py`:
   ```bash
   python proyecto.py
   ```

2. En el menú de la interfaz, ve a **Unidad 3 → Concurrencia**.

3. Ajusta el número de clientes y cajas.

4. Pulsa **"Iniciar"** y observa cómo se atienden los clientes.

5. Verifica la pantalla TFT conectada al ESP32 para ver el estado de las cajas en tiempo real.

## 📁 Resultado generado

Después de terminar la simulación, se genera un archivo:

- `registro_supermercado.csv`: contiene información de cada cliente, el total pagado y su tiempo de atención.

## 🤝 Autor

**Héctor Jiménez Martínez**  
Contacto: [hjimenezm2101@alumno.ipn.mx](mailto:hjimenezm2101@alumno.ipn.mx)  
Instituto Politécnico Nacional – ESIME  
Clase: Programación Avanzada  
Fecha: Junio 2025

## 📝 Licencia

Uso académico y libre distribución para fines educativos.
```
