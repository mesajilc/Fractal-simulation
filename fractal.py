import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

A1=np.array([[0,0],[0,0.16]])
A2=np.array([[0.85,0.04],[-0.04,0.85]])
A3=np.array([[0.2,-0.26],[0.23,0.22]])
A4=np.array([[-0.15,0.28],[0.26,0.24]])
b1=np.array([[0],[0]])
b2=np.array([[0],[1.6]])
b3=np.array([[0],[1.6]])
b4=np.array([[0],[0.44]])
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
        puntosx,puntosy=self.probabilidad()
        #x = np.random.rand(n)
        #y = np.random.rand(n)
        self.ax.scatter(puntosx, puntosy, c='blue')
        self.canvas.draw()

    def change_drawing(self):
        n = self.slider.value()
        self.update_plot(n)

        
    def S1(self,vector):
        return A[0]@vector+b[0]
    def S2(self,vector):
        return A[1]@vector+b[1]
    def S3(self,vector):
        return A[2]@vector+b[2]
    def S4(self,vector):
        return A[3]@vector+b[3]
    S=[S1,S2,S3,S4]

    def probabilidad(self):
        # Definir los valores discretos y sus probabilidades asociadas
        valores = [1, 2, 3, 4]
        probabilidades = [0.01, 0.85, 0.07, 0.07]

        # Verificar que las probabilidades sumen 1
        assert np.isclose(np.sum(probabilidades), 1), "Las probabilidades deben sumar 1."

        # Generar muestras aleatorias basadas en la distribución discreta
        n_muestras = 100000  # Número de muestras a generar
        muestras = np.random.choice(valores, size=n_muestras, p=probabilidades)
        puntosx=[]
        puntosy=[]
        for i in range(0,n_muestras):
            xx=self.S[muestras[i]-1](x)
            puntosx.append(xx[0])
            puntosy.append(xx[1])
        return puntosx,puntosy

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
