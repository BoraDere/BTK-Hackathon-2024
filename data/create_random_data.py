import json
import random

names = [
    'Ahmet', 
    'Mehmet', 
    'Ali', 
    'Hasan', 
    'Hüseyin', 
    'Ayşe', 
    'Sude', 
    'Ceren', 
    'Nazlı', 
    'Zeynep', 
    'Mustafa', 
    'Barış', 
    'Kemal', 
    'Bora', 
    'Yusuf', 
]

last_names = [
    'Kaya',
    'Demir',
    'Çelik',
    'Şahin',
    'Koç',
    'Kurt',
    'Öztürk',
    'Arslan',
    'Kara',
    'Taş',
    'Kaplan',
    'Kılıç',
    'Aydın',
    'Güneş',
    'Keskin',
]

def load_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_random_study_plan(n, metadata, k):
    for _ in range(n):
        # Choose a random grade
        grade = random.choice(metadata['Grades'])
        grade_number = grade['Grade']
        
        courses = random.sample(grade['Courses'], k=k)
        
        course_names = [course['Course'] for course in courses]
        books_solved = []
        topics_missed = []
        
        for course in courses:
            topics = random.sample(course['Topics'], k=k)
            topics_missed.append(f"{course['Course']}: {', '.join(topics)}")
        
        books = random.sample(metadata['Books'], k=k)
        books_solved.append(f"{course['Course']}: {', '.join(books)}")

        name = random.choice(names)
        last_name = random.choice(last_names)
        
        output = f"Name: {name}; Last name: {last_name}; Education: High school; Class: {grade_number}; Courses: {', '.join(course_names)}; Books Solved: {', '.join(books_solved)}; Topics Missed: {', '.join(topics_missed)}\n"

        with open(f"data.txt", 'a', encoding='utf-8') as file:
            file.write(output)

metadata = load_metadata('metadata.json')

with open(f"data.txt", 'a', encoding='utf-8') as file:
    file.write('Higher quality data:\n')
generate_random_study_plan(10, metadata, 5)

with open(f"data.txt", 'a', encoding='utf-8') as file:
    file.write('\nAverage quality data:\n')
generate_random_study_plan(10, metadata, 3)

with open(f"data.txt", 'a', encoding='utf-8') as file:
    file.write('\nLower quality data:\n')
generate_random_study_plan(5, metadata, 2)