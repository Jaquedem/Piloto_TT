import time

class SignLanguageInterpreter:
    def __init__(self):
        self.current_sequence = []  # Buffer de señas detectadas
        self.last_detection_time = time.time()
        self.consecutive_frames = 0
        self.last_label = None
        self.detection_threshold = 8   # Ajuste para responsividad
        self.silence_threshold = 2.5   # Tiempo para borrar texto

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
        
        # 1. Filtro de Estabilidad (Solo si hay label)
        if label:
            if label == self.last_label:
                self.consecutive_frames += 1
            else:
                self.consecutive_frames = 0
                self.last_label = label

            # Agregar a la secuencia si es estable
            if self.consecutive_frames >= self.detection_threshold:
                if not self.current_sequence or self.current_sequence[-1] != label:
                    self.current_sequence.append(label)
                    self.last_detection_time = current_time # Renovamos el tiempo de vida
                    print(f"✅ Seña: {label} -> {self.current_sequence}")

        # 2. Chequeo de Silencio (IMPORTANTE: Esto corre aunque label sea None)
        # Si ha pasado mucho tiempo desde la última seña válida AGREGADA
        if self.current_sequence and (current_time - self.last_detection_time > self.silence_threshold):
            return self.clear()

        # 3. Retornar Traducción Actual
        return self._translate_sequence()

    def _translate_sequence(self):
        if not self.current_sequence:
            return "Esperando señas..." # Texto por defecto
        
        current_node = self.grammar_tree
        current_translation = "..." 

        for word in self.current_sequence:
            found = False
            # Buscar en hijos
            if isinstance(current_node, dict) and "children" in current_node:
                if word in current_node["children"]:
                    current_node = current_node["children"][word]
                    if "result" in current_node:
                        current_translation = current_node["result"]
                    found = True
            
            # Buscar en raíz (nueva frase)
            if not found and word in self.grammar_tree:
                current_node = self.grammar_tree[word]
                if "result" in current_node:
                    current_translation = current_node["result"]
                # Reiniciamos contexto al nodo raíz nuevo
            
        return current_translation

    def clear(self):
        self.current_sequence = []
        self.last_detection_time = time.time()
        self.consecutive_frames = 0
        print("🧹 Limpiando pantalla...")
        return "Esperando señas..."