import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
import serial as tarjeta
from main_gui import Ui_MainWindow 

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def _get_main_stylesheet(self):
        return """
        QWidget {
            background-color: #1A1D21; 
            color: #D0D8E0; 
            font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            font-size: 10pt;
        }
        QMainWindow {
        }
        QLabel {
            color: #C0C8D0; 
            padding: 2px;
        }
        QLabel#motorStatusLed {
            font-size: 20pt; 
            color: #333940; 
            qproperty-alignment: 'AlignCenter';
            min-width: 25px;
            font-weight: bold;
        }
        QLineEdit {
            background-color: #2C313A; 
            border: 1px solid #4A505A; 
            border-radius: 5px;
            padding: 7px 10px; 
            color: #E0E8F0; 
            font-size: 11pt;
        }
        QLineEdit:focus {
            border: 1px solid #00AEEF; 
            background-color: #303540; 
        }
        QPushButton { 
            background-color: #007B8C; 
            color: #FFFFFF;
            border: 1px solid #005F6B;
            border-radius: 5px;
            padding: 7px 15px; 
            font-size: 10pt;
            font-weight: bold;
            min-height: 28px;
        }
        QPushButton:hover {
            background-color: #009CB0; 
            border-color: #007B8C;
        }
        QPushButton:pressed {
            background-color: #005F6B; 
        }
        QPushButton:disabled {
            background-color: #4A505A;
            color: #707880;
            border-color: #3A3F4A;
        }
        QCheckBox {
            spacing: 8px; 
            color: #C0C8D0;
        }
        QCheckBox::indicator {
            width: 18px; 
            height: 18px;
            border: 1px solid #4A505A;
            border-radius: 4px;
            background-color: #2C313A;
        }
        QCheckBox::indicator:checked {
            background-color: #00AEEF; 
            border: 1px solid #0088CC;
        }
        QCheckBox::indicator:hover {
            border: 1px solid #00AEEF;
        }
        QGroupBox {
            font-weight: bold;
            font-size: 12pt; 
            border: 1px solid #4A505A;
            border-radius: 8px; 
            margin-top: 12px; 
            background-color: #23272E; 
            padding-top: 10px; 
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left; 
            padding: 4px 12px; 
            left: 12px; 
            color: #00AEEF; 
            background-color: #2C313A; 
            border: 1px solid #4A505A;
            border-bottom: 1px solid #2C313A; 
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTextEdit { 
            background-color: #171A1E; 
            border: 1px solid #3A3F4A;
            border-radius: 5px;
            color: #A0A8B0; 
            font-family: "Consolas", "Lucida Console", monospace;
            padding: 8px;
            font-size: 9pt;
        }
        QScrollBar:vertical {
            border: none;
            background: #23272E; 
            width: 12px; 
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #4A505A; 
            min-height: 25px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #5A606A;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        QScrollBar:horizontal {
            border: none;
            background: #23272E;
            height: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:horizontal {
            background: #4A505A;
            min-width: 25px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #5A606A;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        QMenuBar {
            background-color: #2C313A;
            color: #D0D8E0;
        }
        QMenuBar::item {
            background: transparent;
            padding: 4px 10px;
        }
        QMenuBar::item:selected {
            background-color: #00AEEF;
            color: #1A1D21;
        }
        QMenu {
            background-color: #2C313A;
            border: 1px solid #4A505A;
            color: #D0D8E0;
        }
        QMenu::item:selected {
            background-color: #00AEEF;
            color: #1A1D21;
        }
        QStatusBar {
            background-color: #2C313A;
            color: #A0A8B0;
        }
        """

    def _update_status_label_color(self, status_text):
        color = "#FFC107" 

        if "CONECTADO" in status_text.upper() and "SIMULACIÓN" not in status_text.upper():
            color = "#00E676"
        elif "SIMULACIÓN ACTIVA (CONECTADO)" in status_text.upper():
            color = "#69F0AE"
        elif "DESCONECTADO" in status_text.upper() or "ERROR" in status_text.upper() or "NOT CONNECTED" in status_text.upper():
            color = "#FF5252"
        elif "CONECTANDO..." in status_text.upper(): 
            color = "#29B6F6" 
        elif "CONNECTING" in status_text.upper() or "RECONECTAR" in status_text.upper():
            color = "#FFAB40"
        elif "SIMULACIÓN ACTIVA (DESCONECTADO)" in status_text.upper():
            color = "#FFD180"

        self.txt_estado.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 13pt; padding: 3px;")
        self.txt_estado.setText(status_text)

    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        
        self.setStyleSheet(self._get_main_stylesheet())

        self.modo_simulacion = False
        self.arduino = None
        self.btn_accion.clicked.connect(self.accion)
        self.segundoPlano = QtCore.QTimer(self) 
        self.segundoPlano.timeout.connect(self.lecturas)
        self.sim_timer_counter = 0

        self.datos = []
        self.btn_control_led.clicked.connect(self.control)

        self.btn_up_0.clicked.connect(lambda: self.arduino_write_command("01", self.izq1, self.status_en1))
        self.btn_down_1.clicked.connect(lambda: self.arduino_write_command("00", self.der1, self.status_en1))
        self.btn_left_2.clicked.connect(lambda: self.arduino_write_command("11", self.izq2, self.status_en2))
        self.btn_right_3.clicked.connect(lambda: self.arduino_write_command("10", self.der2, self.status_en2))
        self.btn_center_4.clicked.connect(lambda: self.arduino_write_command("41", self.izq5, self.status_en5))

        self.btn_up_5.clicked.connect(lambda: self.arduino_write_command("21", self.izq3, self.status_en3))
        self.btn_down_6.clicked.connect(lambda: self.arduino_write_command("20", self.der3, self.status_en3))
        self.btn_left_7.clicked.connect(lambda: self.arduino_write_command("31", self.izq4, self.status_en4))
        self.btn_right_9.clicked.connect(lambda: self.arduino_write_command("30", self.der4, self.status_en4))
        self.btn_center_10.clicked.connect(lambda: self.arduino_write_command("40", self.der5, self.status_en5))

        self.btn_Avanzar.clicked.connect(lambda: self.arduino_write_command("138")) 
        self.btn_Stop.clicked.connect(lambda: self.arduino_write_command("255"))    
        self.btn_Retroceder.clicked.connect(lambda: self.arduino_write_command("61")) 
        self.chk_simulacion.stateChanged.connect(self.toggle_simulation_mode)
        self.btn_limpiar_datos.clicked.connect(self.limpiar_datos_display)

        self._update_status_label_color(self.txt_estado.text())
        
        for i in range(1, 6):
            led_label = getattr(self, f"status_en{i}", None)
            if led_label:
                self._set_led_status(led_label, False)

    def _set_led_status(self, led_label, active):
        if active:
            led_label.setStyleSheet("QLabel#motorStatusLed { color: #00E676; }")
        else:
            led_label.setStyleSheet("QLabel#motorStatusLed { color: #333940; }")

    def limpiar_datos_display(self):
        self.text_edit_datos.clear()
        self.datos = []
        print("Datos display cleared.")

    def activar_boton_visual(self, boton):
        pass 

    def arduino_write_command(self, command, direction_checkbox=None, status_led_label=None):
        if self.modo_simulacion:
            log_message = f"[SIM CMD] Enviado: {command}"
            print(log_message) 
            self.text_edit_datos.append(log_message) 
            self.text_edit_datos.ensureCursorVisible() 

            if direction_checkbox:
                direction_checkbox.setChecked(True)
            if status_led_label:
                self._set_led_status(status_led_label, True)
            
            if direction_checkbox or status_led_label:
                QtCore.QTimer.singleShot(500, lambda: (
                    direction_checkbox.setChecked(False) if direction_checkbox else None,
                    self._set_led_status(status_led_label, False) if status_led_label else None
                ))
        else:
            if self.arduino and self.arduino.isOpen():
                try:
                    self.arduino.write(command.encode())
                    print(f"Sent command: {command}")
                    if direction_checkbox: direction_checkbox.setChecked(True)
                    if status_led_label: self._set_led_status(status_led_label, True)
                    
                    if direction_checkbox or status_led_label:
                        QtCore.QTimer.singleShot(500, lambda: (
                            direction_checkbox.setChecked(False) if direction_checkbox else None,
                            self._set_led_status(status_led_label, False) if status_led_label else None
                        ))
                except tarjeta.SerialException as e:
                    print(f"Serial communication error: {e}")
                    self._update_status_label_color("COM Error")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            else:
                print("Arduino not connected.")
                self._update_status_label_color("Not Connected")

    def keyPressEvent(self, event):
        key_map = {
            QtCore.Qt.Key_W: (self.btn_up_0, "01", self.izq1, self.status_en1),
            QtCore.Qt.Key_S: (self.btn_down_1, "00", self.der1, self.status_en1),
            QtCore.Qt.Key_A: (self.btn_left_2, "11", self.izq2, self.status_en2),
            QtCore.Qt.Key_D: (self.btn_right_3, "10", self.der2, self.status_en2),
            QtCore.Qt.Key_Q: (self.btn_center_4, "41", self.izq5, self.status_en5),
            QtCore.Qt.Key_U: (self.btn_up_5, "21", self.izq3, self.status_en3),
            QtCore.Qt.Key_J: (self.btn_down_6, "20", self.der3, self.status_en3),
            QtCore.Qt.Key_H: (self.btn_left_7, "31", self.izq4, self.status_en4),
            QtCore.Qt.Key_K: (self.btn_right_9, "30", self.der4, self.status_en4),
            QtCore.Qt.Key_Y: (self.btn_center_10, "40", self.der5, self.status_en5),
            QtCore.Qt.Key_1: (self.btn_Retroceder, "61"), 
            QtCore.Qt.Key_2: (self.btn_Stop, "255"),    
            QtCore.Qt.Key_3: (self.btn_Avanzar, "138"), 
        }

        action_tuple = key_map.get(event.key())
        if action_tuple:
            if hasattr(action_tuple[0], 'click'): 
                 action_tuple[0].animateClick(100) 

            if len(action_tuple) == 4:
                _, comando, direction_cb, status_led = action_tuple
                self.arduino_write_command(comando, direction_cb, status_led)
            elif len(action_tuple) == 2:
                _, comando = action_tuple
                self.arduino_write_command(comando)

    def toggle_simulation_mode(self, state):
        self.modo_simulacion = (state == QtCore.Qt.Checked)
        if self.modo_simulacion:
            self.lbl_sim_status.setText("Simulación: ACTIVA")
            self.lbl_sim_status.setStyleSheet("color: #69F0AE; font-style: italic; font-weight: bold;")
            print("Modo Simulación ACTIVADO")
            if self.arduino and self.arduino.isOpen(): 
                self.segundoPlano.stop()
                self.arduino.close()
                self.arduino = None
            self.btn_accion.setText("CONECTAR (SIM)")
            self._update_status_label_color("SIMULACIÓN ACTIVA (DESCONECTADO)")
        else:
            self.lbl_sim_status.setText("Simulación: INACTIVA")
            self.lbl_sim_status.setStyleSheet("color: #FFAB40; font-style: italic;")
            print("Modo Simulación DESACTIVADO")
            if self.segundoPlano.isActive(): 
                self.segundoPlano.stop()
            self.btn_accion.setText("CONECTAR")
            self._update_status_label_color("DESCONECTADO")

    def control(self):
        texto = self.btn_control_led.text()
        if self.modo_simulacion:
            if "PRENDER" in texto.upper():
                self.btn_control_led.setText("APAGAR LED")
                print("[SIM] LED Encendido")
            else:
                self.btn_control_led.setText("PRENDER LED")
                print("[SIM] LED Apagado")
        else:
            if self.arduino and self.arduino.isOpen():
                try:
                    if "PRENDER" in texto.upper():
                        self.btn_control_led.setText("APAGAR LED")
                        self.arduino.write("1".encode())
                        print("Sent command: 1 (LED ON)")
                    else:
                        self.btn_control_led.setText("PRENDER LED")
                        self.arduino.write("0".encode())
                        print("Sent command: 0 (LED OFF)")
                except tarjeta.SerialException as e:
                    print(f"Serial communication error: {e}")
                    self._update_status_label_color("COM Error")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            else:
                print("Arduino not connected. Cannot control LED.")
                self._update_status_label_color("Not Connected")

    def lecturas(self):
        if self.modo_simulacion:
            self.sim_timer_counter += 1
            sim_data = f"SimData-{self.sim_timer_counter}: VAL={time.time()%100:.2f}"
            if self.sim_timer_counter % 5 == 0:
                sim_data = f"Event: {['Alpha','Bravo','Charlie','Delta','Echo'][self.sim_timer_counter % 5]}"
            
            self.text_edit_datos.append(sim_data) 
        elif self.arduino and self.arduino.isOpen():
            try:
                if self.arduino.inWaiting() > 0:
                    cadena = self.arduino.readline().decode('utf-8', errors='ignore').strip()
                    if cadena:
                        self.text_edit_datos.append(cadena)
                        print(f"Received: {cadena}")
            except tarjeta.SerialException as e:
                print(f"Serial read error: {e}")
                if self.arduino and self.arduino.isOpen(): self.arduino.close()
                self.arduino = None
                self.segundoPlano.stop()
                self.btn_accion.setText("RECONECTAR")
                self._update_status_label_color("Read Error - Disconnected")
            except Exception as e:
                print(f"An unexpected error occurred during read: {e}")
        self.text_edit_datos.ensureCursorVisible()


    def accion(self):
        texto_btn = self.btn_accion.text()
        com_port = self.txt_com.text().strip() 

        if self.modo_simulacion:
            if "CONECTAR (SIM)" in texto_btn:
                if not self.segundoPlano.isActive(): 
                    self.segundoPlano.start(500) 
                self.btn_accion.setText("DESCONECTAR (SIM)")
                self._update_status_label_color("SIMULACIÓN ACTIVA (CONECTADO)")
                print("[SIM] Conectado")
            elif "DESCONECTAR (SIM)" in texto_btn:
                if self.segundoPlano.isActive():
                    self.segundoPlano.stop()
                self.btn_accion.setText("CONECTAR (SIM)")
                self._update_status_label_color("SIMULACIÓN ACTIVA (DESCONECTADO)")
                print("[SIM] Desconectado")
            return

        original_button_text = "CONECTAR" 
        if "RECONECTAR" in texto_btn:
            original_button_text = "RECONECTAR"

        if "CONECTAR" in texto_btn or "RECONECTAR" in texto_btn:
            if not com_port:
                self._update_status_label_color("Ingrese Puerto COM")
                QtWidgets.QMessageBox.warning(self, "Error de Conexión", "Por favor, ingrese un puerto COM.")
                return

            if self.arduino and self.arduino.isOpen():
                self.segundoPlano.stop()
                self.arduino.close()
            self.arduino = None

            self.btn_accion.setEnabled(False)
            self.btn_accion.setText("CONECTANDO...")
            self._update_status_label_color("CONECTANDO...") 
            QtWidgets.QApplication.processEvents() 

            try:
                print(f"Attempting to connect to {com_port}...")
                self.arduino = tarjeta.Serial(com_port, baudrate=9600, timeout=1)
                
                start_time = time.time()
                port_opened_within_timeout = False
                while time.time() - start_time < 2.5:
                    if self.arduino.isOpen():
                        port_opened_within_timeout = True
                        break
                    time.sleep(0.05)

                if not port_opened_within_timeout:
                    if self.arduino: self.arduino.close() 
                    raise tarjeta.SerialException(f"Timeout: El puerto {com_port} no se abrió en 2.5s.")

                time.sleep(1.5) 

                if self.arduino.isOpen():
                    if not self.segundoPlano.isActive():
                        self.segundoPlano.start(100)
                    self.btn_accion.setText("DESCONECTAR")
                    self._update_status_label_color(f"CONECTADO en {com_port}")
                    print(f"Connected to {com_port}")
                else:
                    self._update_status_label_color(f"Fallo al abrir {com_port}. Verifique.")
                    print(f"Failed to open serial port {com_port} after reset delay.")
                    if self.arduino: self.arduino.close()
                    self.arduino = None
                    self.btn_accion.setText(original_button_text)

            except tarjeta.SerialException as e:
                error_msg = str(e).splitlines()[0] if str(e) else "Error desconocido al conectar."
                self._update_status_label_color(f"Error: {error_msg}")
                print(f"Serial connection error: {e}")
                QtWidgets.QMessageBox.critical(self, "Error Serial", f"No se pudo conectar a {com_port}.\n{e}")
                if self.arduino: 
                    if self.arduino.isOpen(): self.arduino.close()
                self.arduino = None
                self.btn_accion.setText("RECONECTAR") 
            except Exception as e:
                self._update_status_label_color(f"Error Inesperado: {type(e).__name__}")
                print(f"An unexpected error occurred during connection: {e}")
                QtWidgets.QMessageBox.critical(self, "Error Inesperado", f"Ocurrió un error:\n{e}")
                if self.arduino and self.arduino.isOpen(): self.arduino.close()
                self.arduino = None
                self.btn_accion.setText(original_button_text)
            finally:
                self.btn_accion.setEnabled(True)
                if self.btn_accion.text() == "CONECTANDO...":
                    if self.arduino and self.arduino.isOpen():
                        self.btn_accion.setText("DESCONECTAR")
                    else:
                        self.btn_accion.setText(original_button_text if original_button_text == "RECONECTAR" else "CONECTAR")


        elif "DESCONECTAR" in texto_btn:
            if self.arduino and self.arduino.isOpen():
                self.segundoPlano.stop()
                self.arduino.close()
                self.arduino = None
                self.btn_accion.setText("RECONECTAR")
                self._update_status_label_color("DESCONECTADO")
                print("Disconnected")
            else:
                self._update_status_label_color("No Conectado")
                self.btn_accion.setText("CONECTAR")
                self.arduino = None
                print("Attempted to disconnect, but was not actively connected.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())