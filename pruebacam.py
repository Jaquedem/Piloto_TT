import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk

class CamaraApp:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Monitor de Cámara USB - RPi 4")
        
        # Abrir la fuente de video (0 suele ser la primera cámara USB)
        self.vid = cv2.VideoCapture(video_source)
        
        if not self.vid.isOpened():
            raise ValueError("No se pudo abrir la cámara de video")

        # Obtener dimensiones del video
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Crear un canvas (Label) donde se mostrará la imagen
        self.video_label = Label(window)
        self.video_label.pack(padx=10, pady=10)

        # Botón para salir (buenas prácticas: permitir cierre limpio)
        self.btn_quit = Button(window, text="Cerrar Sistema", width=20, command=self.close_app, bg="#ffdddd")
        self.btn_quit.pack(pady=5)

        # Iniciar el bucle de actualización del video
        self.delay = 15 # Milisegundos entre frames
        self.update()

        self.window.mainloop()

    def update(self):
        # Obtener un frame de la fuente de video
        ret, frame = self.vid.read()

        if ret:
            # OpenCV usa BGR, Tkinter/PIL usa RGB. Hay que convertirlo.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convertir el array de imagen a objeto de imagen PIL
            image = Image.fromarray(frame_rgb)
            
            # Convertir a formato compatible con Tkinter
            photo = ImageTk.PhotoImage(image=image)
            
            # Actualizar el label con la nueva imagen
            self.video_label.configure(image=photo)
            self.video_label.image = photo # Mantener una referencia para evitar el Garbage Collector

        # Llamarse a sí misma después de 'delay' ms
        self.window.after(self.delay, self.update)

    def close_app(self):
        # Liberar recurso de cámara y cerrar ventana
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

# Ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    app = CamaraApp(root)
    