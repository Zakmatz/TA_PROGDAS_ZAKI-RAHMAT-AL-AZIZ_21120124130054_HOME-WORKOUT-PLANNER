from tkinter import Tk
from guiComponents import WorkoutApp

if __name__ == "__main__":
    root = Tk()
    app = WorkoutApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()