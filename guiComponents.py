from tkinter import *
from tkinter import messagebox
from workout import Exercise, WorkoutPlan

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Workout Planner")
        self.root.geometry("600x400")
        self.root.config(bg="#0c013d")

        self.workout_plan = WorkoutPlan()
        self.workout_plan.load_from_file()

        self.current_exercise_index = 0
        self.current_set = 1

        self.setup_main_screen()

    def setup_main_screen(self):
        self.clear_screen()

        title_label = Label(self.root, text="Home Workout Planner", font=("Arial", 24, "bold"), bg="#0c013d", fg="white",)
        title_label.pack(pady=20)

        self.button_frame = Frame(self.root, bg="#0c013d")
        self.button_frame.pack(pady=20)

        start_button = Button(self.button_frame, text="Start Workout", command=self.start_workout, width=20, bg="#079460", fg="white",)
        start_button.pack(pady=10)

        add_button = Button(self.button_frame, text="Add Workout", command=self.add_workout_screen, width=20, bg="#079460", fg="white",)
        add_button.pack(pady=10)

        edit_button = Button(self.button_frame, text="Edit Workout", command=self.edit_workout_screen, width=20, bg="#079460", fg="white",)
        edit_button.pack(pady=10)

        delete_button = Button(self.button_frame, text="Delete Workout", command=self.delete_workout_screen, width=20, bg="#079460", fg="white",)
        delete_button.pack(pady=10)

    def start_workout(self):
        if not self.workout_plan.exercises:
            messagebox.showerror("Error", "No workouts available! Add some workouts first.")
            return

        self.current_exercise_index = 0
        self.current_set = 1
        self.show_exercises_screen()

    def show_exercises_screen(self):
        self.clear_screen()

        if self.current_exercise_index >= len(self.workout_plan.exercises):
            messagebox.showinfo("Workout Complete", "You've completed all exercises!")
            self.setup_main_screen()
            return
        
        exercise = self.workout_plan.exercises[self.current_exercise_index]

        exercise_label = Label(self.root, text=f"Exercise: {exercise.name} ({exercise.category})", font=("Arial", 16, "bold"), bg="#0c013d", fg="white",)
        exercise_label.pack(pady=10)

        set_label = Label(self.root, text=f"Set: {self.current_set}/{exercise.sets}", font=("Arial", 14), bg="#0c013d", fg="white")
        set_label.pack(pady=5)

        reps_label = Label(self.root, text=f"Repetitions: {exercise.repetitions}", font=("Arial", 14), bg="#0c013d", fg="white",)
        reps_label.pack(pady=5)

        button_frame = Frame(self.root, bg="#0c013d")
        button_frame.pack(side="bottom", fill="x", pady=20)

        back_button = Button(button_frame, text="Back", command=self.go_to_previous, bg="#079460", fg="white", width=10)
        back_button.pack(side="left", padx=10)

        next_button = Button(button_frame, text="Next", command=self.go_to_next,bg="#079460", fg="white", width=10)
        next_button.pack(side="right", padx=10)
        
        stop_button = Button(self.root, text="Stop Workout", command=self.setup_main_screen, bg="#079460", fg="white", width=20)
        stop_button.place(x=225, y=350)

    def go_to_next(self):
        exercise = self.workout_plan.exercises[self.current_exercise_index]
        if self.current_set < exercise.sets:
            self.current_set += 1
        else:
            self.current_set = 1
            self.current_exercise_index += 1
        self.show_exercises_screen()

    def go_to_previous(self):
        if self.current_set > 1:
            self.current_set -= 1
        else:
            if self.current_exercise_index > 0:
                self.current_exercise_index -= 1
                exercise : self.workout_plan.exercises[self.current_exercise_index]
        self.show_exercises_screen()

    def add_workout_screen(self):
        self.clear_screen()

        name_label = Label(self.root, text="Workout Name:", bg="#0c013d", fg="white")
        name_label.pack(pady=5)
        name_entry = Entry(self.root)
        name_entry.pack(pady=5)

        category_label = Label(self.root, text="Category:", bg="#0c013d", fg="white")
        category_label.pack(pady=5)
        category_entry = Entry(self.root)
        category_entry.pack(pady=5)

        sets_label = Label(self.root, text="Sets:", bg="#0c013d", fg="white")
        sets_label.pack(pady=5)
        sets_entry = Entry(self.root)
        sets_entry.pack(pady=5)

        reps_label = Label(self.root, text="Repetitions:", bg="#0c013d", fg="white")
        reps_label.pack(pady=5)
        reps_entry = Entry(self.root)
        reps_entry.pack(pady=5)

        def submit():
            try:
                name = name_entry.get()
                category = category_entry.get()
                sets = int(sets_entry.get())
                repetitions = int(reps_entry.get())

                new_exercise = Exercise(name, category, sets, repetitions)
                self.workout_plan.add_exercise(new_exercise)

                messagebox.showinfo("Succes", "Your workout added successfully!")
                self.setup_main_screen()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data!")

        submit_button = Button(self.root, text="Add workout", command=submit, width=15, bg="#079460", fg="white")
        submit_button.pack(pady=10)

        back_button = Button(self.root, text="Back", command=self.setup_main_screen, width=10, bg="#079460", fg="white")
        back_button.pack(pady=10)

    def edit_workout_screen(self):
        self.clear_screen()

        title_label = Label(self.root, text="Edit Workout", font=("Arial", 20, "bold"), bg="#0c013d", fg="white",)
        title_label.pack(pady=20)

        workout_listbox = Listbox(self.root, bg="#0c013d", fg="white", font=("Arial", 12), selectmode=SINGLE)
        workout_listbox.pack(pady=10, fill=BOTH, expand=True)

        for exercise in self.workout_plan.exercises:
            workout_listbox.insert(END, exercise.name)

        def edit_selected_workout():
            selected_index = workout_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a workout to edit!")
                return

            selected_index = selected_index[0]
            exercise = self.workout_plan.exercises[selected_index]

            self.clear_screen()

            name_label = Label(self.root, text="Workout Name:", bg="#0c013d", fg="white")
            name_label.pack(pady=5)
            name_entry = Entry(self.root)
            name_entry.insert(0, exercise.name)
            name_entry.pack(pady=5)

            category_label = Label(self.root, text="Category:", bg="#0c013d", fg="white")
            category_label.pack(pady=5)
            category_entry = Entry(self.root)
            category_entry.insert(0, exercise.category)
            category_entry.pack(pady=5)

            sets_label = Label(self.root, text="Sets:", bg="#0c013d", fg="white")
            sets_label.pack(pady=5)
            sets_entry = Entry(self.root)
            sets_entry.insert(0, exercise.sets)
            sets_entry.pack(pady=5)

            reps_label = Label(self.root, text="Repetitions:", bg="#0c013d", fg="white")
            reps_label.pack(pady=5)
            reps_entry = Entry(self.root)
            reps_entry.insert(0, exercise.repetitions)
            reps_entry.pack(pady=5)

            def save_changes():
                try:
                    exercise.name = name_entry.get()
                    exercise.category = category_entry.get()
                    exercise.sets = int(sets_entry.get())
                    exercise.repetitions = int(reps_entry.get())
                    self.workout_plan.save_to_file()
                    messagebox.showinfo("Success", "Workout updated successfully!")
                    self.setup_main_screen()
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid data!")

            save_button = Button(self.root, text="Save Changes", command=save_changes, bg="#079460", fg="white")
            save_button.pack(pady=10)

            back_button = Button(self.root, text="Back", command=self.setup_main_screen, bg="#079460", fg="white")
            back_button.pack(pady=10)

        edit_button = Button(self.root, text="Edit Selected", command=edit_selected_workout, width=20, bg="#079460", fg="white",)
        edit_button.pack(pady=10)

        back_button = Button(self.root, text="Back", command=self.setup_main_screen, bg="#079460", fg="white")
        back_button.pack(pady=10)

    def delete_workout_screen(self):
        self.clear_screen()

        title_label = Label(self.root, text="Delete Workout", font=("Arial", 20, "bold"), bg="#0c013d", fg="white",)
        title_label.pack(pady=20)

        workout_listbox = Listbox(self.root, bg="#0c013d", fg="white", font=("Arial", 12), selectmode=SINGLE)
        workout_listbox.pack(pady=10, fill=BOTH, expand=True)

        for exercise in self.workout_plan.exercises:
            workout_listbox.insert(END, exercise.name)

        def delete_selected_workout():
            selected_index = workout_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a workout to delete!")
                return

            selected_index = selected_index[0]
            del self.workout_plan.exercises[selected_index]
            self.workout_plan.save_to_file()
            messagebox.showinfo("Success", "Workout deleted successfully!")
            self.setup_main_screen()

        delete_button = Button(self.root, text="Delete Selected", command=delete_selected_workout, bg="#079460", fg="white")
        delete_button.pack(pady=10)

        back_button = Button(self.root, text="Back", command=self.setup_main_screen, bg="#079460", fg="white")
        back_button.pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_exit(self):
        self.workout_plan.save_to_file()
        self.root.destroy()