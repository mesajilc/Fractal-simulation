import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Definir las matrices de transformación y los vectores
A1 = np.array([[0, 0], [0, 0.16]])
A2 = np.array([[0.85, 0.04], [-0.04, 0.85]])
A3 = np.array([[0.2, -0.26], [0.23, 0.22]])
A4 = np.array([[-0.15, 0.28], [0.26, 0.24]])

b1 = np.array([[0], [0]])
b2 = np.array([[0], [1.6]])
b3 = np.array([[0], [1.6]])
b4 = np.array([[0], [0.44]])

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

        # Slider para modificar la cantidad de puntos
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(1000)
        self.slider.valueChanged.connect(self.update_plot)
        layout.addWidget(self.slider)

        # Botón para cambiar el dibujo
        self.button = QPushButton("Cambiar Dibujo")
        self.button.clicked.connect(self.change_drawing)
        layout.addWidget(self.button)

        # Contenedor de la ventana principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Inicializar gráfico
        self.update_plot(10)

    def update_plot(self, value):
        n = int(value)
        self.ax.clear()
        puntosx, puntosy = self.probabilidad(n)
        self.ax.scatter(puntosx, puntosy, c='blue', s=0.1)
        self.canvas.draw()

    def change_drawing(self):
        n = self.slider.value()
        self.update_plot(n)

    # Funciones de transformación
    def S1(self, vector):
        return A1 @ vector + b1

    def S2(self, vector):
        return A2 @ vector + b2

    def S3(self, vector):
        return A3 @ vector + b3

    def S4(self, vector):
        return A4 @ vector + b4

    # Definir las funciones de transformación
    S = [S1, S2, S3, S4]

    def probabilidad(self, n_muestras):
        # Valores y probabilidades
        valores = [1, 2, 3, 4]
        probabilidades = [0.01, 0.85, 0.07, 0.07]

        # Verificar que las probabilidades sumen 1
        assert np.isclose(np.sum(probabilidades), 1), "Las probabilidades deben sumar 1."

        # Punto inicial
        x = np.array([[0], [0]])

        # Generar muestras aleatorias
        muestras = np.random.choice(valores, size=n_muestras, p=probabilidades)
        puntosx = []
        puntosy = []

        # Generar los puntos
        for i in range(n_muestras):
            transformacion = self.S[muestras[i] - 1](self, x)
            x = transformacion
            puntosx.append(x[0, 0])
            puntosy.append(x[1, 0])

        return puntosx, puntosy

# Ejecutar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
