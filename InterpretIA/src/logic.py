import time

class SignLanguageInterpreter:
    def __init__(self):
        self.sentence = [] # Lista para guardar las palabras detectadas
        self.last_prediction = None
        self.consecutive_frames = 0
        self.detection_threshold = 15  # Necesita 15 frames iguales para confirmar la seña (ajustable)
        self.last_update_time = time.time()
        self.silence_threshold = 3.0   # Segundos sin detectar nada para limpiar (ajustable)

    def process_detection(self, label):
        current_time = time.time()

        # Lógica de estabilización (Debounce)
        if label == self.last_prediction:
            self.consecutive_frames += 1
        else:
            self.consecutive_frames = 0
            self.last_prediction = label

        # Si la seña es estable, la agregamos
        if self.consecutive_frames == self.detection_threshold:
            self._add_to_sentence(label)
            self.consecutive_frames = 0 # Reiniciar contador

        # Limpiar oración si pasa mucho tiempo sin señas nuevas
        if current_time - self.last_update_time > self.silence_threshold and self.sentence:
            # Opcional: Aquí podrías limpiar la oración automáticamente
            pass 

        return self.get_sentence_string()

    def _add_to_sentence(self, word):
        # Evitar repetir la misma palabra seguida (ej: "HOLA HOLA")
        if not self.sentence or self.sentence[-1] != word:
            self.sentence.append(word)
            self.last_update_time = time.time()
            
            # Mantener la oración corta (máx 10 palabras para que quepa en pantalla)
            if len(self.sentence) > 10:
                self.sentence.pop(0)

    def get_sentence_string(self):
        return " ".join(self.sentence)

    def clear(self):
        self.sentence = []