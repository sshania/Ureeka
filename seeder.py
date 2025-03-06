from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import Base
from models import Admin, Student, Course, Categories, Enrollments, Materials, Tests, Questions, Answers, Certificates, Forum_Topics, Forum_Replies,Tests_Attempts, Student_Answers

DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/ureekaCourse"


# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

# Seed data
def seed_data():
    # Create a new session
    with Session(bind=engine) as session:
            try:
                # Seed Admins
                admins = [
                Admin(username='admin1', email='admin1@example.com', password_hash='hashedpassword1', first_name='John', last_name='Doe', created_at=datetime(2024, 3, 1, 8, 0), is_active=True),
                Admin(username='admin2', email='admin2@example.com', password_hash='hashedpassword2', first_name='Jane', last_name='Smith', created_at=datetime(2024, 3, 2, 9, 0), is_active=True)
                ]
                session.add_all(admins)

                # Seed Students
                students = [
                    Student(username='student1', email='student1@example.com', password_hash='hashedpassword3', first_name='Alice', last_name='Johnson', join_date=datetime(2023, 9, 1), created_at=datetime(2023, 9, 1, 10, 0), last_login=datetime(2024, 2, 1, 12, 0), is_active=True),
                    Student(username='student2', email='student2@example.com', password_hash='hashedpassword4', first_name='Bob', last_name='Brown', join_date=datetime(2023, 9, 10), created_at=datetime(2023, 9, 10, 11, 0), last_login=datetime(2024, 2, 2, 13, 0), is_active=True)
                ]
                session.add_all(students)

                # Seed Categories
                categories = [
                    Categories(name='Programming', description='Courses related to coding and development'),
                    Categories(name='Databases', description='Courses about database management and SQL')
                ]
                session.add_all(categories)

                # Seed Courses
                courses = [
                    Course(title='Introduction to Programming', description='Learn basic programming concepts.', category_id=1, created_at=datetime(2024, 1, 1, 8, 0), updated_at=datetime(2024, 1, 10, 10, 0), admin_id=1),
                    Course(title='Database Management', description='Understanding relational databases.', category_id=2, created_at=datetime(2024, 2, 1, 9, 0), updated_at=datetime(2024, 2, 5, 11, 0), admin_id=2)
                ]
                session.add_all(courses)

                # Seed Materials
                materials = [
                    Materials(course_id=1, title='Python Basics', description='Introduction to Python programming.', enum='pdf', upload_at=datetime(2024, 1, 5, 10, 0), admin_id=1),
                    Materials(course_id=2, title='SQL Queries', description='Learning how to write SQL queries.', enum='slides', upload_at=datetime(2024, 2, 7, 11, 0), admin_id=2)
                ]
                session.add_all(materials)

                # Seed Enrollments
                enrollments = [
                    Enrollments(student_id=1, course_id=1, enrolled_at=datetime(2024, 1, 15, 9, 0), progress=75.0, completed_at=None, certificate_issued=False),
                    Enrollments(student_id=2, course_id=2, enrolled_at=datetime(2024, 2, 10, 10, 30), progress=100.0, completed_at=datetime(2024, 3, 1, 15, 0), certificate_issued=True)
                ]
                session.add_all(enrollments)

                # Seed Tests
                tests = [
                    Tests(course_id=1, title='Intro to Programming Quiz', description='Basic programming questions.', pass_percentage=60, time_limit=30, created_at=datetime(2024, 1, 20, 8, 0), admin_id=1),
                    Tests(course_id=2, title='SQL Basics Test', description='Fundamentals of SQL.', pass_percentage=70, time_limit=45, created_at=datetime(2024, 2, 15, 9, 0), admin_id=2)
                ]
                session.add_all(tests)

                # Commit all changes in one transaction
                session.commit()
                print("Database seeding successful!")

            except Exception as e:
                session.rollback()
                print(f"Error occurred while seeding data: {e}")
            finally:
                session.close()


# Run the seeder
if __name__ == "__main__":
    seed_data()