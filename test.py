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
            self.physics_comment = f"#50({self.physics_score})"
            self.physics_score = 50
        if self.physics_score >= 90 and 35 <= self.math_score <= 49:
            self.math_comment = f"#50({self.math_score})"
            self.math_score = 50
        if self.informatics_score is not None and self.informatics_score >= 90 and 35 <= self.math_score <= 49:
            self.math_comment = f"#50({self.math_score})"
            self.math_score = 50

    def calculate_total_score(self):
        if self.informatics_score is not None:
            return self.math_score + max(self.physics_score, self.informatics_score) + self.russian_score
        else:
            return self.math_score + self.physics_score + self.russian_score

    def is_eligible(self):
        return self.math_score >= 50 and self.physics_score >= 50 and self.russian_score >= 50

    def __str__(self):
        achievements = "*" if self.has_achievements else ""
        math_display = f"{self.math_score}{self.math_comment}"
        physics_display = f"{self.physics_score}{self.physics_comment}"
        informatics = f", Информатика: {self.informatics_score}" if self.informatics_score is not None else ""
        russian_display = f"{self.russian_score}"
        return f"{self.name}{achievements}: {self.total_score} (Математика: {math_display}, Физика: {physics_display}{informatics}, Русский: {russian_display})"

def get_score(subject):
    while True:
        try:
            score = int(input(f"Введите баллы по {subject}: "))
            if 0 <= score <= 100:
                return score
            else:
                print("Ошибка: баллы должны быть в диапазоне от 0 до 100.")
        except ValueError:
            print("Ошибка: пожалуйста, введите числовое значение.")

def add_student(students):
    name = input("Введите ФИО ученика: ")
    math_score = get_score("математике")
    physics_score = get_score("физике")
    russian_score = get_score("русскому языку")
    informatics_choice = input("Ученик сдавал информатику? (да/нет): ").strip().lower()
    informatics_score = None

    if informatics_choice == "да":
        informatics_score = get_score("информатике")

    has_achievements = input("Есть ли у ученика достижения по олимпиадам? (да/нет): ").strip().lower() == "да"

    student = Student(name, math_score, physics_score, russian_score, informatics_score, has_achievements)
    students.append(student)
    students.sort(key=lambda s: (s.has_achievements, s.total_score, s.math_score, s.physics_score, s.russian_score), reverse=True)

def display_ranking(students):
    if not students:
        print("Рейтинг пуст.")
    else:
        print("\nРейтинг учеников:")
        for i, student in enumerate(students, 1):
            if i == 71:
                print("------------ Список поступивших закончился ------------")
            print(f"{i}. {student}")

def delete_student_by_number(students):
    if not students:
        print("Список учеников пуст.")
        return
    
    display_ranking(students)
    try:
        number = int(input("Введите номер ученика для удаления: "))
        if 1 <= number <= len(students):
            removed_student = students.pop(number - 1)
            print(f"Ученик {removed_student.name} удален.")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")

def delete_all_students(students):
    students.clear()
    print("Все записи удалены.")

def export_to_csv(students):
    if not students:
        print("Список учеников пуст. Нечего экспортировать.")
        return

    data = {
        "ФИО": [student.name for student in students],
        "Баллы по математике": [f"{student.math_score}{student.math_comment}" for student in students],
        "Баллы по физике": [f"{student.physics_score}{student.physics_comment}" for student in students],
        "Баллы по информатике": [student.informatics_score if student.informatics_score is not None else "" for student in students],
        "Баллы по русскому языку": [student.russian_score for student in students],
        "Общая сумма баллов": [student.total_score for student in students],
        "Достижения по олимпиадам": ["Да" if student.has_achievements else "Нет" for student in students]
    }

    df = pd.DataFrame(data)
    df.to_csv('students_ranking.csv', index=False, encoding='utf-8-sig')
    print("Рейтинг экспортирован в файл 'students_ranking.csv'.")

def import_from_csv(students):
    try:
        df = pd.read_csv('students_ranking.csv', encoding='utf-8-sig')
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
            students.append(student)

        students.sort(key=lambda s: (s.total_score,s.has_achievements, s.math_score, s.physics_score, s.russian_score), reverse=True)
        print("Рейтинг импортирован из файла 'students_ranking.csv'.")
    except FileNotFoundError:
        print("Файл 'students_ranking.csv' не найден.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")

def main():
    students = []

    while True:
        print("\nМеню:")
        print("1. Добавить ученика")
        print("2. Показать рейтинг")
        print("3. Удалить ученика по номеру")
        print("4. Удалить все записи")
        print("5. Экспортировать рейтинг в CSV")
        print("6. Импортировать рейтинг из CSV")
        print("7. Выйти")

        choice = input("Выберите действие (1/2/3/4/5/6/7): ")

        if choice == '1':
            add_student(students)
        elif choice == '2':
            display_ranking(students)
        elif choice == '3':
            delete_student_by_number(students)
        elif choice == '4':
            delete_all_students(students)
        elif choice == '5':
            export_to_csv(students)
        elif choice == '6':
            import_from_csv(students)
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3, 4, 5, 6 или 7.")

if __name__ == "__main__":
    main()
