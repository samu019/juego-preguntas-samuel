import random
import threading

class QuizLogic:
    def __init__(self, questions):
        self.questions = questions
        self.session_questions = []
        self.score = 0
        self.current_index = 0
        self.time_left = 30
        self.timer_running = False
        self.timer_callback = None  # función para actualizar UI cada segundo
        self.time_up_callback = None  # función para manejar tiempo agotado

    def start_session(self, questions_per_session=30):
        # Escoge preguntas aleatorias sin repetir, máximo la cantidad que hay
        count = min(questions_per_session, len(self.questions))
        self.session_questions = random.sample(self.questions, k=count)
        self.score = 0
        self.current_index = 0
        self.time_left = 30
        self.timer_running = True

    def get_current_question(self):
        if self.current_index < len(self.session_questions):
            return self.session_questions[self.current_index]
        return None

    def answer_current_question(self, selected_option):
        if not self.timer_running:
            return None  # Ignorar si el tiempo ya acabó o se respondió

        self.timer_running = False
        current_q = self.get_current_question()
        if current_q is None:
            return None

        correct_answer = current_q["answer"]
        correct = (selected_option == correct_answer)
        if correct:
            self.score += 1
        return correct, correct_answer

    def next_question(self):
        self.current_index += 1
        self.time_left = 30
        self.timer_running = True

    def timer_tick(self):
        if self.timer_running:
            self.time_left -= 1
            if self.timer_callback:
                self.timer_callback(self.time_left)
            if self.time_left <= 0:
                self.timer_running = False
                if self.time_up_callback:
                    self.time_up_callback()
                return
            # Usar un hilo para esperar 1 segundo sin bloquear la interfaz
            threading.Timer(1.0, self.timer_tick).start()
