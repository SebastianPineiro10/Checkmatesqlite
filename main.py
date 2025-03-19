import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from cryptography.fernet import Fernet
import os

# --- Función para generar y guardar la clave de cifrado ---
def generar_clave():
    return Fernet.generate_key()

def guardar_clave(clave, archivo="clave.key"):
    """Guardar la clave de cifrado en un archivo (solo se hace una vez)."""
    with open(archivo, "wb") as key_file:
        key_file.write(clave)

def cargar_clave(archivo="clave.key"):
    """Cargar la clave de cifrado desde un archivo."""
    if not os.path.exists(archivo):  # Si no existe la clave, generar una nueva
        clave = generar_clave()
        guardar_clave(clave, archivo)
    else:
        with open(archivo, "rb") as key_file:
            clave = key_file.read()
    return clave

# --- Funciones de cifrado y descifrado ---
def cifrar_datos(datos, clave):
    """Cifra los datos antes de guardarlos en el archivo."""
    f = Fernet(clave)
    return f.encrypt(datos.encode())

def descifrar_datos(datos_cifrados, clave):
    """Descifra los datos al leerlos del archivo."""
    f = Fernet(clave)
    return f.decrypt(datos_cifrados).decode()

# --- Función para inicializar la base de datos y crear las tablas ---
def inicializar_bd():
    conn = sqlite3.connect("registros.db")
    cursor = conn.cursor()

    # Crear la tabla de registros si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        trabajador TEXT NOT NULL,
                        tipo_registro TEXT NOT NULL,
                        fecha TEXT NOT NULL,
                        hora TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

# --- Función para verificar si el registro existe para un usuario en el día actual ---
def registro_existe(trabajador, tipo_registro):
    fecha_hoy = datetime.datetime.now().strftime("%d-%m-%Y")
    conn = sqlite3.connect("registros.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM registros WHERE trabajador=? AND fecha=? AND tipo_registro=?''',
                   (trabajador, fecha_hoy, tipo_registro))
    registro = cursor.fetchone()
    conn.close()
    return registro is not None

# --- Función para registrar la entrada ---
def registrar_entrada():
    trabajador = input_trabajador.text().strip()
    contraseña = input_contraseña.text().strip()

    if not validar_usuario(trabajador, contraseña):
        error_label.setText("¡Usuario o contraseña incorrectos!")
        return

    if registro_existe(trabajador, "Entrada"):
        error_label.setText("Ya tienes un registro de entrada hoy.")
        return

    hora_actual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    # Insertar registro en la base de datos
    conn = sqlite3.connect("registros.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO registros (trabajador, tipo_registro, fecha, hora) 
                      VALUES (?, ?, ?, ?)''', (trabajador, "Entrada", hora_actual.split()[0], hora_actual.split()[1]))
    conn.commit()
    conn.close()

    dashboard_entrada.append(f"<b>{hora_actual}</b> - {trabajador} - Entrada registrada")
    error_label.setText(f"Hora de entrada registrada para {trabajador}")

# --- Función para registrar la salida ---
def registrar_salida():
    trabajador = input_trabajador.text().strip()
    contraseña = input_contraseña.text().strip()

    if not validar_usuario(trabajador, contraseña):
        error_label.setText("¡Usuario o contraseña incorrectos!")
        return

    if registro_existe(trabajador, "Salida"):
        error_label.setText("Ya tienes un registro de salida hoy.")
        return

    hora_actual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    # Insertar registro en la base de datos
    conn = sqlite3.connect("registros.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO registros (trabajador, tipo_registro, fecha, hora) 
                      VALUES (?, ?, ?, ?)''', (trabajador, "Salida", hora_actual.split()[0], hora_actual.split()[1]))
    conn.commit()
    conn.close()

    dashboard_salida.append(f"<b>{hora_actual}</b> - {trabajador} - Salida registrada")
    error_label.setText(f"Hora de salida registrada para {trabajador}")

# --- Función para validar usuario y contraseña ---
def validar_usuario(trabajador, contraseña):
    usuarios = {
        "Monica Dental": "monicadental20",
        "Dalia Dental": "daliadental21",
        "Alejandro Dental": "alexdental22",
        "Adriana Dental": "adrianadental23",
        "Jessica Dental": "jessicadental24",
        "Tere Dental": "teredental25"
    }
    if trabajador in usuarios and usuarios[trabajador] == contraseña:
        return True
    return False

# --- Función para ver los registros ---
def ver_registros():
    try:
        conn = sqlite3.connect("registros.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM registros ORDER BY trabajador, fecha, hora''')
        registros = cursor.fetchall()
        conn.close()

        # Organizar los registros por trabajador
        registros_por_usuario = {}
        for registro in registros:
            trabajador = registro[1]
            if trabajador not in registros_por_usuario:
                registros_por_usuario[trabajador] = []
            registros_por_usuario[trabajador].append(f"{registro[2]}: {registro[3]} {registro[4]}")

        # Crear un texto organizado con las entradas por trabajador
        registros_organizados = ""
        for trabajador, registros_trabajador in registros_por_usuario.items():
            registros_organizados += f"<b style='color:#2e8b57;'>{trabajador}</b><br>"  # Nombre en verde
            for registro in registros_trabajador:
                registros_organizados += f"<p style='margin-left:20px;color:#333;'>{registro}</p>"  # Entradas en gris
            registros_organizados += "<hr style='border: 0; border-top: 1px solid #ddd;'>"

        registros_window.setText(registros_organizados)

    except FileNotFoundError:
        registros_window.setText("No se han encontrado registros.")

# --- Crear la interfaz gráfica ---
app = QApplication(sys.argv)

# Crear ventana principal
window = QWidget()
window.setWindowTitle("Registro de Entrada y Salida")
window.setWindowIcon(QIcon("favicon.ico"))

# Estilos embebidos en el código (interfaz con fuente nativa de Apple)
app.setStyleSheet("""
    QWidget {
        font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
        font-size: 14px;
        background-color: #ffffff;  /* Fondo blanco */
    }
    QLabel {
        color: #333;
        font-size: 16px;
    }
    QLineEdit {
        padding: 12px;
        margin: 5px 0;
        border: 2px solid #2c3e50;  /* Azul marino */
        border-radius: 6px;
        background-color: #ffffff;
        color: #333;  /* Color del texto */
        font-size: 16px;
    }
    QLineEdit:focus {
        border-color: #16a085;  /* Verde menta al enfocar */
        border-width: 3px;  /* Aumentar grosor para destacar */
    }
    QPushButton {
        background-color: #2c3e50;  /* Azul marino */
        color: white;
        border-radius: 6px;
        padding: 12px 20px;
        font-size: 16px;
    }
    QPushButton:hover {
        background-color: #34495e;  /* Azul más oscuro */
    }
    #btn_entrada {
        background-color: #2980b9;  /* Azul más brillante */
    }
    #btn_entrada:hover {
        background-color: #3498db;
    }
    #btn_salida {
        background-color: #e74c3c;  /* Rojo suave */
    }
    #btn_salida:hover {
        background-color: #c0392b;
    }
    #btn_ver_registros {
        background-color: #16a085;  /* Verde menta */
    }
    #btn_ver_registros:hover {
        background-color: #1abc9c;
    }
    #lbl_error {
        color: red;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        text-align: center;
    }
    QTextEdit {
        border: 1px solid #2c3e50;  /* Azul marino */
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 6px;
        font-size: 14px;
        color: #333;
    }
    QTextEdit:focus {
        border-color: #16a085;
    }
    QScrollArea {
        margin-top: 20px;
        border-radius: 6px;
    }
    QScrollBar {
        background: #f1f1f1;
        border-radius: 6px;
    }
    QScrollBar::handle {
        background: #2980b9;
        border-radius: 6px;
    }
""")

# Etiquetas para los campos de entrada
label_trabajador = QLabel("Empleado:")
label_contraseña = QLabel("Contraseña:")

# Layouts
layout = QVBoxLayout()
form_layout = QFormLayout()

# Crear elementos de la interfaz
input_trabajador = QLineEdit()
input_trabajador.setPlaceholderText("Ingresa el nombre del empleado")
input_contraseña = QLineEdit()
input_contraseña.setEchoMode(QLineEdit.Password)
input_contraseña.setPlaceholderText("Ingresa la contraseña")

# Botones de acción
btn_entrada = QPushButton("Registrar Entrada")
btn_entrada.setObjectName("btn_entrada")
btn_entrada.clicked.connect(registrar_entrada)

btn_salida = QPushButton("Registrar Salida")
btn_salida.setObjectName("btn_salida")
btn_salida.clicked.connect(registrar_salida)

btn_ver_registros = QPushButton("Ver Registros")
btn_ver_registros.setObjectName("btn_ver_registros")
btn_ver_registros.clicked.connect(ver_registros)

# Etiqueta de errores o mensajes
error_label = QLabel("")
error_label.setObjectName("lbl_error")
error_label.setAlignment(Qt.AlignCenter)

# Crear caja de texto para mostrar los registros
registros_window = QLabel("")
registros_window.setAlignment(Qt.AlignLeft)
registros_window.setStyleSheet("font-size: 14px; color: #333; background-color: #f8f9fa; border: 1px solid #ccc; padding: 10px;")

# Crear el Dashboard para mostrar las horas
dashboard_layout = QVBoxLayout()

# Títulos para los cuadros de entrada y salida
titulo_entrada = QLabel("<b>Entradas Registradas</b>")
dashboard_entrada = QTextEdit()
dashboard_entrada.setObjectName("dashboard_entrada")
dashboard_entrada.setReadOnly(True)
dashboard_entrada.setPlaceholderText("Aquí aparecerán las entradas registradas.")

titulo_salida = QLabel("<b>Salidas Registradas</b>")
dashboard_salida = QTextEdit()
dashboard_salida.setObjectName("dashboard_salida")
dashboard_salida.setReadOnly(True)
dashboard_salida.setPlaceholderText("Aquí aparecerán las salidas registradas.")

# Agregar los elementos al layout
dashboard_layout.addWidget(titulo_entrada)
dashboard_layout.addWidget(dashboard_entrada)
dashboard_layout.addWidget(titulo_salida)
dashboard_layout.addWidget(dashboard_salida)

# Scroll area para los registros
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setWidget(registros_window)

# Agregar los elementos al layout
form_layout.addRow(label_trabajador, input_trabajador)
form_layout.addRow(label_contraseña, input_contraseña)

layout.addLayout(form_layout)
layout.addWidget(btn_entrada)
layout.addWidget(btn_salida)
layout.addWidget(btn_ver_registros)
layout.addWidget(error_label)
layout.addWidget(scroll_area)
layout.addLayout(dashboard_layout)

# Establecer el layout en la ventana principal
window.setLayout(layout)

# Permitir que la ventana se redimensione
window.setMinimumSize(500, 700)

# Inicializar la base de datos
inicializar_bd()

# Cargar la clave de cifrado
clave = cargar_clave()

# Mostrar la ventana
window.show()

# Ejecutar la aplicación
sys.exit(app.exec_())
