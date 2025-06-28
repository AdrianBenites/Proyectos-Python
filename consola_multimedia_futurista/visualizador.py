from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import random
import math

class VisualizadorAudio(QWidget):
    def __init__(self, modo="lineal"):
        super().__init__()
        self.modo = modo
        self.setMinimumHeight(200)
        self.setStyleSheet("background-color: #000000;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Actualiza cada 100 ms

        layout = QVBoxLayout(self)
        self.selector = QComboBox()
        self.selector.addItems(["lineal", "ondas", "pulsos", "espectro", "radial", "digital"])
        self.selector.currentTextChanged.connect(self.cambiar_modo)
        layout.addWidget(self.selector)
        layout.setContentsMargins(0, 0, 0, 0)

    def cambiar_modo(self, nuevo_modo):
        self.modo = nuevo_modo
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        ancho = self.width()
        alto = self.height()

        if self.modo == "lineal":
            for i in range(0, ancho, 15):
                h = random.randint(10, alto // 2)
                painter.fillRect(i, alto // 2 - h, 10, h * 2, QColor(0, 255, 255))

        elif self.modo == "ondas":
            pen = QPen(QColor(0, 255, 0), 2)
            painter.setPen(pen)
            for i in range(ancho):
                y = int(alto / 2 + 30 * math.sin(i * 0.05 + random.random()))
                painter.drawPoint(i, y)

        elif self.modo == "pulsos":
            radio = random.randint(20, 80)
            centro = (ancho // 2, alto // 2)
            color = QColor(255, 0, 100, 150)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(centro[0] - radio, centro[1] - radio, radio * 2, radio * 2)

        elif self.modo == "espectro":
            for i in range(0, ancho, 20):
                h = random.randint(20, alto)
                color = QColor(255, 255, 0)
                painter.fillRect(i, alto - h, 15, h, color)

        elif self.modo == "radial":
            centro = (ancho // 2, alto // 2)
            for angle in range(0, 360, 20):
                length = random.randint(30, 100)
                rad = math.radians(angle)
                x = centro[0] + math.cos(rad) * length
                y = centro[1] + math.sin(rad) * length
                pen = QPen(QColor(0, 200, 255), 2)
                painter.setPen(pen)
                painter.drawLine(centro[0], centro[1], int(x), int(y))

        elif self.modo == "digital":
            painter.setPen(QColor(0, 255, 0))
            font_size = 18
            for i in range(50):
                x = random.randint(0, ancho)
                y = random.randint(0, alto)
                char = random.choice("01")
                painter.drawText(x, y, char)

