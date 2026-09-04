from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import insert, update, delete, func, asc, desc
from sqlalchemy.orm import sessionmaker
import json

with open('config.json') as f:
    config = json.load(f)

db_user = config['database']['user']
db_password = config['database']['password']
db_access = config['database']['access']
db = 'Academy'

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/{db}'
engine = create_engine(db_url)

metadata = MetaData()
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_row(table_name):
    # table_name = 'users'
    table = metadata.tables.get(table_name)
    columns = table.columns.keys()
    values = {}
    for column in columns:
        value = input(f"Enter value for column {column}: ")
        values[column] = value

    try:
        query = insert(table).values(values)
        session.execute(query)
        session.commit()
        print("data successfully inserted")
    except Exception as e:
        print(f"Error: {str(e)}")
        session.rollback()


def update_row(table_name):
    # table_name = 'users'
    table = metadata.tables.get(table_name)
    columns = table.columns.keys()
    search_id = int(input("Select id to update: "))
    new_values = {}
    for column in columns:
        value = input(f"Enter new value for column {column}: ")
        new_values[column] = value

    try:
        query = update(table).where(table.c.id == search_id).values(new_values)
        session.execute(query)
        session.commit()
        print("successfull update")
    except Exception as e:
        print(f"Query error: {str(e)}")
        session.rollback()


def delete_row(table_name):
    # table_name = 'users'
    table = metadata.tables.get(table_name)
    search_id = int(input("Select id to delete: "))

    try:
        query = delete(table).where(table.c.id == search_id)
        session.execute(query)
        session.commit()
        print("successfull delete")
    except Exception as e:
        print(f"Query error: {str(e)}")
        session.rollback()


def save_data(file_path, data):
    with open(file_path, 'w') as wfile:
        wfile.write(data)
        print("data saved")


def execute_queries():
    print("вивести інформацію про всі навчальні групи")
    groups = metadata.tables.get('groups')
    results = session.query(groups).all()

    for row in results:
        print(row._asdict())
    print("--" * 20)

    print("вивести інформацію про всіх викладачів,")
    teachers = metadata.tables.get("teachers")
    results = session.query(teachers).all()

    for row in results:
        print(row._asdict())
    print("--" * 20)

    print("вивести назви усіх кафедр")
    departments = metadata.tables.get('departments')
    results = session.query(departments.c.name).all()

    for row in results:
        print(row)
    print("--" * 20)

    print("вивести імена та прізвища викладачів, які читають лекції в конкретній групі,")
    teachers = metadata.tables.get('teachers')
    groups_lectures = metadata.tables.get('groupslectures')
    lectures = metadata.tables.get("lectures")
    group_id = 1
    results = session.query(teachers.c.name, teachers.c.surname) \
        .join(lectures, teachers.c.id == lectures.c.teacherid) \
        .join(groups_lectures, groups_lectures.c.lectureid == lectures.c.id) \
        .filter(groups_lectures.c.groupid == group_id)

    for row in results:
        print(f"""
        teacher: {row.name} {row.surname}
        """)
    print("--" * 20)

    print("вивести назви кафедр і груп, які до них відносяться,")
    results = session.query(departments.c.name.label('d_name'), groups.c.name.label('g_name')) \
        .filter(groups.c.departmentid == departments.c.id)

    for row in results:
        print(row._asdict())
    print("--" * 20)

    print(" відобразити кафедру з максимальною кількістю груп,")
    result = session.query(departments.c.name, func.count(groups.c.id).label('group_count')) \
        .join(groups, departments.c.id == groups.c.departmentid) \
        .group_by(departments.c.id) \
        .order_by(func.count(groups.c.id).desc()) \
        .first()

    print(f"Department with the maximum number of groups:")
    print(f"Department Name: {result.name}")
    print(f"Number of Groups: {result.group_count}")
    print("--" * 20)

    print("відобразити кафедру з мінімальною кількістю груп")
    result = session.query(departments.c.name, func.count(groups.c.id).label('group_count')) \
        .join(groups, departments.c.id == groups.c.departmentid) \
        .group_by(departments.c.id) \
        .order_by(func.count(groups.c.id).asc()) \
        .first()

    print(f"Department with the minimum number of groups:")
    print(f"Department Name: {result.name}")
    print(f"Number of Groups: {result.group_count}")
    print("--" * 20)

    print("вивести назви предметів, які викладає конкретний викладач,")
    subjects = metadata.tables.get('subjects')
    teacher_id = 2
    results = session.query(subjects.c.name) \
        .join(lectures, lectures.c.subjectid == subjects.c.id) \
        .join(teachers, teachers.c.id == lectures.c.teacherid) \
        .filter(teachers.c.id == teacher_id)

    for row in results:
        print(row.name)
    print("--" * 20)

    print("▷ вивести назви кафедр, на яких викладається конкретна дисципліна,")
    faculties = metadata.tables.get('faculties')
    faculty_id = 1
    results = session.query(departments.c.name).filter(departments.c.facultyid == faculty_id)
    for row in results:
        print(row.name)
    print("--" * 20)

    print("вивести назви груп, що належать до конкретного факультету,")
    results = session.query(groups.c.name) \
        .join(departments, departments.c.id == groups.c.departmentid) \
        .join(faculties, faculties.c.id == departments.c.facultyid) \
        .filter(faculties.c.id == faculty_id)
    for row in results:
        print(row.name)
    print("--" * 20)

    print("вивести назви предметів та повні імена викладачів, які читають найбільшу кількість лекцій з них,")

    result = session.query(subjects.c.name.label('subject_name'),
                           func.concat(teachers.c.name, ' ', teachers.c.surname).label('full_name'),
                           func.count(lectures.c.id).label('lecture_count')) \
        .join(lectures, subjects.c.id == lectures.c.subjectid) \
        .join(teachers, teachers.c.id == lectures.c.teacherid) \
        .group_by(subjects.c.id, teachers.c.id) \
        .order_by(func.count(lectures.c.id).desc()) \
        .first()

    print(f"Subject with the most lectures and corresponding teacher:")
    print(f"Subject Name: {result.subject_name}")
    print(f"Teacher Full Name: {result.full_name}")
    print(f"Lecture Count: {result.lecture_count}")
    print("--" * 20)

    print("вивести назву предмету, за яким читається найменше лекцій,")

    result = session.query(subjects.c.name.label('subject_name'),
                           func.count(lectures.c.id).label('lecture_count')) \
        .join(lectures, subjects.c.id == lectures.c.subjectid) \
        .group_by(subjects.c.id) \
        .order_by(func.count(lectures.c.id).asc()) \
        .first()

    print(f"Subject Name: {result.subject_name}")
    print(f"Lecture Count: {result.lecture_count}")
    print("--" * 20)

    print("вивести назву предмету, за яким читається найбільше лекцій;")
    result = session.query(subjects.c.name.label('subject_name'),
                           func.count(lectures.c.id).label('lecture_count')) \
        .join(lectures, subjects.c.id == lectures.c.subjectid) \
        .group_by(subjects.c.id) \
        .order_by(func.count(lectures.c.id).desc()) \
        .first()

    print(f"Subject Name: {result.subject_name}")
    print(f"Lecture Count: {result.lecture_count}")
    print("--" * 20)


while True:
    if db_access.lower() == 'admin':
        print("Choose Table: ")
        for table_name in metadata.tables.keys():
            print(table_name)
        table_name = input("\nEnter table name or 0 to exit: ")

        if table_name == '0':
            break

        if table_name in metadata.tables:
            table = metadata.tables[table_name]
            print(f"\n{table_name}\n")

            print("1. Вставити рядки")
            print("2. Оновити рядки")
            print("3. Видалити рядки")
            print("4. execute all queries ")
            print("0. Вийти")

            choice = input("Оберіть опцію: ")
            if choice == "0":
                break
            elif choice == "1":
                add_row(table)
            elif choice == "2":
                update_row(table)
            elif choice == "3":
                delete_row(table)
            elif choice == "4":
                execute_queries()

            else:
                print("Невірний вибір. Будь ласка, оберіть знову.")
        else:
            print("Такої таблиці не існує. Будь ласка, введіть правильну назву.")
    else:
        isExecute = input("You can only execute queries, execute it? y/n: ")
        if isExecute.lower() == 'y':
            execute_queries()
        else:
            break

session.close()