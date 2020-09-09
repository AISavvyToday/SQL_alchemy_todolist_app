from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def get_day(s):
    weekday = ""
    if s == 0:
        weekday = "Monday"
    elif s == 1:
        weekday = "Tuesday"
    elif s == 2:
        weekday = "Wednesday"
    elif s == 3:
        weekday = "Thursday"
    elif s == 4:
        weekday = "Friday"
    elif s == 5:
        weekday = "Saturday"
    elif s == 6:
        weekday = "Sunday"

    return weekday


def add_task():
    input_str = input("Enter task\n")
    input_deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
    new_row = Table(task=input_str, deadline=input_deadline.date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def query_today():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f"Today {today.day} {today.strftime('%b')}:")
    if len(rows) == 0:
        print("Nothing to do!\n")
    else:
        for i in rows:
            print(i)


def query_week():
    cur_day = datetime.today()
    weekday = ""

    for i in range(7):
        cur_day = datetime.today() + timedelta(days=i)
        weekday = get_day(cur_day.weekday())

        print(weekday, cur_day.day, cur_day.strftime('%b'))
        rows = session.query(Table).filter(Table.deadline == cur_day.date()).all()

        if len(rows) == 0:
            print("Nothing to do!\n")
        else:
            for j in rows:
                print(j, "\n")


def query_all():
    rows = session.query(Table).order_by(Table.deadline).all()

    j = 1
    for i in rows:
        print(f"{j}.{i.task}. {i.deadline.day} {i.deadline.strftime('%b')}")
        j += 1


def query_missed():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    j = 1
    print("Missed tasks:")
    for i in rows:
        print(f"{j}.{i.task}. {i.deadline.day} {i.deadline.strftime('%b')}")
        j += 1


def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    to_delete = int(input("Choose the number of the task you want to delete:"))
    j = 1
    for i in rows:
        print(f"{j}.{i.task}. {i.deadline.day} {i.deadline.strftime('%b')}")
        j += 1
    rows_to_del = session.query(Table).filter(Table.id == to_delete).all()
    if len(rows_to_del) == 0:
        print("Nothing to delete")
    else:
        row_to_del = rows_to_del[0]
        session.delete(row_to_del)
        session.commit()
        print("The task has been deleted!")


while True:
    print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
''')
    order = input()
    if order == "1":
        query_today()
    elif order == "2":
        query_week()
    elif order == "3":
        query_all()
    elif order == "4":
        query_missed()
    elif order == "5":
        add_task()
    elif order == "6":
        delete_task()
    elif order == "0":
        print("Bye!")
        exit()
