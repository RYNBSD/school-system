import re
import sqlite3
import datetime as dt

db = sqlite3.connect("school.db")

cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS students (
                    id INTEGER UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    class TEXT NOT NULL,
                    date_registration TEXT NOT NULL,
                    PRIMARY KEY (id)
                )""")

cur.execute("""CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER UNIQUE NOT NULL,
                lesson_name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                PRIMARY KEY (id AUTOINCREMENT)
                FOREIGN KEY (user_id) REFERENCES students (id)
            )""")

db.commit()

def getChoice():

    while True:

        print("لإضافة طالب إضغط على حرف a")
        print("لحذف طالب إضغط على حرف d")
        print("لتعديل معلومات طالب إضغط على حرف u")
        print("لعرض معلومات طالب إضغط على حرف s")
        print("Enter e for echoiceit")

        choice = input("Enter your choice: ")

        if choice == 'a' or choice == 'd' or choice == 'u' or choice == 's' or choice == 'e':
            return choice

def checkStudentID (id):

    data = cur.execute(f"SELECT * FROM students WHERE id = {id}").fetchone()

    if not (data is None):
        return True
    return False

def checkStudentInfo (student):
    data = cur.execute(f"SELECT * FROM students WHERE id={student['id']} AND first_name='{student['first_name']}' AND last_name='{student['last_name']}' AND age={student['age']} AND class='{student['class']}'").fetchone()

    if data is None:
        print("\nCheck your Data\n")
        return True
    return False

def checkLessonName(name, lessons):

    for lsn in lessons:
        if lsn == name:
            print("\nCheck your lesson name (Don't duplicate)\n")
            return True
    return False

def addStudent():
    student = {
        "id": 0,
        "first_name": '',
        "last_name": '',
        "age": 0,
        "class": '',
        "date_registration": '',
    }

    check = True

    while check:

        student["id"] = input("Enter your ID: ")
        student["first_name"] = input("Enter your first name: ")
        student["last_name"] = input("Enter your last name: ")
        student["age"] = input("Enter your age: ")
        student["class"] = input("Enter your class: ")


        if (re.findall("[a-zA-Z]", student["first_name"]) and 
            re.findall("[a-zA-Z]", student["last_name"]) and 
            re.findall("[a-zA-Z1-9]", student["class"]) and 
            re.findall("[1-9]", student["age"]) and 
            re.findall("[1-9]", student["id"])
        ):
            while checkStudentID(student["id"]):
                student["id"] = input("Enter your ID: ")
                
            check = False
        else:
            print("\nCheck your data\n")

    check = True

    lessons = []
    lesson_name = ''

    while check:
        lesson_name = input("Enter your lesson name: ")

        if re.findall("[a-zA-Z]", lesson_name):
            #check for lesson to be not dublicate
            while checkLessonName(lesson_name, lessons):
                lesson_name = input("Enter your lesson name: ")

            check = False
            lessons.append(lesson_name)

            wantMore = input("For more lesson press y else n: ")

            while not (wantMore == 'y' or wantMore == 'n'):
                print("\nCheck your lesson data\n")
                wantMore = input("For more lesson press y else n: ")

            if wantMore == 'y':
                check = True

        else:
            print("\nCheck your data\n")


    
    cur.execute(f"""INSERT INTO students VALUES ({student['id']}, '{student['first_name']}', '{student['last_name']}', {student['age']}, '{student['class']}', '{dt.datetime.now()}')""")

    for lsn in lessons:
        cur.execute(f"""INSERT INTO lessons (lesson_name, user_id) VALUES ('{lsn}', {student["id"]})""")

def deleteData():
    student = {
        "id": 0,
        "first_name": '',
        "last_name": '',
        "age": 0,
        "class": '',
        "date_registration": '',
    }

    check = True

    while check:
        student["id"] = input("Enter your ID: ")
        student["first_name"] = input("Enter your first name: ")
        student["last_name"] = input("Enter your last name: ")
        student["age"] = input("Enter your age: ")
        student["class"] = input("Enter your class: ")

        if (re.findall("[a-zA-Z]", student["first_name"]) and 
            re.findall("[a-zA-Z]", student["last_name"]) and 
            re.findall("[a-zA-Z1-9]", student["class"]) and 
            re.findall("[1-9]", student["age"]) and 
            re.findall("[1-9]", student["id"])
        ):

            while checkStudentInfo(student):
                student["id"] = input("Enter your ID: ")
                student["first_name"] = input("Enter your first name: ")
                student["last_name"] = input("Enter your last name: ")
                student["age"] = input("Enter your age: ")
                student["class"] = input("Enter your class: ")
        
            check = False
        else:
            print("\nCheck your data\n")

    cur.execute(f"""DELETE FROM lessons WHERE user_id={student['id']}""")
    cur.execute(f"""DELETE FROM students 
                        WHERE id={student['id']} AND first_name='{student['first_name']}' AND last_name='{student['last_name']}' AND age={student['age']} AND class='{student['class']}'""")

    print(f"student with id {student['id']} has deleted")
               
def updateData():
    student = {
        "id": 0,
        "first_name": '',
        "last_name": '',
        "age": 0,
        "class": '',
        "date_registration": '',
    }

    check = True

    while check:
        student["id"] = input("Enter your ID: ")
        student["first_name"] = input("Enter your first name: ")
        student["last_name"] = input("Enter your last name: ")
        student["age"] = input("Enter your age: ")
        student["class"] = input("Enter your class: ")

        if (re.findall("[a-zA-Z]", student["first_name"]) and 
            re.findall("[a-zA-Z]", student["last_name"]) and 
            re.findall("[a-zA-Z1-9]", student["class"]) and 
            re.findall("[1-9]", student["age"]) and 
            re.findall("[1-9]", student["id"])
        ):

            while checkStudentInfo(student):
                student["id"] = input("Enter your ID: ")
                student["first_name"] = input("Enter your first name: ")
                student["last_name"] = input("Enter your last name: ")
                student["age"] = input("Enter your age: ")
                student["class"] = input("Enter your class: ")
        
            check = False
        else:
            print("\nCheck your data\n")

    new_student_data = {
        "first_name": '',
        "last_name": '',
        "age": 0,
        "class": '',
        "date_registration": '',
    }

    check = True

    while check:
        new_student_data["first_name"] = input("Enter your new first name: ")
        new_student_data["last_name"] = input("Enter your new last name: ")
        new_student_data["age"] = input("Enter new your age: ")
        new_student_data["class"] = input("Enter new your class: ")

        if (re.findall("[a-zA-Z]", new_student_data["first_name"]) and 
            re.findall("[a-zA-Z]", new_student_data["last_name"]) and 
            re.findall("[a-zA-Z1-9]", new_student_data["class"]) and 
            re.findall("[1-9]", new_student_data["age"])
        ):

            check = False
        else:
            print("\nCheck your data\n")

    cur.execute(f"""UPDATE students set last_name='{new_student_data["last_name"]}', first_name='{new_student_data["first_name"]}', age={new_student_data["age"]}, class='{new_student_data["class"]}' WHERE id={student["id"]} AND last_name='{student["last_name"]}' AND first_name='{student["first_name"]}' AND age={student["age"]} AND class='{student["class"]}'""")

    print("Data updated")

def selectData():
    student = {
        "id": 0,
        "first_name": '',
        "last_name": '',
        "age": 0,
        "class": '',
        "date_registration": '',
    }

    check = True

    while check:
        student["id"] = input("Enter your ID: ")
        student["first_name"] = input("Enter your first name: ")
        student["last_name"] = input("Enter your last name: ")
        student["age"] = input("Enter your age: ")
        student["class"] = input("Enter you class: ")

        if (re.findall("[a-zA-Z]", student["first_name"]) and 
            re.findall("[a-zA-Z]", student["last_name"]) and 
            re.findall("[a-zA-Z1-9]", student["class"]) and 
            re.findall("[1-9]", student["age"]) and 
            re.findall("[1-9]", student["id"])
        ):

            while checkStudentInfo(student):
                student["id"] = input("Enter your ID: ")
                student["first_name"] = input("Enter your first name: ")
                student["last_name"] = input("Enter your last name: ")
                student["age"] = input("Enter your age: ")
                student["class"] = input("Enter you class: ")
        
            check = False
        elif re.findall("[1-9]", student["id"]):

            if student["first_name"] or student["last_name"] or student["age"] or student["class"]:
                print("\nCheck your data\n")
            else:
                while not checkStudentID(student["id"]):
                    student["id"] = input("Enter your ID: ")
            
            check = False
        else:
            print("\nCheck your data\n")

    result = cur.execute(f"""SELECT students.id, students.first_name, students.last_name, students.age, students.class, students.date_registration, lessons.lesson_name 
                        FROM students
                        LEFT JOIN lessons
                        WHERE students.id = lessons.user_id AND students.id = {student['id']}""")

    print(f"\n{result.fetchall()}\n")

def main():

    while True:
        choice = getChoice()

        if choice == 'e':
            db.close()
            return
        elif choice == 'a':
            addStudent()
            db.commit()
        elif choice == 'd':
            deleteData()
            db.commit()
        elif choice == 'u':
            updateData()
            db.commit()
        elif choice == 's':
            selectData()
            db.commit()
        else:
            print("wrong choice")

if __name__ == "__main__":
    main()