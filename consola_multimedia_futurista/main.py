import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from sistema import PanelSistema
from visualizador import VisualizadorAudio
from efectos import aplicar_eco, aplicar_reverb, aplicar_pitch, aplicar_filtro_bajo

class ConsolaMultimedia(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎧 Consola Multimedia Futurista")
        self.setGeometry(100, 100, 900, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tema_combo = QComboBox()
        self.tema_combo.addItems([
            "tema_neonazul.css", "tema_matrixverde.css", "tema_terminal.css",
            "tema_oceanoprofundo.css", "tema_calidoretro.css",
            "tema_grafito_moderno.css", "tema_claro_minimalista.css",
            "tema_modo_hacker.css"
        ])
        self.tema_combo.currentTextChanged.connect(self.cargar_tema)
        self.layout.addWidget(QLabel("🎨 Selecciona un tema visual:"))
        self.layout.addWidget(self.tema_combo)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Panel de Sistema
        self.tabs.addTab(PanelSistema(), "🖥️ Sistema")

        # Visualizador
        self.visualizador = VisualizadorAudio()
        self.tabs.addTab(self.visualizador, "🎛️ Visualizador")

        # Panel de efectos
        self.efectos_widget = QWidget()
        efectos_layout = QVBoxLayout()
        self.efectos_widget.setLayout(efectos_layout)

        btn_eco = QPushButton("🎵 Aplicar Eco")
        btn_eco.clicked.connect(lambda: aplicar_eco("audio.wav"))
        btn_reverb = QPushButton("🌊 Reverb")
        btn_reverb.clicked.connect(lambda: aplicar_reverb("audio.wav"))
        btn_pitch = QPushButton("🎚️ Cambiar Pitch")
        btn_pitch.clicked.connect(lambda: aplicar_pitch("audio.wav"))
        btn_filtro = QPushButton("🔈 Filtro Bajo")
        btn_filtro.clicked.connect(lambda: aplicar_filtro_bajo("audio.wav"))

        for b in [btn_eco, btn_reverb, btn_pitch, btn_filtro]:
            efectos_layout.addWidget(b)

        self.tabs.addTab(self.efectos_widget, "🎶 Efectos")

        # Cargar el tema inicial
        self.cargar_tema(self.tema_combo.currentText())

    def cargar_tema(self, nombre_archivo):
        try:
            with open(f"estilos/{nombre_archivo}", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("No se pudo cargar el tema:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ConsolaMultimedia()
    ventana.show()
    sys.exit(app.exec_())
