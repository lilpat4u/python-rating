import csv
import random

# Функция для генерации случайного ФИО
def generate_name():
    first_names = ["Иван", "Петр", "Мария", "Алексей", "Ольга", "Сергей", "Елена", "Андрей", "Наталья", "Владимир"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Федоров", "Александров", "Михайлов", "Николаев", "Сергеев"]
    middle_names = ["Иванович", "Петрович", "Сидорович", "Алексеевич", "Олегович", "Сергеевич", "Владимирович", "Андреевич", "Алексеевна", "Сергеевна"]
    return f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(middle_names)}"

# Функция для генерации случайного балла
def generate_score(min_score=0, max_score=100):
    return random.randint(min_score, max_score)

# Функция для генерации комментариев по условиям
def apply_conditions(math_score, physics_score, informatics_score):
    math_comment = ""
    physics_comment = ""

    if math_score >= 85 and 35 <= physics_score <= 49:
        physics_comment = f"#({physics_score})"
        physics_score = 50
    if physics_score >= 90 and 35 <= math_score <= 49:
        math_comment = f"#({math_score})"
        math_score = 50
    if informatics_score is not None and informatics_score >= 90 and 35 <= math_score <= 49:
        math_comment = f"#({math_score})"
        math_score = 50

    return math_score, physics_score, math_comment, physics_comment

# Генерация данных для 1000 учеников
students_data = []
for _ in range(1000):
    name = generate_name()
    math_score = generate_score()
    physics_score = generate_score()
    russian_score = generate_score()
    informatics_score = generate_score() if random.choice([True, False]) else None
    has_achievements = random.choice(["Да", "Нет"])

    math_score, physics_score, math_comment, physics_comment = apply_conditions(math_score, physics_score, informatics_score)

    if informatics_score is not None:
        total_score = math_score + max(physics_score, informatics_score) + russian_score
    else:
        total_score = math_score + physics_score + russian_score

    students_data.append({
        "ФИО": name,
        "Баллы по математике": f"{math_score}{math_comment}",
        "Баллы по физике": f"{physics_score}{physics_comment}",
        "Баллы по информатике": informatics_score if informatics_score is not None else "",
        "Баллы по русскому языку": russian_score,
        "Общая сумма баллов": total_score,
        "Достижения по олимпиадам": has_achievements
    })

# Запись данных в файл CSV
with open('students_ranking.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ["ФИО", "Баллы по математике", "Баллы по физике", "Баллы по информатике", "Баллы по русскому языку", "Общая сумма баллов", "Достижения по олимпиадам"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for student in students_data:
        writer.writerow(student)

print("Файл 'students_ranking.csv' успешно создан.")
