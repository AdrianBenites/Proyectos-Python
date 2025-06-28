import psutil
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

class PanelSistema(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.cpu_label = QLabel("CPU: Cargando...")
        self.ram_label = QLabel("RAM: Cargando...")
        self.usuario_label = QLabel("Usuario: Cargando...")
        self.uptime_label = QLabel("Tiempo encendido: Cargando...")

        for label in [self.cpu_label, self.ram_label, self.usuario_label, self.uptime_label]:
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(1000)
        self.actualizar()

    def actualizar(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        usuario = psutil.users()[0].name if psutil.users() else "Desconocido"
        uptime = int(psutil.boot_time())
        from datetime import datetime
        encendido = datetime.now().timestamp() - uptime
        horas = int(encendido // 3600)
        minutos = int((encendido % 3600) // 60)

        self.cpu_label.setText(f"🖥️ CPU en uso: {cpu}%")
        self.ram_label.setText(f"📦 RAM en uso: {ram}%")
        self.usuario_label.setText(f"👤 Usuario: {usuario}")
        self.uptime_label.setText(f"⏱️ Tiempo encendido: {horas}h {minutos}min")
