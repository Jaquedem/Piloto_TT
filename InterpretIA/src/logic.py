import time

class SignLanguageInterpreter:
    def __init__(self):
        self.current_sequence = []  # Buffer de señas detectadas
        self.last_detection_time = time.time()
        self.consecutive_frames = 0
        self.last_label = None
        self.detection_threshold = 8   # Ajuste para responsividad
        self.silence_threshold = 2.5   # Tiempo para borrar texto

        # Estado del árbol de contexto
        self.current_tree_node = None  # Nodo actual en el árbol
        self.current_translation = "Esperando señas..."  # Traducción actual

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
        """
        Procesa una nueva detección y actualiza el estado interno.
        No retorna nada - usar get_current_translation() para obtener el texto.
        """
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
                    self.last_detection_time = current_time
                    print(f"✅ Seña detectada: {label}")
                    print(f"   Secuencia actual: {self.current_sequence}")

                    # Actualizar navegación del árbol con la nueva seña
                    self._navigate_tree(label)

        # 2. Chequeo de Silencio (IMPORTANTE: Esto corre aunque label sea None)
        if self.current_sequence and (current_time - self.last_detection_time > self.silence_threshold):
            self.clear()

    def _navigate_tree(self, new_sign):
        """
        Navega por el árbol de gramática con la nueva seña detectada.
        Actualiza current_tree_node y current_translation.
        """
        # Caso 1: Primera seña (iniciar en raíz)
        if self.current_tree_node is None:
            if new_sign in self.grammar_tree:
                self.current_tree_node = self.grammar_tree[new_sign]
                if "result" in self.current_tree_node:
                    self.current_translation = self.current_tree_node["result"]
                    print(f"   → Traducción: {self.current_translation}")
                return

        # Caso 2: Continuar desde nodo actual
        # Intentar buscar la nueva seña en los hijos del nodo actual
        if isinstance(self.current_tree_node, dict) and "children" in self.current_tree_node:
            if new_sign in self.current_tree_node["children"]:
                # Encontrada en hijos - seguir navegando
                self.current_tree_node = self.current_tree_node["children"][new_sign]
                if "result" in self.current_tree_node:
                    self.current_translation = self.current_tree_node["result"]
                    print(f"   → Traducción: {self.current_translation}")
                return

        # Caso 3: No encontrada en hijos - ¿Es una nueva frase raíz?
        if new_sign in self.grammar_tree:
            # Reset: iniciar nueva frase desde raíz
            print(f"   🔄 Iniciando nueva frase con: {new_sign}")
            self.current_tree_node = self.grammar_tree[new_sign]
            if "result" in self.current_tree_node:
                self.current_translation = self.current_tree_node["result"]
                print(f"   → Traducción: {self.current_translation}")
            # Limpiar secuencia anterior (nueva frase)
            self.current_sequence = [new_sign]
        else:
            # Caso 4: Seña no reconocida en el contexto actual
            print(f"   ⚠️ Seña '{new_sign}' no encaja en el contexto actual")

    def get_current_translation(self):
        """
        Retorna la traducción actual sin procesar nada nuevo.
        """
        return self.current_translation

    def clear(self):
        """
        Limpia el estado del intérprete y resetea el árbol.
        """
        self.current_sequence = []
        self.last_detection_time = time.time()
        self.consecutive_frames = 0
        self.current_tree_node = None
        self.current_translation = "Esperando señas..."
        print("🧹 Limpiando pantalla y reseteando árbol de contexto...")