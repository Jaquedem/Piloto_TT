import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import os # Importante para encontrar la ruta del logo
from ultralytics import YOLO
from src.logic import SignLanguageInterpreter

class InterpretIA_App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("InterpretIA - LSM")
        self.geometry("1000x700")
        ctk.set_appearance_mode("Dark") # Tema oscuro profesional
        
        # --- COLORES DE IDENTIDAD ---
        self.color_fondo_logo = "#D0B3E9" # El lila claro del fondo de tu imagen
        self.color_texto_contraste = "#2E003E" # Morado oscuro para que se lea bien
        
        # Variables de control IA
        self.model = YOLO("models/best.pt") # Cargar tu modelo
        self.interpreter = SignLanguageInterpreter()
        self.cap = None
        self.is_running = False

        # Variables de Optimización (Estrategia 3: Frame Skipping)
        self.frame_count = 0
        self.last_annotated_frame = None

        # Cargar la imagen del logo una sola vez
        self.logo_image = self.load_logo_image()

        # Iniciar con pantalla de bienvenida
        self.show_splash_screen()

    def load_logo_image(self):
        # Busca el logo en la carpeta src
        logo_path = os.path.join("src", "Logo.png")
        try:
            pil_img = Image.open(logo_path)
            # Ajustamos el tamaño para que se vea bien (aprox. 60% del ancho)
            target_width = 600
            w, h = pil_img.size
            aspect_ratio = h / w
            target_height = int(target_width * aspect_ratio)
            
            # Creamos la imagen CTk optimizada
            logo = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(target_width, target_height))
            print("✅ Logo cargado correctamente.")
            return logo
        except Exception as e:
            print(f"❌ Error al cargar el logo en '{logo_path}': {e}")
            return None

    def show_splash_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Usamos el color del fondo del logo para toda la pantalla
        self.splash_frame = ctk.CTkFrame(self, fg_color=self.color_fondo_logo)
        self.splash_frame.pack(expand=True, fill="both")

        # Contenedor para centrar verticalmente
        center_box = ctk.CTkFrame(self.splash_frame, fg_color="transparent")
        center_box.pack(expand=True)

        # 1. Texto "Bienvenid@ a"
        label_welcome = ctk.CTkLabel(
            center_box, 
            text="Bienvenid@ a", 
            font=("Roboto", 32, "bold"),
            text_color=self.color_texto_contraste
        )
        label_welcome.pack(pady=(0, 20))

        # 2. El LOGO
        if self.logo_image:
            label_logo = ctk.CTkLabel(center_box, text="", image=self.logo_image)
            label_logo.pack(pady=10)
        else:
            # Fallback por si no encuentra la imagen
            label_logo = ctk.CTkLabel(center_box, text="InterpretIA", font=("Roboto", 50, "bold"), text_color=self.color_texto_contraste)
            label_logo.pack(pady=10)

        # 3. Subtítulo con saltos de línea
        label_subtitle = ctk.CTkLabel(
            center_box, 
            text="\nDetectora de señas de la\nLengua de Señas Mexicana", 
            font=("Roboto", 22),
            text_color=self.color_texto_contraste
        )
        label_subtitle.pack(pady=(20, 0))

        # Transición a los 4.5 segundos
        self.after(4500, self.setup_main_interface)

    def setup_main_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        # --- DISEÑO PRINCIPAL (Grid) ---
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Área de Video (Izquierda)
        self.video_frame = ctk.CTkFrame(self, fg_color="#644287") # Tu fondo lila oscuro
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 2. Despliegue de Texto
        self.text_display = ctk.CTkLabel(
            self.video_frame,
            text="Esperando señas...",
            font=("Arial", 24, "bold"),
            fg_color="#290B44", # Tu fondo morado oscuro
            text_color="#CD9EF7", # Tu texto lila claro
            corner_radius=10,
            height=60
        )
        self.text_display.pack(fill="x", padx=20, pady=20)

        # 3. Panel Lateral (Derecha)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ns")

        # Botones
        self.btn_start = ctk.CTkButton(self.sidebar, text="INICIAR\nDETECCIÓN", font=("Roboto", 16, "bold"), fg_color="#B72CC9", hover_color="#6D2091", corner_radius=30, height=80, command=self.start_detection)
        self.btn_start.pack(pady=(50, 20), padx=20, fill="x")

        self.btn_stop = ctk.CTkButton(self.sidebar, text="DETENER", font=("Roboto", 16, "bold"), fg_color="#C92C38", hover_color="#912028", corner_radius=30, height=60, command=self.stop_detection, state="disabled")
        self.btn_stop.pack(pady=10, padx=20, fill="x")

        self.btn_exit = ctk.CTkButton(self.sidebar, text="SALIR", fg_color="#7F7283", command=self.show_goodbye_screen)
        self.btn_exit.pack(side="bottom", pady=40, padx=20)

    # --- Funciones de la cámara (start, stop, update) IGUALES que antes ---
    def start_detection(self):
        self.is_running = True
        self.btn_start.configure(state="disabled", fg_color="#555555")
        self.btn_stop.configure(state="normal", fg_color="#C92C38")
        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def stop_detection(self):
        self.is_running = False
        self.btn_start.configure(state="normal", fg_color="#2CC985")
        self.btn_stop.configure(state="disabled", fg_color="#555555")
        if self.cap: self.cap.release()
        self.video_label.configure(image=None)
        self.interpreter.clear()

    def update_camera(self):
        if self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                if self.frame_count % 3 == 0:
                    results = self.model(frame, verbose=False, conf=0.6, imgsz=320)
                    self.last_annotated_frame = results[0].plot()
                    if results[0].boxes:
                        label_name = self.model.names[int(results[0].boxes[0].cls)]
                        sentence = self.interpreter.process_detection(label_name)
                        self.text_display.configure(text=sentence)
                
                img_to_show = self.last_annotated_frame if self.last_annotated_frame is not None else frame
                img = cv2.cvtColor(img_to_show, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img)
                w = self.video_label.winfo_width()
                h = self.video_label.winfo_height()
                if w < 10 or h < 10: w, h = 640, 480
                img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(w, h))
                self.video_label.configure(image=img_ctk)
                self.video_label.image = img_ctk 
            self.after(10, self.update_camera)
    # -------------------------------------------------------------------

    def show_goodbye_screen(self):
        self.stop_detection()
        for widget in self.winfo_children():
            widget.destroy()

        # Fondo del color del logo
        self.goodbye_frame = ctk.CTkFrame(self, fg_color=self.color_fondo_logo)
        self.goodbye_frame.pack(expand=True, fill="both")

        center_box = ctk.CTkFrame(self.goodbye_frame, fg_color="transparent")
        center_box.pack(expand=True)

        # 1. Texto de agradecimiento
        label_thanks = ctk.CTkLabel(
            center_box, 
            text="¡Gracias por usar", 
            font=("Roboto", 32, "bold"),
            text_color=self.color_texto_contraste
        )
        label_thanks.pack(pady=(0, 20))

        # 2. El LOGO
        if self.logo_image:
            label_logo = ctk.CTkLabel(center_box, text="", image=self.logo_image)
            label_logo.pack(pady=10)
        else:
            label_logo = ctk.CTkLabel(center_box, text="InterpretIA!", font=("Roboto", 50, "bold"), text_color=self.color_texto_contraste)
            label_logo.pack(pady=10)
            
        # Espacio final para balancear visualmente
        ctk.CTkLabel(center_box, text="\n", font=("Roboto", 20)).pack()
        
        self.after(3000, self.destroy)