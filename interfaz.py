import tkinter as tk
from tkinter import messagebox, font
from logica import QuizLogic
from preguntas import questions

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        super().__init__(master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = '#74b9ff'  # color hover

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class QuizAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Slimmy - Juego de Preguntas")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        # Fondo degradado simulado con canvas
        self.canvas = tk.Canvas(root, width=750, height=550)
        self.canvas.pack(fill="both", expand=True)
        self.gradient_background("#1e3799", "#2980b9")

        # Fuente personalizada
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.question_font = font.Font(family="Segoe UI", size=15)
        self.option_font = font.Font(family="Segoe UI", size=13)
        self.feedback_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.footer_font = font.Font(family="Segoe UI", size=10, weight="bold")

        # Marco principal para preguntas
        self.frame_main = tk.Frame(root, bg="white", bd=3, relief="raised")
        self.frame_main.place(relx=0.5, rely=0.5, anchor="center", width=700, height=450)

        # Etiqueta título
        self.label_title = tk.Label(self.frame_main, text="¡Bienvenido! Gracias a Slimmy Barrios por crear este juego.",
                                    font=self.title_font, bg="white", fg="#34495e")
        self.label_title.pack(pady=10)

        # Etiqueta pregunta con marco y padding
        self.label_question = tk.Label(self.frame_main, text="", font=self.question_font, bg="white", fg="#2c3e50", wraplength=650, justify="center")
        self.label_question.pack(pady=20, padx=10)

        # Frame para botones con sombra simulada
        self.buttons_frame = tk.Frame(self.frame_main, bg="white")
        self.buttons_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = HoverButton(self.buttons_frame, text="", font=self.option_font, width=30, height=2,
                              bg="#0984e3", fg="white", activebackground="#74b9ff", relief="flat",
                              command=lambda idx=i: self.select_option(idx))
            btn.grid(row=i//2, column=i%2, padx=15, pady=10)
            self.option_buttons.append(btn)

        # Temporizador con barra de progreso
        self.timer_frame = tk.Frame(self.frame_main, bg="white")
        self.timer_frame.pack(pady=15)

        self.label_timer = tk.Label(self.timer_frame, text="Tiempo: 30s", font=self.feedback_font, bg="white", fg="#27ae60")
        self.label_timer.pack()

        self.timer_bar = tk.Canvas(self.timer_frame, width=400, height=20, bg="#dfe6e9", highlightthickness=0)
        self.timer_bar.pack(pady=5)
        self.timer_bar_fill = self.timer_bar.create_rectangle(0, 0, 400, 20, fill="#27ae60")

        # Feedback para respuestas
        self.label_feedback = tk.Label(self.frame_main, text="", font=self.feedback_font, bg="white")
        self.label_feedback.pack(pady=10)

        # Puntaje
        self.label_score = tk.Label(self.frame_main, text="", font=("Segoe UI", 12), bg="white", fg="#34495e")
        self.label_score.pack(pady=5)

        # Botón de iniciar juego
        self.button_start = HoverButton(self.frame_main, text="Comenzar Juego", font=self.title_font,
                                        bg="#27ae60", fg="white", activebackground="#2ecc71",
                                        command=self.start_game)
        self.button_start.pack(pady=20)

        # Footer con nombre
        self.label_footer = tk.Label(root, text="Samuel Mba Esono Mangue", font=self.footer_font, bg="#1e3799", fg="white")
        self.label_footer.place(relx=0.5, rely=0.97, anchor="center")

        # Lógica del juego
        self.quiz_logic = QuizLogic(questions)
        self.quiz_logic.timer_callback = self.update_timer
        self.quiz_logic.time_up_callback = self.handle_time_up

    def gradient_background(self, color1, color2):
        # Simple degradado vertical
        for i in range(550):
            r1, g1, b1 = self.root.winfo_rgb(color1)
            r2, g2, b2 = self.root.winfo_rgb(color2)
            nr = int(r1 + (r2 - r1) * i / 550) >> 8
            ng = int(g1 + (g2 - g1) * i / 550) >> 8
            nb = int(b1 + (b2 - b1) * i / 550) >> 8
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            self.canvas.create_line(0, i, 750, i, fill=color)

    def start_game(self):
        self.quiz_logic.start_session()
        self.button_start.config(state="disabled")
        self.label_feedback.config(text="")
        self.label_score.config(text="")
        self.show_question()
        self.quiz_logic.timer_tick()

    def show_question(self):
        q = self.quiz_logic.get_current_question()
        if q is None:
            self.end_game()
            return
        self.label_question.config(text=f"Pregunta {self.quiz_logic.current_index + 1} de {len(self.quiz_logic.session_questions)}:\n\n{q['question']}")
        for i, option in enumerate(q["options"]):
            self.option_buttons[i].config(text=option, state="normal", bg="#0984e3")
        self.label_feedback.config(text="")
        self.update_timer(self.quiz_logic.time_left)

    def select_option(self, idx):
        if not self.quiz_logic.timer_running:
            return
        selected_text = self.option_buttons[idx].cget("text")
        result = self.quiz_logic.answer_current_question(selected_text)
        if result is None:
            return

        correct, correct_answer = result
        if correct:
            self.label_feedback.config(text="¡Correcto!", fg="#27ae60")
            self.option_buttons[idx].config(bg="#27ae60")
        else:
            self.label_feedback.config(text=f"❌ Incorrecto. La respuesta correcta era: {correct_answer}", fg="#d63031")
            self.option_buttons[idx].config(bg="#d63031")
            for btn in self.option_buttons:
                if btn.cget("text") == correct_answer:
                    btn.config(bg="#27ae60")

        self.disable_options()
        self.root.after(2000, self.next_question)

    def disable_options(self):
        for btn in self.option_buttons:
            btn.config(state="disabled")

    def next_question(self):
        self.quiz_logic.next_question()
        self.show_question()
        self.quiz_logic.timer_tick()

    def update_timer(self, time_left):
        self.label_timer.config(text=f"Tiempo: {time_left}s")
        # Actualizar barra de progreso
        width = int(400 * time_left / 30)
        self.timer_bar.coords(self.timer_bar_fill, 0, 0, width, 20)
        if time_left <= 10:
            self.label_timer.config(fg="#d63031")
            self.timer_bar.itemconfig(self.timer_bar_fill, fill="#d63031")
        else:
            self.label_timer.config(fg="#27ae60")
            self.timer_bar.itemconfig(self.timer_bar_fill, fill="#27ae60")

    def handle_time_up(self):
        q = self.quiz_logic.get_current_question()
        if q is None:
            return
        self.label_feedback.config(text=f"⏰ Tiempo agotado. La respuesta correcta era: {q['answer']}", fg="#d63031")
        for btn in self.option_buttons:
            if btn.cget("text") == q["answer"]:
                btn.config(bg="#27ae60")
            else:
                btn.config(state="disabled")
        self.root.after(3000, self.next_question)

    def end_game(self):
        total = len(self.quiz_logic.session_questions)
        score = self.quiz_logic.score
        msg = ""
        if score == total:
            msg = "🏆 ¡Excelente, eres un genio!"
        elif score >= total * 0.83:
            msg = "🔥 ¡Muy bien!"
        elif score >= total * 0.5:
            msg = "👍 Bien jugado"
        else:
            msg = "💬 Intenta mejorar"
        self.label_question.config(text="")
        self.label_feedback.config(text=f"Juego terminado. Tu puntaje: {score} / {total}\n{msg}", fg="#2d3436")
        self.label_timer.config(text="")
        self.disable_options()
        self.button_start.config(state="normal")
