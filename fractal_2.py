import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Clase principal de la ventana
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dibujar Puntos")

        # Layout principal
        layout = QVBoxLayout()

        # Gráfico de Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Slider para modificar la cantidad de puntos, en pasos de 100
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(10000)
        self.slider.setTickInterval(100)  # Hace que el slider se mueva en pasos de 100
        self.slider.setSingleStep(100)
        self.slider.valueChanged.connect(self.update_plot)
        layout.addWidget(self.slider)

        # Botón para cambiar el dibujo
        self.button = QPushButton("Cambiar Dibujo")
        self.button.clicked.connect(self.toggle_probabilidad)
        layout.addWidget(self.button)

        # Contenedor de la ventana principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Inicializar gráfico y modo de probabilidad
        self.current_prob = 0  # Comienza con probabilidad 1

        # Precalcular puntos
        self.puntos_max = 10000
        self.precalculate_points()

        # Inicializar el gráfico con 10 puntos
        self.update_plot(10)

    def precalculate_points(self):
        """ Precalcula los puntos de ambas distribuciones para evitar recalcular constantemente """
        self.puntosx1, self.puntosy1 = self.probabilidad(self.puntos_max)
        self.puntosx2, self.puntosy2 = self.probabilidad2(self.puntos_max)

    def update_plot(self, value):
        """ Actualiza el gráfico usando los primeros 'value' puntos precalculados """
        n = int(value)
        self.ax.clear()

        # Decide qué puntos mostrar basándose en la distribución activa
        if self.current_prob == 0:
            puntosx, puntosy = self.puntosx1[:n], self.puntosy1[:n]
        else:
            puntosx, puntosy = self.puntosx2[:n], self.puntosy2[:n]

        self.ax.scatter(puntosx, puntosy, c='blue', s=1)
        self.canvas.draw()

    def toggle_probabilidad(self):
        """ Cambia entre las dos funciones de probabilidad """
        self.current_prob = 1 - self.current_prob  # Alterna entre 0 y 1
        self.update_plot(self.slider.value())

    def probabilidad(self, n_muestras):
        """ Genera puntos para la primera distribución """
        A1 = np.array([[0, 0], [0, 0.16]])
        A2 = np.array([[0.85, 0.04], [-0.04, 0.85]])
        A3 = np.array([[0.2, -0.26], [0.23, 0.22]])
        A4 = np.array([[-0.15, 0.28], [0.26, 0.24]])

        b1 = np.array([[0], [0]])
        b2 = np.array([[0], [1.6]])
        b3 = np.array([[0], [1.6]])
        b4 = np.array([[0], [0.44]])

        def S1(vector):
            return A1 @ vector + b1

        def S2(vector):
            return A2 @ vector + b2

        def S3(vector):
            return A3 @ vector + b3

        def S4(vector):
            return A4 @ vector + b4

        S = [S1, S2, S3, S4]

        valores = [1, 2, 3, 4]
        probabilidades = [0.01, 0.85, 0.07, 0.07]

        x = np.array([[0], [0]])
        muestras = np.random.choice(valores, size=n_muestras, p=probabilidades)
        puntosx, puntosy = [], []

        for i in range(n_muestras):
            transformacion = S[muestras[i] - 1](x)
            x = transformacion
            puntosx.append(x[0, 0])
            puntosy.append(x[1, 0])

        return puntosx, puntosy

    def probabilidad2(self, n_muestras):
        """ Genera puntos para la segunda distribución """
        A0 = np.array([[0.4000, -0.3733], [0.0600, 0.6000]])
        b0 = np.array([[0.3533], [0.0000]])

        A1 = np.array([[-0.8000, -0.1867], [0.1371, 0.8000]])
        b1 = np.array([[1.1000], [0.1000]])

        def S0(vector):
            return A0 @ vector + b0

        def S1(vector):
            return A1 @ vector + b1

        S = [S0, S1]

        valores = [0, 1]
        probabilidades = [0.2993, 0.7007]

        x = np.array([[0], [0]])
        muestras = np.random.choice(valores, size=n_muestras, p=probabilidades)
        puntosx, puntosy = [], []

        for i in range(n_muestras):
            transformacion = S[muestras[i]](x)
            x = transformacion
            puntosx.append(x[0, 0])
            puntosy.append(x[1, 0])

        return puntosx, puntosy

# Ejecutar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
