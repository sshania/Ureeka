from sqlalchemy import (CheckConstraint, Column, Integer, String, Boolean, ForeignKey, Float, Text, Enum, Date, TIMESTAMP, DECIMAL, DateTime, BigInteger)
from sqlalchemy.orm import relationship, declarative_base

from database import Base

class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    
    
    courses = relationship("Course", back_populates="admin")
    materials = relationship("Materials", back_populates="admin")
    tests = relationship("Tests", back_populates="admin")

class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    join_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    last_login = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    
    enrollments = relationship("Enrollments", back_populates="student")
    tests_attempts = relationship("Tests_Attempts", back_populates="student")
    forum_topics = relationship("Forum_Topics", back_populates="student")
    forum_replies = relationship("Forum_Replies", back_populates="student")
    certificates = relationship("Certificates", back_populates="student")
    # student_answers = relationship("Student_Answers", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
    admin_id = Column(Integer, ForeignKey("admin.admin_id"))
    
    admin = relationship("Admin", back_populates="courses")
    categories = relationship("Categories", back_populates="courses")
    materials = relationship("Materials", back_populates="courses", uselist=True)
    enrollments = relationship("Enrollments", back_populates="courses")
    tests = relationship("Tests", back_populates="courses")
    certificates = relationship("Certificates", back_populates="courses")
    forum_topics = relationship("Forum_Topics", back_populates="courses")

class Categories(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    courses = relationship("Course", back_populates="categories")


class Materials(Base):
    __tablename__ = "materials"
    material_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    enum = Column(Enum("pdf", "video", "slides", "text", name="material_type"))
    upload_at = Column(TIMESTAMP, nullable=False)
    admin_id = Column(Integer, ForeignKey("admin.admin_id"))

    courses = relationship("Course", back_populates="materials")
    admin = relationship("Admin", back_populates="materials")


class Enrollments(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    enrolled_at = Column(TIMESTAMP, nullable=False)
    progress = Column(Float, default=0)
    completed_at = Column(TIMESTAMP)
    certificate_issued = Column(Boolean, default=False)
    
    student = relationship("Student", back_populates="enrollments")
    courses = relationship("Course", back_populates="enrollments")

    __table_args__ = (
        CheckConstraint('progress >= 0 AND progress <= 100', name='check_progress_range'),
    )

class Tests(Base):
    __tablename__ = "tests"
    test_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    pass_percentage = Column(Integer, nullable=False)
    time_limit = Column(Integer, nullable=True)  # in minutes
    created_at = Column(TIMESTAMP, nullable=False)
    admin_id = Column(Integer, ForeignKey("admin.admin_id"))
    
    courses = relationship("Course", back_populates="tests")
    admin = relationship("Admin", back_populates="tests")
    questions = relationship("Questions", back_populates="tests")
    tests_attempts = relationship("Tests_Attempts", back_populates="tests")

class Questions(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("tests.test_id"))
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum("multiple_choice", "true_false", "essay", name="question_type"))
    points = Column(Integer, default=1)
    sequence = Column(Integer, nullable=False)
    
    tests = relationship("Tests", back_populates="questions")
    answers = relationship("Answers", back_populates="questions")
    student_answers = relationship("Student_Answers", back_populates="questions")

class Answers(Base):
    __tablename__ = "answers"
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    explanation = Column(Text, nullable=True)
    
    questions = relationship("Questions", back_populates="answers")
    student_answers = relationship("Student_Answers", back_populates="answers")

class Certificates(Base):
    __tablename__ = "certificates"
    certificate_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    certificate_number = Column(String(100), unique=True, nullable=False)
    issued_at = Column(TIMESTAMP, nullable=False)
    is_valid = Column(Boolean, default=True)
    
    student = relationship("Student", back_populates="certificates")
    courses = relationship("Course", back_populates="certificates")

class Forum_Topics(Base):
    __tablename__ = "forum_topics"
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    student_id = Column(Integer, ForeignKey("student.student_id"))
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    is_pinned = Column(Boolean, default=False)
    is_closed = Column(Boolean, default=False)
    
    courses = relationship("Course", back_populates="forum_topics")
    student = relationship("Student", back_populates="forum_topics")
    forum_replies = relationship("Forum_Replies", back_populates="topic")


class Forum_Replies(Base):
    __tablename__ = "forum_replies"
    reply_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("forum_topics.topic_id"))
    student_id = Column(Integer, ForeignKey("student.student_id"))
    admin_id = Column(Integer, ForeignKey("admin.admin_id"))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    upvotes = Column(Integer, default=0)

    topic = relationship("Forum_Topics", back_populates="forum_replies")
    student = relationship("Student", back_populates="forum_replies")

class Tests_Attempts(Base):
    __tablename__ = "test_attempts"
    attempt_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    test_id = Column(Integer, ForeignKey("tests.test_id"))
    started_at = Column(TIMESTAMP, nullable=False)
    completed_at = Column(TIMESTAMP)
    score = Column(Integer, nullable=True)
    passed = Column(Boolean, nullable=True)
    total_time = Column(Integer, nullable=True)  # in seconds
    
    student = relationship("Student", back_populates="tests_attempts")
    tests = relationship("Tests", back_populates="tests_attempts")
    student_answers = relationship("Student_Answers", back_populates="tests_attempt")

class Student_Answers(Base):
    __tablename__ = "student_answers"
    student_answer_id = Column(Integer, primary_key=True, autoincrement=True)
    # student_id = Column(Integer, ForeignKey("student.student_id"))
    attempt_id = Column(Integer, ForeignKey("test_attempts.attempt_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    answer_id = Column(Integer, ForeignKey("answers.answer_id"))
    essay_answer = Column(Text, nullable=True)
    point_awarded = Column(Integer, nullable=True)
    
    # student = relationship("Student", back_populates="student_answers")  
    questions = relationship("Questions", back_populates="student_answers")
    answers = relationship("Answers", back_populates="student_answers")
    tests_attempt = relationship("Tests_Attempts", back_populates="student_answers")