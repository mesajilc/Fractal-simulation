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

        # Slider para modificar la cantidad de puntos
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(50000)
        self.slider.setTickInterval(5000)  # Hace que el slider se mueva en pasos de 5000
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
        self.precomputed_points = {}  # Memoria dinámica para almacenar puntos precomputados
        self.max_points = 0  # Máximo número de puntos calculados hasta ahora
        self.update_plot(10)

    def update_plot(self, value):
        n = int(value)
        
        # Si ya tenemos más puntos precomputados que 'n', no recalcular
        if self.current_prob not in self.precomputed_points or self.max_points < n:
            self.precompute_points(n)

        self.ax.clear()

        # Obtener los puntos precomputados
        puntosx, puntosy = self.precomputed_points[self.current_prob]

        # Dibujar los puntos hasta 'n' muestras
        self.ax.scatter(puntosx[:n], puntosy[:n], c='blue', s=1)
        self.canvas.draw()

    def precompute_points(self, n):
        # Decide qué función de probabilidad usar
        if self.current_prob == 0:
            puntosx, puntosy = self.probabilidad(n)
        elif self.current_prob == 1:
            puntosx, puntosy = self.probabilidad2(n)
        elif self.current_prob == 2:
            puntosx, puntosy = self.probabilidad3(n)
        elif self.current_prob == 3:
            puntosx, puntosy = self.probabilidad4(n)
        else:
            puntosx, puntosy = self.probabilidad5(n)

        # Guardar los puntos precomputados
        self.precomputed_points[self.current_prob] = (puntosx, puntosy)
        self.max_points = n

    def toggle_probabilidad(self):
        # Alterna entre las tres funciones de probabilidad
        self.current_prob = (self.current_prob + 1) % 5
        self.update_plot(self.slider.value())

    def probabilidad(self, n_muestras):
        A1 = np.array([[0, 0], [0, 0.16]])
        A2 = np.array([[0.85, 0.04], [-0.04, 0.85]])
        A3 = np.array([[0.2, -0.26], [0.23, 0.22]])
        A4 = np.array([[-0.15, 0.28], [0.26, 0.24]])

        b1 = np.array([[0], [0]])
        b2 = np.array([[0], [1.6]])
        b3 = np.array([[0], [1.6]])
        b4 = np.array([[0], [0.44]])

        # Funciones de transformación
        def S1(self, vector):
            return A1 @ vector + b1

        def S2(self, vector):
            return A2 @ vector + b2

        def S3(self, vector):
            return A3 @ vector + b3

        def S4(self, vector):
            return A4 @ vector + b4

        self.S = [S1, S2, S3, S4]

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

    def probabilidad2(self, n_muestras):
        A0 = np.array([[0.4000, -0.3733], [0.0600, 0.6000]])
        b0 = np.array([[0.3533], [0.0000]])

        A1 = np.array([[-0.8000, -0.1867], [0.1371, 0.8000]])
        b1 = np.array([[1.1000], [0.1000]])

        def S0(self, vector):
            return A0 @ vector + b0

        def S1(self, vector):
            return A1 @ vector + b1

        self.S = [S0, S1]

        valores = [0, 1]
        probabilidades = [0.2993, 0.7007]

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
            transformacion = self.S[muestras[i]](self, x)
            x = transformacion
            puntosx.append(x[0, 0])
            puntosy.append(x[1, 0])

        return puntosx, puntosy

    def probabilidad3(self, n_muestras):
        A1 = np.array([[0.5, -0.5], [0.5, 0.5]])
        A2 = np.array([[-0.5, -0.5], [0.5, -0.5]])

        b1 = np.array([[0], [0]])
        b2 = np.array([[1], [0]])
        
        # Funciones de transformación
        def S1(self, vector):
            return A1 @ vector + b1

        def S2(self, vector):
            return A2 @ vector + b2

        self.S = [S1, S2]

        valores = [1, 2]
        probabilidades = [0.5, 0.5]

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

    def probabilidad4(self, n_muestras):
        c = 0.255
        r = 0.75
        q = 0.625
        φ = -np.pi / 8
        ψ = np.pi / 5
        
        A1 = np.array([[0, 0], [0, c]])
        A2 = np.array([[r * np.cos(φ), -r * np.sin(φ)], [r * np.sin(φ), r * np.cos(φ)]])
        A3 = np.array([[q * np.cos(ψ), -r * np.sin(ψ)], [q * np.sin(ψ), r * np.cos(ψ)]])  # Corregido
        
        b1 = np.array([[0.5], [0]])
        b2 = np.array([[0.5 - r * np.cos(φ) / 2], [c - r * np.sin(φ) / 2]])
        b3 = np.array([[0.5 - q * np.cos(ψ) / 2], [(3 * c / 5) - q * np.sin(ψ) / 2]])

        # Funciones de transformación
        def S1(self, vector):
            return A1 @ vector + b1

        def S2(self, vector):
            return A2 @ vector + b2

        def S3(self, vector):
            return A3 @ vector + b3

        self.S = [S1, S2, S3]

        valores = [1, 2, 3]
        probabilidades = [1 / 3, 1 / 3, 1 / 3]

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
   
    def probabilidad5(self, n_muestras):
        
        
        A1 = np.array([[0.5, 0], [0, 0.5]])
        A2 = np.array([[0.5, 0], [0, 0.5]])
        A3 = np.array([[0.5, 0], [0, 0.5]])  # Corregido
        
        b1 = np.array([[0], [0]])
        b2 = np.array([[0.5], [0]])
        b3 = np.array([[1/4], [np.sqrt(3)/4]])

        # Funciones de transformación
        def S1(self, vector):
            return A1 @ vector + b1

        def S2(self, vector):
            return A2 @ vector + b2

        def S3(self, vector):
            return A3 @ vector + b3

        self.S = [S1, S2, S3]

        valores = [1, 2, 3]
        probabilidades = [1 / 3, 1 / 3, 1 / 3]

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
