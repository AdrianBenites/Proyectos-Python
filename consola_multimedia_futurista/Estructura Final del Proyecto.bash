consola_multimedia_futurista/
├── main.py                  # Archivo principal (lo que ejecutas)
├── efectos.py               # Efectos de audio (eco, reverb, etc.)
├── sistema.py               # Info del sistema (RAM, CPU, etc.)
├── visualizador.py          # Visualizadores animados (6 modos)
├── estilos/                 # Temas CSS (8 archivos)
│   ├── tema_neonazul.css
│   ├── tema_matrixverde.css
│   ├── ...
├── requirements.txt         # Paquetes necesarios
├── README.md                # Documentación
└── assets/ (opcional)       # Íconos animados, logos, etc.

pip install pyinstaller

pyinstaller --onefile --windowed main.py
