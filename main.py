import tkinter as tk
from interfaz import QuizAppGUI

def main():
    root = tk.Tk()
    app = QuizAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
