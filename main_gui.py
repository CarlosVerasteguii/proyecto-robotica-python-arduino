from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 850) 

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_vertical_layout.setContentsMargins(12, 12, 12, 12) 
        main_vertical_layout.setSpacing(12) 

        top_area_layout = self._create_connection_area_ui(self.centralwidget)
        main_vertical_layout.addLayout(top_area_layout)

        main_content_layout = QtWidgets.QHBoxLayout()
        main_content_layout.setSpacing(12) 

        left_column_layout = QtWidgets.QVBoxLayout()
        left_column_layout.setSpacing(12)
        
        self.gb_motor_status = self._create_motor_status_area_ui(self.centralwidget)
        left_column_layout.addWidget(self.gb_motor_status) 
        
        self.gb_dev_options = self._create_dev_options_area_ui(self.centralwidget) 
        left_column_layout.addWidget(self.gb_dev_options)

        left_column_layout.addStretch(1) 
        
        main_content_layout.addLayout(left_column_layout, 25) 

        center_column_layout = QtWidgets.QVBoxLayout() 
        self.gb_motor_controls = self._create_motor_controls_area_ui(self.centralwidget)
        center_column_layout.addWidget(self.gb_motor_controls)
        center_column_layout.addStretch(1) 

        main_content_layout.addLayout(center_column_layout, 50) 

        right_column_layout = QtWidgets.QVBoxLayout()
        right_column_layout.setSpacing(12)

        self.gb_band_control = self._create_band_control_area_ui(self.centralwidget) 
        right_column_layout.addWidget(self.gb_band_control) 
        
        self.gb_data_display = self._create_data_display_area_ui(self.centralwidget)
        right_column_layout.addWidget(self.gb_data_display, 1) 

        main_content_layout.addLayout(right_column_layout, 25) 
        
        main_vertical_layout.addLayout(main_content_layout, 1) 

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _create_connection_area_ui(self, parent_widget):
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)

        self.label = QtWidgets.QLabel("Puerto COM:", parent_widget)
        font = QtGui.QFont(); font.setPointSize(11); font.setBold(True)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.txt_com = QtWidgets.QLineEdit(parent_widget)
        self.txt_com.setMinimumWidth(130); self.txt_com.setMaximumWidth(180)
        font_com = QtGui.QFont(); font_com.setPointSize(12)
        self.txt_com.setFont(font_com)
        self.txt_com.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_com.setObjectName("txt_com")
        layout.addWidget(self.txt_com)

        self.btn_accion = QtWidgets.QPushButton(parent_widget)
        self.btn_accion.setObjectName("btn_accion")
        self.btn_accion.setMinimumWidth(130)
        layout.addWidget(self.btn_accion)

        self.txt_estado = QtWidgets.QLabel(parent_widget)
        self.txt_estado.setMinimumWidth(280)
        font_estado = QtGui.QFont(); font_estado.setPointSize(12); font_estado.setBold(True)
        self.txt_estado.setFont(font_estado)
        self.txt_estado.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_estado.setObjectName("txt_estado")
        layout.addWidget(self.txt_estado, 1) 

        self.btn_control_led = QtWidgets.QPushButton(parent_widget)
        self.btn_control_led.setObjectName("btn_control_led")
        self.btn_control_led.setMinimumWidth(110)
        layout.addWidget(self.btn_control_led)
        return layout

    def _create_motor_status_area_ui(self, parent_widget):
        gb = QtWidgets.QGroupBox(parent_widget)
        gb.setObjectName("gb_motor_status")
        frame_layout = QtWidgets.QVBoxLayout(gb)
        frame_layout.setContentsMargins(12, 25, 12, 12) 
        frame_layout.setSpacing(10) 

        font_motor_label = QtGui.QFont(); font_motor_label.setPointSize(10); font_motor_label.setBold(True)

        motors_data = [
            ("Motor 1:", "izq1", "der1", "status_en1"),
            ("Motor 2:", "izq2", "der2", "status_en2"),
            ("Motor 3:", "izq3", "der3", "status_en3"),
            ("Motor 4:", "izq4", "der4", "status_en4"),
            ("Motor 5:", "izq5", "der5", "status_en5"),
        ]

        for label_text, izq_name, der_name, status_name in motors_data:
            motor_layout = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(label_text, gb)
            label.setFont(font_motor_label)
            label.setMinimumWidth(65) 
            motor_layout.addWidget(label)
            
            izq_cb = QtWidgets.QCheckBox("Izq", gb)
            setattr(self, izq_name, izq_cb)
            motor_layout.addWidget(izq_cb)
            
            der_cb = QtWidgets.QCheckBox("Der", gb)
            setattr(self, der_name, der_cb)
            motor_layout.addWidget(der_cb)
            
            status_led = QtWidgets.QLabel("●", gb)
            status_led.setObjectName("motorStatusLed")
            setattr(self, status_name, status_led)
            motor_layout.addWidget(status_led)
            motor_layout.addStretch(1)
            frame_layout.addLayout(motor_layout)

        return gb

    def _create_data_display_area_ui(self, parent_widget):
        gb = QtWidgets.QGroupBox(parent_widget)
        gb.setObjectName("gb_data_display")
        layout = QtWidgets.QVBoxLayout(gb)
        layout.setContentsMargins(10, 25, 10, 10)
        layout.setSpacing(8)

        self.text_edit_datos = QtWidgets.QTextEdit(gb)
        self.text_edit_datos.setReadOnly(True)
        layout.addWidget(self.text_edit_datos, 1) 

        self.btn_limpiar_datos = QtWidgets.QPushButton("Limpiar Datos", gb)
        self.btn_limpiar_datos.setMinimumWidth(100)
        layout.addWidget(self.btn_limpiar_datos, 0, QtCore.Qt.AlignRight)
        return gb

    def _create_dev_options_area_ui(self, parent_widget):
        gb = QtWidgets.QGroupBox(parent_widget)
        gb.setObjectName("gb_dev_options")
        layout = QtWidgets.QVBoxLayout(gb)
        layout.setContentsMargins(10, 25, 10, 10)
        layout.setSpacing(10)

        self.chk_simulacion = QtWidgets.QCheckBox("Habilitar Simulación Arduino", gb)
        layout.addWidget(self.chk_simulacion)
        
        self.lbl_sim_status = QtWidgets.QLabel("Simulación: INACTIVA", gb)
        font = QtGui.QFont(); font.setItalic(True); font.setWeight(QtGui.QFont.Bold if "ACTIVA" in self.lbl_sim_status.text() else QtGui.QFont.Normal)
        self.lbl_sim_status.setFont(font)
        layout.addWidget(self.lbl_sim_status)
        return gb

    def _create_motor_controls_area_ui(self, parent_widget):
        gb = QtWidgets.QGroupBox(parent_widget) 
        gb.setObjectName("gb_motor_controls")
        
        motor_controls_main_layout = QtWidgets.QVBoxLayout(gb) 
        motor_controls_main_layout.setContentsMargins(10, 25, 10, 10) 
        motor_controls_main_layout.setSpacing(6) 

        button_fixed_size = QtCore.QSize(160, 160)
        icon_draw_size = QtCore.QSize(150, 150)

        buttons_data = {
            "btn_up_0": "icons/motor1_arriba.png",    
            "btn_down_1": "icons/motor1_abajo.png",   
            "btn_left_2": "icons/basejoint_izq.png",  
            "btn_right_3": "icons/basejoint_der.png", 
            "btn_center_4": "icons/motor5_izq.png",   
            "btn_up_5": "icons/motor3_arriba.png",    
            "btn_down_6": "icons/motor3_abajo.png",   
            "btn_left_7": "icons/motor4_arriba.png",  
            "btn_right_9": "icons/motor4_abajo.png",  
            "btn_center_10": "icons/motor5_der.png"   
        }

        for name, icon_path in buttons_data.items():
            button = QtWidgets.QPushButton(gb) 
            button.setText("") 
            try:
                icon = QtGui.QIcon(icon_path)
                if icon.isNull():
                    print(f"Advertencia: No se pudo cargar el icono '{icon_path}' para el botón '{name}'.")
                    button.setText("!") 
                    button.setStyleSheet("QPushButton { color: red; font-size: 48pt; border: 2px dashed red; }")
                else:
                    button.setIcon(icon)
            except Exception as e:
                print(f"Error al cargar icono '{icon_path}' para '{name}': {e}")
                button.setText("X")
                button.setStyleSheet("QPushButton { color: red; font-size: 48pt; border: 2px solid red; }")

            button.setIconSize(icon_draw_size)
            button.setFixedSize(button_fixed_size)
            button.setFlat(True) 
            button.setStyleSheet(
                "QPushButton {"
                "   border: 2px solid #4A505A; " 
                "   border-radius: 12px; " 
                "   background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A3F4A, stop:1 #2C313A);" 
                "}"
                "QPushButton:hover {"
                "   background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4A505A, stop:1 #3C414A);"
                "   border-color: #00AEEF;" 
                "}"
                "QPushButton:pressed {"
                "   background-color: #2C313A;" 
                "   border-color: #0088CC;"
                "}"
            )
            setattr(self, name, button) 

        font_motor_group_label = QtGui.QFont()
        font_motor_group_label.setPointSize(12) # Increased label font size
        font_motor_group_label.setWeight(QtGui.QFont.Bold)
        label_min_width = 170 
        button_row_spacing = 6 

        motor_configs = [
            ("Motor 1:", self.btn_up_0, self.btn_down_1, "Mover Motor 1 Arriba", "Mover Motor 1 Abajo"),
            ("Motor 2 (Base):", self.btn_left_2, self.btn_right_3, "Girar Base a la Izquierda", "Girar Base a la Derecha"),
            ("Motor 3:", self.btn_up_5, self.btn_down_6, "Mover Motor 3 Arriba", "Mover Motor 3 Abajo"),
            ("Motor 4:", self.btn_left_7, self.btn_right_9, "Mover Motor 4 (Muñeca) Arriba", "Mover Motor 4 (Muñeca) Abajo"),
            ("Motor 5 (Pinza):", self.btn_center_4, self.btn_center_10, "Cerrar Pinza / Actuar Herramienta", "Abrir Pinza / Retraer Herramienta")
        ]

        for label_text, btn1_obj, btn2_obj, tooltip_btn1, tooltip_btn2 in motor_configs:
            row_layout = QtWidgets.QHBoxLayout()
            row_layout.setSpacing(button_row_spacing)

            label = QtWidgets.QLabel(label_text, gb)
            label.setFont(font_motor_group_label)
            label.setMinimumWidth(label_min_width)
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight) 
            row_layout.addWidget(label)

            btn1_obj.setToolTip(tooltip_btn1)
            btn2_obj.setToolTip(tooltip_btn2)

            row_layout.addWidget(btn1_obj, 0, QtCore.Qt.AlignVCenter)
            row_layout.addWidget(btn2_obj, 0, QtCore.Qt.AlignVCenter)
            
            row_layout.addStretch(1) 
            motor_controls_main_layout.addLayout(row_layout)

        gb.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        return gb

    def _create_band_control_area_ui(self, parent_widget):
        gb = QtWidgets.QGroupBox(parent_widget)
        gb.setObjectName("gb_band_control")
        outer_v_layout = QtWidgets.QVBoxLayout(gb)
        outer_v_layout.setContentsMargins(10,25,10,10) 

        button_h_layout = QtWidgets.QHBoxLayout()
        button_h_layout.setSpacing(10) 
        button_width = 110; button_height = 80 
        button_size_band = QtCore.QSize(button_width, button_height)

        font_band_icons = QtGui.QFont(); font_band_icons.setPointSize(42); font_band_icons.setBold(True)
        
        self.btn_Retroceder = QtWidgets.QPushButton("←", gb) 
        self.btn_Retroceder.setFont(font_band_icons); self.btn_Retroceder.setFixedSize(button_size_band)
        button_h_layout.addWidget(self.btn_Retroceder)

        self.btn_Stop = QtWidgets.QPushButton("⏹", gb) 
        self.btn_Stop.setFont(font_band_icons); self.btn_Stop.setFixedSize(button_size_band)
        button_h_layout.addWidget(self.btn_Stop)

        self.btn_Avanzar = QtWidgets.QPushButton("→", gb) 
        self.btn_Avanzar.setFont(font_band_icons); self.btn_Avanzar.setFixedSize(button_size_band)
        button_h_layout.addWidget(self.btn_Avanzar)
        
        button_h_layout.addStretch(1) 

        outer_v_layout.addLayout(button_h_layout)
        gb.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        return gb

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Panel de Control Robótico Industrial")) 
        
        self.txt_com.setText(_translate("MainWindow", "COM3")) 
        self.txt_com.setPlaceholderText(_translate("MainWindow", "Ej: COM3"))
        self.btn_accion.setText(_translate("MainWindow", "CONECTAR"))
        self.txt_estado.setText(_translate("MainWindow", "DESCONECTADO"))
        self.btn_control_led.setText(_translate("MainWindow", "PRENDER LED"))

        self.gb_motor_status.setTitle(_translate("MainWindow", "Estado Actuadores")) 
        self.gb_motor_controls.setTitle(_translate("MainWindow", "Control Manual Brazo")) 
        self.gb_data_display.setTitle(_translate("MainWindow", "Telemetría / Logs")) 
        self.gb_band_control.setTitle(_translate("MainWindow", "Control Cinta Transportadora"))
        self.gb_dev_options.setTitle(_translate("MainWindow", "Opciones de Desarrollo"))