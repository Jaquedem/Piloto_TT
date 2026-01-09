import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from src.logic import SignLanguageInterpreter

class InterpretIA_App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("InterpretIA - LSM")
        self.geometry("1000x700")
        ctk.set_appearance_mode("Dark") # Tema oscuro profesional
        
        # Variables de control
        self.model = YOLO("models/best.pt") # Cargar tu modelo
        self.interpreter = SignLanguageInterpreter()
        self.cap = None
        self.is_running = False

        # Iniciar con pantalla de bienvenida
        self.show_splash_screen()

    def show_splash_screen(self):
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()

        self.splash_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.splash_frame.pack(expand=True)

        label_title = ctk.CTkLabel(
            self.splash_frame, 
            text="Bienvenid@ a\nInterpretIA", 
            font=("Roboto", 40, "bold"),
            text_color="#3B8ED0" # Azul bonito
        )
        label_title.pack(pady=20)

        label_subtitle = ctk.CTkLabel(
            self.splash_frame, 
            text="Detectora de señas de la\nLengua de Señas Mexicana", 
            font=("Roboto", 20)
        )
        label_subtitle.pack(pady=10)

        # Transición automática a los 3 segundos (3000 ms)
        self.after(3000, self.setup_main_interface)

    def setup_main_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        # --- DISEÑO PRINCIPAL (Grid) ---
        self.grid_columnconfigure(0, weight=3) # Columna video (más ancha)
        self.grid_columnconfigure(1, weight=1) # Columna botones
        self.grid_rowconfigure(0, weight=1)

        # 1. Área de Video (Izquierda)
        self.video_frame = ctk.CTkFrame(self, fg_color="#1F1F1F")
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Label donde se pintará la imagen de la cámara
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 2. Despliegue de Texto (Overlay arriba del video o abajo)
        # Lo pondremos abajo del video para que sea legible
        self.text_display = ctk.CTkLabel(
            self.video_frame,
            text="Esperando señas...",
            font=("Arial", 24, "bold"),
            fg_color="#2B2B2B",
            corner_radius=10,
            height=60
        )
        self.text_display.pack(fill="x", padx=20, pady=20)

        # 3. Panel Lateral (Derecha)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ns")

        # Botón INICIO (Verde, redondeado)
        self.btn_start = ctk.CTkButton(
            self.sidebar,
            text="INICIAR\nDETECCIÓN",
            font=("Roboto", 16, "bold"),
            fg_color="#2CC985", # Verde
            hover_color="#209160",
            corner_radius=30, # ¡Aquí hacemos que no sea cuadrado!
            height=80,
            command=self.start_detection
        )
        self.btn_start.pack(pady=(50, 20), padx=20, fill="x")

        # Botón DETENER (Rojo, redondeado)
        self.btn_stop = ctk.CTkButton(
            self.sidebar,
            text="DETENER",
            font=("Roboto", 16, "bold"),
            fg_color="#C92C38", # Rojo
            hover_color="#912028",
            corner_radius=30,
            height=60,
            command=self.stop_detection,
            state="disabled"
        )
        self.btn_stop.pack(pady=10, padx=20, fill="x")

        # Botón SALIR (Gris)
        self.btn_exit = ctk.CTkButton(
            self.sidebar,
            text="SALIR",
            fg_color="#555555",
            command=self.show_goodbye_screen
        )
        self.btn_exit.pack(side="bottom", pady=40, padx=20)

    def start_detection(self):
        self.is_running = True
        self.btn_start.configure(state="disabled", fg_color="#555555")
        self.btn_stop.configure(state="normal", fg_color="#C92C38")
        
        self.cap = cv2.VideoCapture(0) # 0 es la webcam por defecto
        self.update_camera()

    def stop_detection(self):
        self.is_running = False
        self.btn_start.configure(state="normal", fg_color="#2CC985")
        self.btn_stop.configure(state="disabled", fg_color="#555555")
        
        if self.cap:
            self.cap.release()
        self.video_label.configure(image=None) # Limpiar imagen
        self.interpreter.clear() # Limpiar texto

    def update_camera(self):
        if self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # 1. Inferencia YOLO
                results = self.model(frame, verbose=False, conf=0.6)
                annotated_frame = results[0].plot()

                # 2. Lógica de Texto
                # Buscamos si detectó algo con alta confianza
                detected_text = ""
                if results[0].boxes:
                    # Tomamos la clase con mayor confianza
                    box = results[0].boxes[0]
                    class_id = int(box.cls)
                    label_name = self.model.names[class_id]
                    
                    # Procesamos con nuestra lógica de oraciones
                    sentence = self.interpreter.process_detection(label_name)
                    self.text_display.configure(text=sentence)

                # 3. Convertir imagen para Tkinter (BGR -> RGB)
                img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                # Redimensionar para ajustar al frame si es necesario
                img_tk = ImageTk.PhotoImage(image=img)

                self.video_label.configure(image=img_tk)
                self.video_label.image = img_tk

            # Llamarse a sí misma en 10ms (Loop)
            self.after(10, self.update_camera)

    def show_goodbye_screen(self):
        self.stop_detection()
        for widget in self.winfo_children():
            widget.destroy()

        label_bye = ctk.CTkLabel(
            self, 
            text="¡Gracias por usar\nInterpretIA!", 
            font=("Roboto", 40, "bold"),
            text_color="#2CC985"
        )
        label_bye.pack(expand=True)
        
        # Cerrar app después de 3 segundos
        self.after(3000, self.destroy)