import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

class Student:
    def __init__(self, name, math_score, physics_score, russian_score, informatics_score=None, has_achievements=False):
        self.name = name
        self.math_score = math_score
        self.physics_score = physics_score
        self.russian_score = russian_score
        self.informatics_score = informatics_score
        self.has_achievements = has_achievements
        self.math_comment = ""
        self.physics_comment = ""
        self.apply_conditions()
        self.total_score = self.calculate_total_score()

    def apply_conditions(self):
        if self.math_score >= 85 and 35 <= self.physics_score <= 49:
            self.physics_comment = f"({self.physics_score})"
            self.physics_score = 50
        if self.physics_score >= 90 and 35 <= self.math_score <= 49:
            self.math_comment = f"({self.math_score})"
            self.math_score = 50
        if self.informatics_score is not None and self.informatics_score >= 90 and 35 <= self.math_score <= 49:
            self.math_comment = f"({self.math_score})"
            self.math_score = 50

    def calculate_total_score(self):
        if self.informatics_score is not None:
            return self.math_score + max(self.physics_score, self.informatics_score) + self.russian_score
        else:
            return self.math_score + self.physics_score + self.russian_score

    def __str__(self):
        achievements = "*" if self.has_achievements else ""
        math_display = f"{self.math_score}{self.math_comment}"
        physics_display = f"{self.physics_score}{self.physics_comment}"
        informatics = f", Информатика: {self.informatics_score}" if self.informatics_score is not None else ""
        russian_display = f"{self.russian_score}"
        return f"{self.name}{achievements}: {self.total_score} (Математика: {math_display}, Физика: {physics_display}{informatics}, Русский: {russian_display})"

class App:
    def __init__(self, root):
        self.students = []
        self.root = root
        self.root.title("Рейтинг учеников")

        # Поля ввода
        self.name_var = tk.StringVar()
        self.math_var = tk.StringVar()
        self.physics_var = tk.StringVar()
        self.russian_var = tk.StringVar()
        self.informatics_var = tk.StringVar()
        self.achievements_var = tk.BooleanVar()
        self.delete_var = tk.StringVar()  # Поле для ввода номера ученика для удаления

        tk.Label(root, text="ФИО").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(root, text="Математика").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.math_var).grid(row=1, column=1)

        tk.Label(root, text="Физика").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.physics_var).grid(row=2, column=1)

        tk.Label(root, text="Русский язык").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.russian_var).grid(row=3, column=1)

        tk.Label(root, text="Информатика").grid(row=4, column=0)
        tk.Entry(root, textvariable=self.informatics_var).grid(row=4, column=1)

        tk.Checkbutton(root, text="Достижения по олимпиадам", variable=self.achievements_var).grid(row=5, columnspan=2)

        # Кнопки
        tk.Button(root, text="Добавить ученика", command=self.add_student).grid(row=6, columnspan=2)
        tk.Button(root, text="Показать рейтинг", command=self.display_ranking).grid(row=7, columnspan=2)
        
        tk.Label(root, text="Номер ученика для удаления").grid(row=8, column=0)
        tk.Entry(root, textvariable=self.delete_var).grid(row=8, column=1)
        tk.Button(root, text="Удалить ученика по номеру", command=self.delete_student_by_number).grid(row=9, columnspan=2)
        
        tk.Button(root, text="Удалить все записи", command=self.delete_all_students).grid(row=10, columnspan=2)
        tk.Button(root, text="Экспортировать в CSV", command=self.export_to_csv).grid(row=11, columnspan=2)
        tk.Button(root, text="Импортировать из CSV", command=self.import_from_csv).grid(row=12, columnspan=2)
        tk.Button(root, text="Выйти", command=root.quit).grid(row=13, columnspan=2)

        self.text = tk.Text(root, height=20, width=80)
        self.text.grid(row=14, columnspan=2)

    def add_student(self):
        try:
            name = self.name_var.get()
            math_score = int(self.math_var.get())
            physics_score = int(self.physics_var.get())
            russian_score = int(self.russian_var.get())
            informatics_score = int(self.informatics_var.get()) if self.informatics_var.get() else None
            has_achievements = self.achievements_var.get()

            if not (0 <= math_score <= 100 and 0 <= physics_score <= 100 and 0 <= russian_score <= 100 and (informatics_score is None or 0 <= informatics_score <= 100)):
                raise ValueError("Баллы должны быть в диапазоне от 0 до 100")

            student = Student(name, math_score, physics_score, russian_score, informatics_score, has_achievements)
            self.students.append(student)
            self.students.sort(key=lambda s: (s.total_score, s.has_achievements, s.math_score, s.physics_score, s.russian_score), reverse=True)
            self.clear_inputs()
            self.display_ranking()

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def clear_inputs(self):
        self.name_var.set("")
        self.math_var.set("")
        self.physics_var.set("")
        self.russian_var.set("")
        self.informatics_var.set("")
        self.achievements_var.set(False)
        self.delete_var.set("")

    def display_ranking(self):
        self.text.delete(1.0, tk.END)
        if not self.students:
            self.text.insert(tk.END, "Рейтинг пуст.\n")
        else:
            for i, student in enumerate(self.students, 1):
                if i == 71:
                    self.text.insert(tk.END, "------------ Список поступивших закончился ------------\n")
                self.text.insert(tk.END, f"{i}. {student}\n")

    def delete_student_by_number(self):
        try:
            number = int(self.delete_var.get())
            if 1 <= number <= len(self.students):
                removed_student = self.students.pop(number - 1)
                messagebox.showinfo("Удаление ученика", f"Ученик {removed_student.name} удален.")
                self.display_ranking()
            else:
                messagebox.showerror("Ошибка", "Неверный номер.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный номер.")

    def delete_all_students(self):
        self.students.clear()
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, "Все записи удалены.\n")

    def export_to_csv(self):
        if not self.students:
            messagebox.showerror("Ошибка", "Список учеников пуст. Нечего экспортировать.")
            return

        data = {
            "ФИО": [student.name for student in self.students],
            "Баллы по математике": [f"{student.math_score}{student.math_comment}" for student in self.students],
            "Баллы по физике": [f"{student.physics_score}{student.physics_comment}" for student in self.students],
            "Баллы по информатике": [student.informatics_score if student.informatics_score is not None else "" for student in self.students],
            "Баллы по русскому языку": [student.russian_score for student in self.students],
            "Общая сумма баллов": [student.total_score for student in self.students],
            "Достижения по олимпиадам": ["Да" if student.has_achievements else "Нет" for student in self.students]
        }

        df = pd.DataFrame(data)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Экспорт в CSV", "Рейтинг экспортирован в файл.")

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
                for _, row in df.iterrows():
                    name = row['ФИО']
                    math_score_str = row['Баллы по математике']
                    if "50" in math_score_str:
                        math_comment = math_score_str.split(")")[0][-3:] + ")"
                        math_score = int(math_score_str.split("#")[0].strip())
                    else:
                        math_score = int(math_score_str)
                        math_comment = ""

                    physics_score_str = row['Баллы по физике']
                    if "50" in physics_score_str:
                        physics_comment = physics_score_str.split(")")[0][-3:] + ")"
                        physics_score = int(physics_score_str.split("#")[0].strip())
                    else:
                        physics_score = int(physics_score_str)
                        physics_comment = ""

                    russian_score = int(row['Баллы по русскому языку'])

                    informatics_score = int(row['Баллы по информатике']) if pd.notna(row['Баллы по информатике']) else None
                    has_achievements = row['Достижения по олимпиадам'] == "Да"

                    student = Student(name, math_score, physics_score, russian_score, informatics_score, has_achievements)
                    student.math_comment = math_comment
                    student.physics_comment = physics_comment
                    self.students.append(student)

                self.students.sort(key=lambda s: (s.total_score, s.has_achievements, s.math_score, s.physics_score, s.russian_score), reverse=True)
                messagebox.showinfo("Импорт из CSV", "Рейтинг импортирован из файла.")
                self.display_ranking()
            except Exception as e:
                messagebox.showerror("Ошибка при импорте", f"Ошибка при импорте: {e}")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
