import time

class SignLanguageInterpreter:
    def __init__(self):
        self.current_sequence = []  # Buffer de señas detectadas en orden
        self.last_detection_time = time.time()
        self.consecutive_frames = 0
        self.last_label = None
        self.detection_threshold = 10  # Frames necesarios para confirmar seña (ajustable)
        self.silence_threshold = 2.0   # Segundos de inactividad para reiniciar frase

        # --- ÁRBOL DE DECISIONES (Basado en tu PDF) ---
        # Estructura: { "SEÑA_ACTUAL": { "SIGUIENTE_SEÑA": { ...Result... }, "result": "Traducción base" } }
        self.grammar_tree = {
            "tu": {
                "result": "Tú...",
                "children": {
                    "bien": {"result": "¿Tú estás bien?"},      # 
                    "comer": {
                        "result": "Tú comes.",                   # 
                        "children": {
                            "bien": {"result": "¿Tú comiste bien?"},  # 
                            "no": {
                                "children": {
                                    "bien": {"result": "Tú no comes bien."}, # 
                                    "estar": {
                                        "children": {
                                            "bien": {"result": "¿Tu comida no está bien?"} # 
                                        }
                                    }
                                }
                            },
                            "que": {"result": "¿Tú qué comes?"},      # 
                            "estar": {
                                "children": {
                                    "bien": {"result": "¿Tu comida está bien?"}, # 
                                    "no": {
                                        "children": {
                                            "bien": {"result": "¿Tu comida no está bien?"} #  Variation
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "que": {
                         "children": {
                             "comer": {"result": "¿Tú qué vas a comer?"} # 
                         }
                    }
                }
            },
            "comer": {
                "result": "Comer...",
                "children": {
                    "bien": {"result": "¡Come bien!"}, # [cite: 6]
                    "no": {
                        "children": {
                            "bien": {"result": "Tú no comes bien."},        # [cite: 6]
                            "estar": {
                                "children": {
                                    "bien": {"result": "Tu comida no está bien."} # [cite: 7]
                                }
                            }
                        }
                    },
                    "estar": {
                        "children": {
                            "bien": {"result": "La comida está bien."}            # [cite: 7]
                        }
                    }
                }
            },
            "hola": {
                "result": "Hola.", # [cite: 9]
                "children": {
                    "como": {
                        "children": {
                            "estar": {
                                "result": "Hola, ¿cómo estás?",           # [cite: 9]
                                "children": {
                                    "tu": {"result": "Hola, ¿cómo estás tú?"} # [cite: 9]
                                }
                            }
                        }
                    }
                }
            },
            "como": {
                "result": "¿Cómo...?",
                "children": {
                    "estar": {
                        "result": "¿Cómo estás?",       # [cite: 11]
                        "children": {
                            "tu": {"result": "¿Cómo estás tú?"} # [cite: 11]
                        }
                    }
                }
            },
            "que": {
                "result": "¿Qué...?",
                "children": {
                    "comer": {
                        "result": "¿Qué hay de comer?",     # [cite: 18]
                        "children": {
                            "tu": {"result": "¿Qué comes tú?"} # [cite: 22]
                        }
                    },
                    "bien": {
                        "result": "¡Qué bien!",            # [cite: 25]
                        "children": {
                            "tu": {
                                "children": {
                                    "comer": {"result": "¡Qué bien comes!"} # [cite: 26]
                                }
                            }
                        }
                    }
                }
            },
            "no": {
                "result": "No.", # [cite: 30]
                "children": {
                    "bien": {"result": "No estoy bien."},       # [cite: 30]
                    "estar": {
                        "children": {
                            "bien": {"result": "No estoy bien."} # [cite: 30]
                        }
                    },
                    "comer": {"result": "No quiero comer / No como"} # [cite: 30]
                }
            },
            "estar": {
                "children": {
                    "bien": {"result": "Estoy bien."} # [cite: 32]
                }
            },
            "gracias": {
                "result": "Gracias.", # [cite: 34]
                "children": {
                    "comer": {
                        "children": {
                            "bien": {"result": "Gracias, comí bien."} # [cite: 34]
                        }
                    }
                }
            },
            "bien": {
                "result": "Bien." # [cite: 34]
            }
        }

    def process_detection(self, label):
        current_time = time.time()
        
        # 1. Filtro de Estabilidad (Debounce)
        if label == self.last_label:
            self.consecutive_frames += 1
        else:
            self.consecutive_frames = 0
            self.last_label = label

        # 2. Si la seña es estable y es diferente a la última registrada en la secuencia
        if self.consecutive_frames >= self.detection_threshold:
            # Solo añadir si es una seña nueva (evitar "tu tu tu")
            if not self.current_sequence or self.current_sequence[-1] != label:
                self.current_sequence.append(label)
                self.last_detection_time = current_time
                print(f"✅ Seña agregada: {label} | Secuencia: {self.current_sequence}")

        # 3. Validar Tiempos de Silencio (Limpieza automática)
        # Si pasa X tiempo sin señas nuevas, limpiamos
        if current_time - self.last_detection_time > self.silence_threshold:
            if self.current_sequence: # Solo si había algo
                self.clear()
                return "" # Retornamos vacío para limpiar pantalla

        # 4. Traducir Secuencia usando el Árbol
        translation = self._translate_sequence()
        return translation

    def _translate_sequence(self):
        # Recorremos el árbol siguiendo la lista self.current_sequence
        if not self.current_sequence:
            return "Esperando señas..."
        
        current_node = self.grammar_tree
        current_translation = "..." # Default si no encuentra traducción exacta

        # Navegar el árbol
        for word in self.current_sequence:
            # Caso 1: La palabra es un nodo hijo válido
            if isinstance(current_node, dict) and "children" in current_node and word in current_node["children"]:
                current_node = current_node["children"][word]
                if "result" in current_node:
                    current_translation = current_node["result"]
            
            # Caso 2: Es el inicio de una nueva frase (Raíz)
            elif word in self.grammar_tree:
                current_node = self.grammar_tree[word]
                if "result" in current_node:
                    current_translation = current_node["result"]
            
            else:
                # La seña rompió la secuencia lógica, reiniciar secuencia desde esta seña
                # Esto permite corregir si el usuario cambia de idea
                # Ej: Estaba haciendo "Tu comer" y de repente hace "Hola"
                if word in self.grammar_tree:
                     # Intentamos recuperar si es una palabra raíz válida
                     current_node = self.grammar_tree[word]
                     if "result" in current_node:
                        current_translation = current_node["result"]
                else:
                    current_translation = f"{word} (?)"

        return current_translation

    def clear(self):
        self.current_sequence = []
        self.last_detection_time = time.time()
        print("🧹 Secuencia limpiada por inactividad")
        return "Esperando señas..."