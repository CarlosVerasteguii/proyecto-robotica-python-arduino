# Panel de Control Robótico Industrial con Python y Arduino

Este proyecto implementa una interfaz gráfica de usuario (GUI) desarrollada en Python con PyQt5 para controlar un sistema robótico conectado a un Arduino. Permite enviar comandos, visualizar el estado de los actuadores y recibir datos de telemetría.

## Características Principales

*   Interfaz Gráfica Intuitiva: GUI construida con PyQt5, con un tema oscuro personalizado.
*   Control de Múltiples Actuadores:
    *   Control individual para 5 conjuntos de motores/actuadores (identificados como Motor 1 a Motor 5, incluyendo base y pinza) con indicadores de dirección (Izq/Der) y estado (LEDs).
    *   Control para una cinta transportadora (Avanzar, Stop, Retroceder).
*   Comunicación Serial: Conexión y comunicación con Arduino a través del puerto COM especificado por el usuario (usando "pyserial").
*   Estado de Conexión Dinámico: Indicador visual del estado de la conexión con el Arduino (Desconectado, Conectando, Conectado, Error, etc.).
*   Visualización de Datos: Un área de texto para mostrar logs, comandos enviados y datos recibidos del Arduino (telemetría).
*   Modo Simulación: Permite probar la interfaz y la lógica de comandos sin necesidad de un Arduino conectado físicamente. Los comandos y lecturas simuladas se muestran en el área de datos.
*   Control por Teclado: Atajos de teclado para las principales acciones de control de motores y cinta transportadora.
*   Estilo Personalizado: Hoja de estilos (CSS-like) para una apariencia moderna y consistente de la GUI.
*   Indicadores LED de Estado: LEDs visuales para el estado de los actuadores (encendido/apagado).


## Requisitos Previos

*   Software:
    *   Python 3.x
    *   PyQt5 ("pip install PyQt5")
    *   pyserial ("pip install pyserial")
    *   Arduino IDE (para cargar el sketch en la placa Arduino)
    *   Git (para clonar el repositorio)
*   Hardware (para modo no-simulación):
    *   Placa Arduino (Uno, Mega, Nano, etc.)
    *   Circuitería para motores, LEDs, y cualquier otro actuador/sensor que estés controlando.
    *   Fuente de alimentación adecuada para los componentes.

## Estructura del Proyecto
ROBOTICA/
├── Proyecto/
│ ├── icons/ # Directorio para los iconos de la GUI
│ │ ├── motor1_arriba.png
│ │ ├── motor1_abajo.png
│ │ ├── basejoint_izq.png
│ │ ├── ... (otros iconos)
│ └── main_gui.py # Definición de la estructura de la UI 
├── P_ArduinoPythonGUI_ReadWrite.py # Lógica principal de la aplicación, manejo de eventos y comunicación Arduino
├── README.md # Este archivo


## Atajos de Teclado

*   Motor 1: "W" (Arriba), "S" (Abajo)
*   Motor 2 (Base): "A" (Izquierda), "D" (Derecha)
*   Motor 3: "U" (Arriba), "J" (Abajo)
*   Motor 4 (Muñeca): "H" (Arriba), "K" (Abajo)
*   Motor 5 (Pinza/Herramienta): "Q" (Acción 1/Cerrar), "Y" (Acción 2/Abrir)
*   Cinta Transportadora:
    *   "1": Retroceder
    *   "2": Stop
    *   "3": Avanzar

