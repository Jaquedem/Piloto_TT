import time

class SignLanguageInterpreter:
    def __init__(self):
        self.current_sequence = []  # Buffer de señas detectadas
        self.last_detection_time = time.time()
        self.consecutive_frames = 0
        self.last_label = None

        # Tiempos optimizados para detección rápida
        self.detection_threshold = 3   # Frames para confirmar seña (más rápido)
        self.cooldown_time = 2.5        # Espera entre señas (2.5 segundos)
        self.silence_threshold = 3.5    # Tiempo sin detección para finalizar (3.5 segundos)
        self.last_sign_added_time = 0   # Timestamp de última seña agregada

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

            # Verificar si la seña es estable Y si ya pasó el cooldown
            if self.consecutive_frames >= self.detection_threshold:
                # Verificar que sea una seña nueva (no repetida)
                is_new_sign = not self.current_sequence or self.current_sequence[-1] != label

                # Verificar cooldown: si hay secuencia, debe haber pasado cooldown_time
                cooldown_passed = (self.last_sign_added_time == 0 or
                                  (current_time - self.last_sign_added_time >= self.cooldown_time))

                if is_new_sign and cooldown_passed:
                    # Agregar la nueva seña
                    self.current_sequence.append(label)
                    self.last_detection_time = current_time
                    self.last_sign_added_time = current_time  # Timestamp de cuando se agregó

                    # Actualizar navegación del árbol con la nueva seña
                    self._navigate_tree(label)

                    # Resetear frames para siguiente detección
                    self.consecutive_frames = 0

        # 2. Chequeo de Silencio (finalizar secuencia después del tiempo límite sin nueva seña)
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
                return

        # Caso 2: Continuar desde nodo actual
        # Intentar buscar la nueva seña en los hijos del nodo actual
        if isinstance(self.current_tree_node, dict) and "children" in self.current_tree_node:
            if new_sign in self.current_tree_node["children"]:
                # Encontrada en hijos - seguir navegando
                self.current_tree_node = self.current_tree_node["children"][new_sign]
                if "result" in self.current_tree_node:
                    self.current_translation = self.current_tree_node["result"]
                return

        # Caso 3: No encontrada en hijos - ¿Es una nueva frase raíz?
        if new_sign in self.grammar_tree:
            # Reset: iniciar nueva frase desde raíz
            self.current_tree_node = self.grammar_tree[new_sign]
            if "result" in self.current_tree_node:
                self.current_translation = self.current_tree_node["result"]
            # Limpiar secuencia anterior (nueva frase)
            self.current_sequence = [new_sign]

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
        self.last_sign_added_time = 0
        self.current_tree_node = None
        self.current_translation = "Esperando señas..."