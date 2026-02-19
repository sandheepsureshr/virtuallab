from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lab.models import (Subject, Chapter, Topic, QuizQuestion, StudentProfile)


class Command(BaseCommand):
    help = 'Seed the database with demo subjects, chapters, topics and quiz questions'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with demo data...\n')

        # ── Admin User ────────────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@virtuallab.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Admin created: admin / admin123'))
        else:
            self.stdout.write('  Admin already exists.')

        # ── Demo Student ──────────────────────────────────────────────────────
        if not User.objects.filter(username='student1').exists():
            student = User.objects.create_user(
                'student1', 'student@example.com', 'student123',
                first_name='John', last_name='Doe'
            )
            StudentProfile.objects.create(user=student, institution='Demo University')
            self.stdout.write(self.style.SUCCESS('✅ Student created: student1 / student123'))
        else:
            self.stdout.write('  Student already exists.')

        # ═══════════════════════════════════════════════════════════════
        # SUBJECT 1: Python Programming
        # ═══════════════════════════════════════════════════════════════
        python_subj, _ = Subject.objects.get_or_create(
            title='Python Programming',
            defaults={
                'description': 'Master Python from basics to advanced OOP, file handling, and modules.',
                'category': 'programming',
                'icon': 'code',
                'color': '#3b82f6',
                'order': 1,
                'is_active': True,
            }
        )
        self.stdout.write(f'  Subject: {python_subj.title}')

        # Chapter 1: Introduction to Python
        py_ch1, _ = Chapter.objects.get_or_create(
            subject=python_subj,
            title='Introduction to Python',
            defaults={'description': 'Variables, data types, and basic syntax', 'order': 1, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=py_ch1, title='What is Python?',
            defaults={
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/Y8Tko2YC5hA',
                'content': '''<h2>What is Python?</h2>
<p>Python is a high-level, interpreted programming language known for its simplicity and readability.
Created by <strong>Guido van Rossum</strong> in 1991, Python has become one of the most popular programming
languages in the world.</p>

<h3>Key Features of Python</h3>
<ul>
  <li><strong>Easy to Read:</strong> Python syntax closely resembles English</li>
  <li><strong>Interpreted:</strong> Code runs line by line — no compilation needed</li>
  <li><strong>Dynamically Typed:</strong> No need to declare variable types</li>
  <li><strong>Multi-paradigm:</strong> Supports OOP, functional, and procedural programming</li>
  <li><strong>Huge Standard Library:</strong> "Batteries included" philosophy</li>
</ul>

<h3>Your First Python Program</h3>
<pre><code>
# This is a comment
print("Hello, World!")

# Variables
name = "VirtualLab"
version = 3.11
is_awesome = True

print(f"Welcome to {name} version {version}!")
</code></pre>

<h3>Python Use Cases</h3>
<ul>
  <li>🌐 Web Development (Django, Flask, FastAPI)</li>
  <li>🤖 Artificial Intelligence &amp; Machine Learning</li>
  <li>📊 Data Science &amp; Visualization</li>
  <li>🔒 Cybersecurity &amp; Automation</li>
  <li>🎮 Game Development (Pygame)</li>
</ul>

<blockquote>
  "Python is an experiment in how much freedom programmers need." — Guido van Rossum
</blockquote>

<h3>Summary</h3>
<p>Python is beginner-friendly yet powerful enough for professional development. In this course you will
learn Python from the ground up through practical examples and exercises.</p>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=py_ch1, title='Variables and Data Types',
            defaults={
                'order': 2,
                'video_url': 'https://www.youtube.com/embed/cQT33yu9pY8',
                'content': '''<h2>Variables and Data Types in Python</h2>
<p>A variable is a container that stores data. Python creates a variable when you first assign a value to it —
no declaration keyword needed.</p>

<h3>Core Data Types</h3>
<table>
  <tr><th>Type</th><th>Example</th><th>Description</th></tr>
  <tr><td><code>int</code></td><td><code>age = 25</code></td><td>Whole numbers</td></tr>
  <tr><td><code>float</code></td><td><code>pi = 3.14</code></td><td>Decimal numbers</td></tr>
  <tr><td><code>str</code></td><td><code>name = "Alice"</code></td><td>Text strings</td></tr>
  <tr><td><code>bool</code></td><td><code>active = True</code></td><td>True or False</td></tr>
  <tr><td><code>list</code></td><td><code>nums = [1, 2, 3]</code></td><td>Ordered, mutable collection</td></tr>
  <tr><td><code>tuple</code></td><td><code>point = (3, 4)</code></td><td>Ordered, immutable collection</td></tr>
  <tr><td><code>dict</code></td><td><code>info = {"a": 1}</code></td><td>Key-value pairs</td></tr>
  <tr><td><code>set</code></td><td><code>items = {1, 2, 3}</code></td><td>Unique unordered collection</td></tr>
</table>

<h3>Code Examples</h3>
<pre><code>
# Numbers
age = 25            # int
gpa = 3.85          # float

# Strings
name = "VirtualLab"
greeting = f"Hello, {name}!"  # f-string formatting
print(greeting)     # Hello, VirtualLab!

# Lists (mutable)
subjects = ["Python", "DBMS", "Algorithms"]
subjects.append("Networks")
print(subjects[0])  # Python

# Dictionary
student = {"name": "Alice", "grade": 90, "passed": True}
print(student["name"])  # Alice

# Type checking and conversion
x = int("42")      # str -> int
y = str(100)       # int -> str
z = float("3.14")  # str -> float
print(type(x))     # &lt;class 'int'&gt;
</code></pre>

<blockquote>
Python is <em>dynamically typed</em> — the type is inferred at runtime. Use <code>type(var)</code> to
check the type of any variable.
</blockquote>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=py_ch1, title='Operators in Python',
            defaults={
                'order': 3,
                'content': '''<h2>Operators in Python</h2>
<p>Operators are symbols that perform operations on values and variables.</p>

<h3>Arithmetic Operators</h3>
<pre><code>
a, b = 10, 3

print(a + b)   # 13  — Addition
print(a - b)   # 7   — Subtraction
print(a * b)   # 30  — Multiplication
print(a / b)   # 3.33 — Division (always float)
print(a // b)  # 3   — Floor division
print(a % b)   # 1   — Modulo (remainder)
print(a ** b)  # 1000 — Exponentiation
</code></pre>

<h3>Comparison Operators</h3>
<pre><code>
x = 5
print(x == 5)  # True
print(x != 3)  # True
print(x > 3)   # True
print(x <= 5)  # True
</code></pre>

<h3>Logical Operators</h3>
<pre><code>
a, b = True, False
print(a and b)  # False
print(a or b)   # True
print(not a)    # False
</code></pre>

<h3>Assignment Operators</h3>
<pre><code>
x = 10
x += 5   # x = x + 5 = 15
x -= 3   # x = x - 3 = 12
x *= 2   # x = x * 2 = 24
x //= 4  # x = x // 4 = 6
</code></pre>'''
            }
        )

        # Quiz for Chapter 1
        if not py_ch1.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=py_ch1, order=1, marks=1,
                    question_text='What year was Python first released?',
                    option_a='1985', option_b='1991', option_c='1998', option_d='2004',
                    correct_answer='B',
                    explanation='Python was created by Guido van Rossum and first released in 1991.'),
                QuizQuestion(chapter=py_ch1, order=2, marks=1,
                    question_text='Which function is used to display output in Python?',
                    option_a='output()', option_b='echo()', option_c='print()', option_d='display()',
                    correct_answer='C',
                    explanation='print() is the built-in function to display output to the console.'),
                QuizQuestion(chapter=py_ch1, order=3, marks=1,
                    question_text='Which of the following is a valid Python variable name?',
                    option_a='2name', option_b='my_name', option_c='my-name', option_d='my name',
                    correct_answer='B',
                    explanation='Variable names can contain letters, digits, and underscores but cannot start with a digit or contain spaces/hyphens.'),
                QuizQuestion(chapter=py_ch1, order=4, marks=1,
                    question_text='What data type stores True or False values?',
                    option_a='int', option_b='str', option_c='float', option_d='bool',
                    correct_answer='D',
                    explanation='The bool type stores boolean values: True or False.'),
                QuizQuestion(chapter=py_ch1, order=5, marks=1,
                    question_text='What is the result of 10 // 3 in Python?',
                    option_a='3.33', option_b='3', option_c='1', option_d='0.33',
                    correct_answer='B',
                    explanation='// is floor division — it returns the integer part of the division result.'),
            ])
            self.stdout.write('    ✅ Python Ch1 quiz added')

        # Chapter 2: Control Flow & Functions
        py_ch2, _ = Chapter.objects.get_or_create(
            subject=python_subj,
            title='Control Flow & Functions',
            defaults={'description': 'if/else, loops, and reusable functions', 'order': 2, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=py_ch2, title='Conditional Statements',
            defaults={
                'order': 1,
                'content': '''<h2>Conditional Statements</h2>
<p>Conditional statements allow your program to make decisions and run different code based on conditions.</p>

<h3>if / elif / else</h3>
<pre><code>
age = 18

if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")
</code></pre>

<h3>Ternary (One-line) Expression</h3>
<pre><code>
score = 75
result = "Pass" if score >= 60 else "Fail"
print(result)  # Pass
</code></pre>

<h3>Nested Conditions</h3>
<pre><code>
x = 15
if x > 0:
    if x % 2 == 0:
        print("Positive even")
    else:
        print("Positive odd")
else:
    print("Not positive")
# Output: Positive odd
</code></pre>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=py_ch2, title='Loops',
            defaults={
                'order': 2,
                'content': '''<h2>Loops in Python</h2>
<p>Loops allow you to repeat a block of code multiple times.</p>

<h3>for Loop</h3>
<pre><code>
# Iterate over a range
for i in range(5):
    print(i)    # 0 1 2 3 4

# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# range with start and step
for i in range(0, 10, 2):
    print(i)    # 0 2 4 6 8
</code></pre>

<h3>while Loop</h3>
<pre><code>
count = 0
while count < 5:
    print(count)
    count += 1

# while with break
n = 0
while True:
    if n >= 3:
        break
    print(n)
    n += 1
</code></pre>

<h3>Loop Control: break, continue, pass</h3>
<pre><code>
for i in range(10):
    if i == 5:
        break       # stop the loop
    if i % 2 == 0:
        continue    # skip even numbers
    print(i)        # prints 1 3
</code></pre>

<h3>List Comprehension</h3>
<pre><code>
squares = [x**2 for x in range(6)]
print(squares)  # [0, 1, 4, 9, 16, 25]

evens = [x for x in range(20) if x % 2 == 0]
print(evens)    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
</code></pre>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=py_ch2, title='Functions',
            defaults={
                'order': 3,
                'content': '''<h2>Functions in Python</h2>
<p>Functions are reusable blocks of code defined with the <code>def</code> keyword.</p>

<h3>Defining and Calling Functions</h3>
<pre><code>
def greet(name):
    return f"Hello, {name}!"

message = greet("Alice")
print(message)  # Hello, Alice!
</code></pre>

<h3>Default Parameters</h3>
<pre><code>
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Bob"))           # Hello, Bob!
print(greet("Bob", "Hi"))     # Hi, Bob!
</code></pre>

<h3>*args and **kwargs</h3>
<pre><code>
def add(*args):
    return sum(args)

print(add(1, 2, 3, 4))  # 10

def describe(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

describe(name="Alice", age=22, city="Delhi")
</code></pre>

<h3>Lambda Functions</h3>
<pre><code>
square = lambda x: x ** 2
print(square(5))   # 25

nums = [3, 1, 4, 1, 5]
nums.sort(key=lambda x: -x)
print(nums)        # [5, 4, 3, 1, 1]
</code></pre>

<blockquote>
Functions promote <strong>DRY (Don't Repeat Yourself)</strong> programming. Write once, use many times.
</blockquote>'''
            }
        )

        if not py_ch2.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=py_ch2, order=1, marks=1,
                    question_text='Which keyword defines a function in Python?',
                    option_a='function', option_b='define', option_c='def', option_d='func',
                    correct_answer='C',
                    explanation='The def keyword is used to define a function in Python.'),
                QuizQuestion(chapter=py_ch2, order=2, marks=1,
                    question_text='What does range(1, 6) produce?',
                    option_a='[1,2,3,4,5,6]', option_b='[0,1,2,3,4,5]',
                    option_c='[1,2,3,4,5]', option_d='[1,2,3,4,5,6,7]',
                    correct_answer='C',
                    explanation='range(start, stop) produces numbers from start up to (but not including) stop.'),
                QuizQuestion(chapter=py_ch2, order=3, marks=1,
                    question_text='Which statement immediately exits a loop?',
                    option_a='exit', option_b='stop', option_c='continue', option_d='break',
                    correct_answer='D',
                    explanation='break immediately terminates the loop execution.'),
                QuizQuestion(chapter=py_ch2, order=4, marks=1,
                    question_text='What does the continue statement do in a loop?',
                    option_a='Exits the loop', option_b='Skips the rest of the current iteration',
                    option_c='Pauses the loop', option_d='Restarts the loop',
                    correct_answer='B',
                    explanation='continue skips the remaining code in the current iteration and moves to the next.'),
            ])
            self.stdout.write('    ✅ Python Ch2 quiz added')

        # Chapter 3: OOP
        py_ch3, _ = Chapter.objects.get_or_create(
            subject=python_subj,
            title='Object-Oriented Programming',
            defaults={'description': 'Classes, objects, inheritance and encapsulation', 'order': 3, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=py_ch3, title='Classes and Objects',
            defaults={
                'order': 1,
                'content': '''<h2>Classes and Objects</h2>
<p>OOP models real-world entities as <strong>objects</strong> that have attributes (data) and methods (behavior).</p>

<h3>Defining a Class</h3>
<pre><code>
class Student:
    # Class attribute
    school = "VirtualLab Academy"

    # Constructor (initializer)
    def __init__(self, name, age, grade):
        self.name = name      # instance attribute
        self.age = age
        self.grade = grade

    # Method
    def introduce(self):
        return f"Hi, I am {self.name}, aged {self.age}."

    def is_passing(self):
        return self.grade >= 60

# Create objects (instances)
s1 = Student("Alice", 20, 85)
s2 = Student("Bob", 22, 55)

print(s1.introduce())       # Hi, I am Alice, aged 20.
print(s1.is_passing())      # True
print(s2.is_passing())      # False
print(Student.school)       # VirtualLab Academy
</code></pre>

<h3>Inheritance</h3>
<pre><code>
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"

class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)     # call parent constructor
        self.subject = subject

    def teach(self):
        return f"{self.name} teaches {self.subject}"

t = Teacher("Dr. Smith", "Python")
print(t.greet())    # Hello, I am Dr. Smith
print(t.teach())    # Dr. Smith teaches Python
</code></pre>

<blockquote>
The four pillars of OOP are: <strong>Encapsulation</strong>, <strong>Abstraction</strong>,
<strong>Inheritance</strong>, and <strong>Polymorphism</strong>.
</blockquote>'''
            }
        )

        if not py_ch3.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=py_ch3, order=1, marks=1,
                    question_text='What is the constructor method called in Python?',
                    option_a='__start__', option_b='__init__', option_c='__new__', option_d='__constructor__',
                    correct_answer='B',
                    explanation='__init__ is the special constructor method called automatically when an object is created.'),
                QuizQuestion(chapter=py_ch3, order=2, marks=1,
                    question_text='Which keyword is used to inherit from a parent class?',
                    option_a='inherits', option_b='extends', option_c='super', option_d='The parent class name in parentheses',
                    correct_answer='D',
                    explanation='In Python, you inherit by putting the parent class name in parentheses: class Child(Parent).'),
                QuizQuestion(chapter=py_ch3, order=3, marks=1,
                    question_text='What does self refer to in a class method?',
                    option_a='The class itself', option_b='The current instance of the class',
                    option_c='The parent class', option_d='A global variable',
                    correct_answer='B',
                    explanation='self refers to the current object instance, allowing access to its attributes and methods.'),
            ])
            self.stdout.write('    ✅ Python Ch3 quiz added')

        # ═══════════════════════════════════════════════════════════════
        # SUBJECT 2: Database Management Systems
        # ═══════════════════════════════════════════════════════════════
        dbms_subj, _ = Subject.objects.get_or_create(
            title='Database Management Systems',
            defaults={
                'description': 'Learn relational databases, SQL queries, normalization, transactions and indexing.',
                'category': 'database',
                'icon': 'database',
                'color': '#10b981',
                'order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(f'  Subject: {dbms_subj.title}')

        # Chapter 1: Introduction to Databases
        db_ch1, _ = Chapter.objects.get_or_create(
            subject=dbms_subj,
            title='Introduction to Databases',
            defaults={'description': 'What are databases, DBMS, and relational model', 'order': 1, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=db_ch1, title='What is a Database?',
            defaults={
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/wR0jg0eQsZA',
                'content': '''<h2>What is a Database?</h2>
<p>A <strong>database</strong> is an organized collection of structured data stored electronically in a computer system.
A <strong>Database Management System (DBMS)</strong> is software that manages, controls, and provides access to that data.</p>

<h3>Why Use a Database?</h3>
<ul>
  <li>✅ Eliminate data redundancy and inconsistency</li>
  <li>✅ Enable multi-user concurrent access</li>
  <li>✅ Enforce data integrity and security</li>
  <li>✅ Provide efficient querying and retrieval</li>
  <li>✅ Support backup, recovery, and transactions</li>
</ul>

<h3>Types of Databases</h3>
<table>
  <tr><th>Type</th><th>Description</th><th>Examples</th></tr>
  <tr><td>Relational (RDBMS)</td><td>Data in tables with rows &amp; columns</td><td>MySQL, PostgreSQL, Oracle, SQLite</td></tr>
  <tr><td>NoSQL</td><td>Flexible schemas: documents, key-value, graph</td><td>MongoDB, Redis, Neo4j, Cassandra</td></tr>
  <tr><td>In-Memory</td><td>Data stored in RAM for ultra-fast access</td><td>Redis, Memcached</td></tr>
  <tr><td>Cloud</td><td>Managed databases on cloud platforms</td><td>AWS RDS, Google Cloud SQL, Azure SQL</td></tr>
</table>

<h3>Key Terminology</h3>
<table>
  <tr><th>Term</th><th>Definition</th></tr>
  <tr><td>Table / Relation</td><td>A collection of related data in rows and columns</td></tr>
  <tr><td>Row / Tuple</td><td>A single record in a table</td></tr>
  <tr><td>Column / Attribute</td><td>A field representing one property of the data</td></tr>
  <tr><td>Primary Key (PK)</td><td>Unique identifier for each row — cannot be NULL</td></tr>
  <tr><td>Foreign Key (FK)</td><td>A field referencing the PK of another table</td></tr>
  <tr><td>Schema</td><td>The structure/definition of a database</td></tr>
</table>

<blockquote>
"Without data, you are just another person with an opinion." — W. Edwards Deming
</blockquote>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=db_ch1, title='SQL Fundamentals',
            defaults={
                'order': 2,
                'content': '''<h2>SQL Fundamentals</h2>
<p><strong>SQL (Structured Query Language)</strong> is the universal language for relational databases.
SQL commands are grouped into four categories:</p>

<h3>DDL — Data Definition Language</h3>
<pre><code>
-- Create a new table
CREATE TABLE students (
    id       INT PRIMARY KEY AUTO_INCREMENT,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(150) UNIQUE,
    age      INT,
    grade    DECIMAL(5,2),
    joined   DATE DEFAULT CURRENT_DATE
);

-- Modify table structure
ALTER TABLE students ADD COLUMN city VARCHAR(100);
ALTER TABLE students DROP COLUMN city;

-- Remove table permanently
DROP TABLE students;
</code></pre>

<h3>DML — Data Manipulation Language</h3>
<pre><code>
-- Insert records
INSERT INTO students (name, email, age, grade)
VALUES ('Alice Smith', 'alice@example.com', 20, 88.5);

INSERT INTO students (name, email, age, grade) VALUES
  ('Bob Jones',  'bob@example.com',   22, 76.0),
  ('Carol White','carol@example.com', 21, 92.5);

-- Query records
SELECT * FROM students;
SELECT name, grade FROM students WHERE grade >= 80;
SELECT * FROM students ORDER BY grade DESC LIMIT 5;

-- Update records
UPDATE students SET grade = 95.0 WHERE name = 'Alice Smith';

-- Delete records
DELETE FROM students WHERE age < 18;
</code></pre>

<h3>Aggregate Functions</h3>
<pre><code>
SELECT COUNT(*)       AS total_students  FROM students;
SELECT AVG(grade)     AS average_grade   FROM students;
SELECT MAX(grade)     AS highest_grade   FROM students;
SELECT MIN(grade)     AS lowest_grade    FROM students;
SELECT SUM(grade)     AS total_points    FROM students;

-- Group by + Having
SELECT city, AVG(grade) AS avg_grade
FROM students
GROUP BY city
HAVING AVG(grade) > 75;
</code></pre>

<h3>JOINs</h3>
<pre><code>
-- INNER JOIN: only matching rows
SELECT s.name, c.title AS course
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c     ON e.course_id = c.id;

-- LEFT JOIN: all students, even those not enrolled
SELECT s.name, c.title
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN courses c     ON e.course_id = c.id;
</code></pre>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=db_ch1, title='Normalization',
            defaults={
                'order': 3,
                'content': '''<h2>Database Normalization</h2>
<p>Normalization is the process of organizing a database to reduce redundancy and improve data integrity.
It follows a series of rules called <strong>Normal Forms (NF)</strong>.</p>

<h3>First Normal Form (1NF)</h3>
<ul>
  <li>Each column must contain <strong>atomic (indivisible)</strong> values</li>
  <li>Each column must contain values of a <strong>single type</strong></li>
  <li>Each row must be <strong>unique</strong></li>
</ul>
<p><strong>❌ Bad (violates 1NF):</strong> Phone column contains "9876543210, 8765432109"</p>
<p><strong>✅ Good (1NF):</strong> Separate rows for each phone number.</p>

<h3>Second Normal Form (2NF)</h3>
<ul>
  <li>Must already be in 1NF</li>
  <li>Every non-key attribute must depend on the <strong>entire primary key</strong> (no partial dependency)</li>
</ul>

<h3>Third Normal Form (3NF)</h3>
<ul>
  <li>Must already be in 2NF</li>
  <li>No <strong>transitive dependencies</strong> (non-key attributes must not depend on other non-key attributes)</li>
</ul>

<h3>Benefits of Normalization</h3>
<ul>
  <li>🗑️ Eliminates data redundancy</li>
  <li>✅ Ensures data consistency</li>
  <li>⚡ Improves update, insert, delete performance</li>
  <li>📦 Reduces storage requirements</li>
</ul>

<blockquote>
Most production databases are normalized to <strong>3NF</strong>. Beyond 3NF, performance trade-offs
often make lower normal forms preferable (denormalization for read-heavy workloads).
</blockquote>'''
            }
        )

        if not db_ch1.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=db_ch1, order=1, marks=1,
                    question_text='What does DBMS stand for?',
                    option_a='Database Management Software', option_b='Data Base Management System',
                    option_c='Data Backup Management System', option_d='Database Multiple Systems',
                    correct_answer='B',
                    explanation='DBMS stands for Database Management System — software for managing databases.'),
                QuizQuestion(chapter=db_ch1, order=2, marks=1,
                    question_text='Which SQL command is used to retrieve data from a table?',
                    option_a='GET', option_b='FETCH', option_c='SELECT', option_d='RETRIEVE',
                    correct_answer='C',
                    explanation='SELECT is the SQL DML command used to query and retrieve data from tables.'),
                QuizQuestion(chapter=db_ch1, order=3, marks=1,
                    question_text='Which constraint ensures that a column value uniquely identifies each row?',
                    option_a='FOREIGN KEY', option_b='UNIQUE', option_c='PRIMARY KEY', option_d='NOT NULL',
                    correct_answer='C',
                    explanation='PRIMARY KEY uniquely identifies each row and cannot contain NULL values.'),
                QuizQuestion(chapter=db_ch1, order=4, marks=1,
                    question_text='Which SQL command deletes all rows from a table but keeps its structure?',
                    option_a='DELETE FROM table', option_b='DROP TABLE', option_c='TRUNCATE TABLE', option_d='REMOVE TABLE',
                    correct_answer='C',
                    explanation='TRUNCATE TABLE removes all rows efficiently while keeping the table structure. DROP TABLE removes the table itself.'),
                QuizQuestion(chapter=db_ch1, order=5, marks=1,
                    question_text='In normalization, what does 3NF prevent?',
                    option_a='Duplicate primary keys', option_b='NULL values',
                    option_c='Transitive dependencies', option_d='Multi-valued attributes',
                    correct_answer='C',
                    explanation='3NF eliminates transitive dependencies — where a non-key attribute depends on another non-key attribute.'),
            ])
            self.stdout.write('    ✅ DBMS Ch1 quiz added')

        # Chapter 2: Advanced SQL
        db_ch2, _ = Chapter.objects.get_or_create(
            subject=dbms_subj,
            title='Advanced SQL & Transactions',
            defaults={'description': 'Subqueries, indexes, views, and ACID transactions', 'order': 2, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=db_ch2, title='Indexes and Views',
            defaults={
                'order': 1,
                'content': '''<h2>Indexes and Views</h2>

<h3>Database Indexes</h3>
<p>An <strong>index</strong> is a data structure that improves the speed of data retrieval operations.
Think of it like a book index — instead of reading every page, you go directly to the right page.</p>

<pre><code>
-- Create an index on the email column
CREATE INDEX idx_email ON students(email);

-- Create a unique index
CREATE UNIQUE INDEX idx_unique_email ON students(email);

-- Drop an index
DROP INDEX idx_email ON students;
</code></pre>

<h3>Views</h3>
<p>A <strong>view</strong> is a virtual table based on a SELECT query. It simplifies complex queries and
can restrict access to sensitive data.</p>

<pre><code>
-- Create a view showing only passing students
CREATE VIEW passing_students AS
SELECT id, name, email, grade
FROM students
WHERE grade >= 60;

-- Use the view like a table
SELECT * FROM passing_students;

-- Drop a view
DROP VIEW passing_students;
</code></pre>

<h3>Subqueries</h3>
<pre><code>
-- Find students with above-average grades
SELECT name, grade
FROM students
WHERE grade > (SELECT AVG(grade) FROM students);

-- Correlated subquery
SELECT name, grade
FROM students s
WHERE grade = (
    SELECT MAX(grade)
    FROM students
    WHERE city = s.city
);
</code></pre>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=db_ch2, title='ACID Transactions',
            defaults={
                'order': 2,
                'content': '''<h2>ACID Transactions</h2>
<p>A <strong>transaction</strong> is a sequence of SQL operations treated as a single unit of work.
Transactions follow the <strong>ACID</strong> properties to ensure data integrity.</p>

<h3>ACID Properties</h3>
<table>
  <tr><th>Property</th><th>Meaning</th></tr>
  <tr><td><strong>Atomicity</strong></td><td>All operations succeed or all fail — no partial updates</td></tr>
  <tr><td><strong>Consistency</strong></td><td>The database moves from one valid state to another</td></tr>
  <tr><td><strong>Isolation</strong></td><td>Concurrent transactions don't interfere with each other</td></tr>
  <tr><td><strong>Durability</strong></td><td>Committed changes are permanently saved even after crashes</td></tr>
</table>

<h3>Transaction Commands</h3>
<pre><code>
-- Start a transaction
BEGIN;

-- Transfer money between accounts
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;

-- If everything is OK, commit
COMMIT;

-- If something goes wrong, rollback
ROLLBACK;
</code></pre>

<blockquote>
ACID transactions are critical in banking, e-commerce, and any system where data correctness is
non-negotiable. A failed transaction must leave the database unchanged.
</blockquote>'''
            }
        )

        if not db_ch2.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=db_ch2, order=1, marks=1,
                    question_text='What does the A in ACID stand for?',
                    option_a='Authorization', option_b='Availability', option_c='Atomicity', option_d='Accuracy',
                    correct_answer='C',
                    explanation='Atomicity means all operations in a transaction succeed or all are rolled back — no partial updates.'),
                QuizQuestion(chapter=db_ch2, order=2, marks=1,
                    question_text='What is a database index primarily used for?',
                    option_a='Data encryption', option_b='Faster data retrieval', option_c='Backup', option_d='User authentication',
                    correct_answer='B',
                    explanation='Indexes speed up SELECT queries by allowing the database engine to find rows without scanning the entire table.'),
                QuizQuestion(chapter=db_ch2, order=3, marks=1,
                    question_text='What SQL command undoes an uncommitted transaction?',
                    option_a='UNDO', option_b='REVERT', option_c='ROLLBACK', option_d='CANCEL',
                    correct_answer='C',
                    explanation='ROLLBACK undoes all changes made since the last BEGIN or SAVEPOINT.'),
            ])
            self.stdout.write('    ✅ DBMS Ch2 quiz added')

        # ═══════════════════════════════════════════════════════════════
        # SUBJECT 3: Data Structures & Algorithms
        # ═══════════════════════════════════════════════════════════════
        algo_subj, _ = Subject.objects.get_or_create(
            title='Data Structures & Algorithms',
            defaults={
                'description': 'Master arrays, linked lists, trees, graphs, sorting, searching and complexity analysis.',
                'category': 'algorithms',
                'icon': 'cpu',
                'color': '#8b5cf6',
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(f'  Subject: {algo_subj.title}')

        # Chapter 1: Introduction to Algorithms
        al_ch1, _ = Chapter.objects.get_or_create(
            subject=algo_subj,
            title='Introduction to Algorithms',
            defaults={'description': 'What are algorithms, Big-O complexity analysis', 'order': 1, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=al_ch1, title='What is an Algorithm?',
            defaults={
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/rL8X2mlNHPM',
                'content': '''<h2>What is an Algorithm?</h2>
<p>An <strong>algorithm</strong> is a step-by-step, finite set of well-defined instructions for solving a
problem or performing a computation.</p>

<h3>Characteristics of a Good Algorithm</h3>
<ul>
  <li><strong>Correctness:</strong> Produces the right output for all valid inputs</li>
  <li><strong>Efficiency:</strong> Uses minimal time and memory</li>
  <li><strong>Definiteness:</strong> Every step is clearly and precisely defined</li>
  <li><strong>Finiteness:</strong> Terminates after a finite number of steps</li>
  <li><strong>Generality:</strong> Works for a range of inputs, not just one case</li>
</ul>

<h3>Big-O Notation — Time Complexity</h3>
<p>Big-O describes how an algorithm's runtime grows as the input size <strong>n</strong> increases.</p>
<table>
  <tr><th>Notation</th><th>Name</th><th>Example</th></tr>
  <tr><td>O(1)</td><td>Constant</td><td>Array index access</td></tr>
  <tr><td>O(log n)</td><td>Logarithmic</td><td>Binary search</td></tr>
  <tr><td>O(n)</td><td>Linear</td><td>Linear search, single loop</td></tr>
  <tr><td>O(n log n)</td><td>Linearithmic</td><td>Merge Sort, Heap Sort</td></tr>
  <tr><td>O(n²)</td><td>Quadratic</td><td>Bubble Sort, nested loops</td></tr>
  <tr><td>O(2ⁿ)</td><td>Exponential</td><td>Naive recursive Fibonacci</td></tr>
  <tr><td>O(n!)</td><td>Factorial</td><td>Brute-force Travelling Salesman</td></tr>
</table>

<h3>Example: Linear vs Binary Search</h3>
<pre><code>
# Linear Search — O(n)
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Binary Search — O(log n) — requires sorted array
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

nums = list(range(1, 101))  # [1 .. 100]
print(linear_search(nums, 73))  # 72
print(binary_search(nums, 73))  # 72
</code></pre>

<blockquote>
For n = 1,000,000 items, linear search may check all 1M elements; binary search needs only ~20 steps!
</blockquote>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=al_ch1, title='Sorting Algorithms',
            defaults={
                'order': 2,
                'content': '''<h2>Sorting Algorithms</h2>
<p>Sorting arranges elements in a specific order (ascending/descending). Choosing the right algorithm
depends on data size, data distribution, and available memory.</p>

<h3>Bubble Sort — O(n²)</h3>
<pre><code>
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
# [11, 12, 22, 25, 34, 64, 90]
</code></pre>

<h3>Merge Sort — O(n log n)</h3>
<pre><code>
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
# [3, 9, 10, 27, 38, 43, 82]
</code></pre>

<h3>Comparison of Sorting Algorithms</h3>
<table>
  <tr><th>Algorithm</th><th>Best</th><th>Average</th><th>Worst</th><th>Space</th></tr>
  <tr><td>Bubble Sort</td><td>O(n)</td><td>O(n²)</td><td>O(n²)</td><td>O(1)</td></tr>
  <tr><td>Selection Sort</td><td>O(n²)</td><td>O(n²)</td><td>O(n²)</td><td>O(1)</td></tr>
  <tr><td>Insertion Sort</td><td>O(n)</td><td>O(n²)</td><td>O(n²)</td><td>O(1)</td></tr>
  <tr><td>Merge Sort</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n)</td></tr>
  <tr><td>Quick Sort</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n²)</td><td>O(log n)</td></tr>
  <tr><td>Heap Sort</td><td>O(n log n)</td><td>O(n log n)</td><td>O(n log n)</td><td>O(1)</td></tr>
</table>'''
            }
        )

        if not al_ch1.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=al_ch1, order=1, marks=1,
                    question_text='What is the time complexity of Binary Search?',
                    option_a='O(1)', option_b='O(n)', option_c='O(log n)', option_d='O(n²)',
                    correct_answer='C',
                    explanation='Binary search halves the search space each step, giving O(log n) time complexity.'),
                QuizQuestion(chapter=al_ch1, order=2, marks=1,
                    question_text='Which sorting algorithm has O(n log n) worst-case complexity?',
                    option_a='Bubble Sort', option_b='Insertion Sort', option_c='Selection Sort', option_d='Merge Sort',
                    correct_answer='D',
                    explanation='Merge Sort always divides and merges in O(n log n) regardless of input order.'),
                QuizQuestion(chapter=al_ch1, order=3, marks=1,
                    question_text='Which notation describes the worst-case performance of an algorithm?',
                    option_a='Omega (Ω)', option_b='Theta (Θ)', option_c='Big-O (O)', option_d='Little-o',
                    correct_answer='C',
                    explanation='Big-O notation describes the upper bound / worst-case time complexity.'),
                QuizQuestion(chapter=al_ch1, order=4, marks=1,
                    question_text='What is the space complexity of Merge Sort?',
                    option_a='O(1)', option_b='O(log n)', option_c='O(n)', option_d='O(n²)',
                    correct_answer='C',
                    explanation='Merge Sort requires O(n) extra space for the temporary arrays used during merging.'),
            ])
            self.stdout.write('    ✅ Algorithms Ch1 quiz added')

        # Chapter 2: Data Structures
        al_ch2, _ = Chapter.objects.get_or_create(
            subject=algo_subj,
            title='Linear Data Structures',
            defaults={'description': 'Arrays, Linked Lists, Stacks and Queues', 'order': 2, 'is_active': True}
        )

        Topic.objects.get_or_create(
            chapter=al_ch2, title='Arrays and Linked Lists',
            defaults={
                'order': 1,
                'content': '''<h2>Arrays and Linked Lists</h2>

<h3>Arrays</h3>
<p>An array stores elements in <strong>contiguous memory locations</strong>, allowing O(1) index access.</p>
<pre><code>
# Python list (dynamic array)
arr = [10, 20, 30, 40, 50]

# Access — O(1)
print(arr[2])       # 30

# Insert at end — O(1) amortized
arr.append(60)

# Insert at index — O(n) due to shifting
arr.insert(2, 99)   # [10, 20, 99, 30, 40, 50, 60]

# Delete — O(n)
arr.remove(99)
</code></pre>

<h3>Linked Lists</h3>
<p>A linked list stores elements in <strong>non-contiguous nodes</strong>, each holding data and a pointer to the next node.</p>
<pre><code>
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements))

ll = LinkedList()
ll.append(1); ll.append(2); ll.append(3)
ll.display()  # 1 -> 2 -> 3
</code></pre>

<h3>Arrays vs Linked Lists</h3>
<table>
  <tr><th>Operation</th><th>Array</th><th>Linked List</th></tr>
  <tr><td>Access by index</td><td>O(1)</td><td>O(n)</td></tr>
  <tr><td>Search</td><td>O(n)</td><td>O(n)</td></tr>
  <tr><td>Insert at beginning</td><td>O(n)</td><td>O(1)</td></tr>
  <tr><td>Insert at end</td><td>O(1)*</td><td>O(n) or O(1)**</td></tr>
  <tr><td>Delete</td><td>O(n)</td><td>O(n)</td></tr>
</table>'''
            }
        )

        Topic.objects.get_or_create(
            chapter=al_ch2, title='Stacks and Queues',
            defaults={
                'order': 2,
                'content': '''<h2>Stacks and Queues</h2>

<h3>Stack — LIFO (Last In, First Out)</h3>
<p>Like a stack of plates — you add and remove from the <strong>top</strong>.</p>
<pre><code>
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):     # O(1)
        self._data.append(item)

    def pop(self):            # O(1)
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):           # O(1)
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
s.push(1); s.push(2); s.push(3)
print(s.pop())   # 3
print(s.peek())  # 2
</code></pre>

<h3>Real-world Stack Applications</h3>
<ul>
  <li>🔙 Browser back/forward history</li>
  <li>↩️ Undo/Redo in text editors</li>
  <li>📞 Function call stack in programs</li>
  <li>🔢 Expression evaluation (brackets matching)</li>
</ul>

<h3>Queue — FIFO (First In, First Out)</h3>
<p>Like a queue at a ticket counter — first person in is first served.</p>
<pre><code>
from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):  # O(1)
        self._data.append(item)

    def dequeue(self):        # O(1)
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()

    def is_empty(self):
        return len(self._data) == 0

q = Queue()
q.enqueue("Alice"); q.enqueue("Bob"); q.enqueue("Carol")
print(q.dequeue())  # Alice
print(q.dequeue())  # Bob
</code></pre>

<h3>Real-world Queue Applications</h3>
<ul>
  <li>🖨️ Print spooler / task scheduling</li>
  <li>🌐 Web server request handling</li>
  <li>📨 Message queues (RabbitMQ, Kafka)</li>
  <li>🔍 BFS graph traversal</li>
</ul>'''
            }
        )

        if not al_ch2.questions.exists():
            QuizQuestion.objects.bulk_create([
                QuizQuestion(chapter=al_ch2, order=1, marks=1,
                    question_text='What principle does a Stack follow?',
                    option_a='FIFO', option_b='FILO', option_c='LIFO', option_d='LILO',
                    correct_answer='C',
                    explanation='Stack follows LIFO — Last In, First Out. The last element pushed is the first to be popped.'),
                QuizQuestion(chapter=al_ch2, order=2, marks=1,
                    question_text='What is the time complexity of accessing an element by index in an array?',
                    option_a='O(n)', option_b='O(log n)', option_c='O(n²)', option_d='O(1)',
                    correct_answer='D',
                    explanation='Arrays store elements in contiguous memory, so any index can be accessed in constant O(1) time.'),
                QuizQuestion(chapter=al_ch2, order=3, marks=1,
                    question_text='Which data structure is best suited for BFS (Breadth-First Search)?',
                    option_a='Stack', option_b='Queue', option_c='Array', option_d='Linked List',
                    correct_answer='B',
                    explanation='BFS uses a Queue (FIFO) to visit nodes level by level.'),
            ])
            self.stdout.write('    ✅ Algorithms Ch2 quiz added')

        # ── Final summary ─────────────────────────────────────────────────────
        self.stdout.write('\n' + '─' * 55)
        self.stdout.write(self.style.SUCCESS('✅  Database seeded successfully!'))
        self.stdout.write('─' * 55)
        self.stdout.write('  Subjects created : 3  (Python, DBMS, Algorithms)')
        self.stdout.write('  Chapters created : 7')
        self.stdout.write('  Topics created   : 14')
        self.stdout.write('  Quiz questions   : 30+')
        self.stdout.write('─' * 55)
        self.stdout.write('  🔑 Admin login   :  admin     /  admin123')
        self.stdout.write('  🎓 Student login :  student1  /  student123')
        self.stdout.write('─' * 55)
        self.stdout.write('  Run the server with:')
        self.stdout.write('    python manage.py runserver')
        self.stdout.write('  Then open:  http://127.0.0.1:8000/')
        self.stdout.write('─' * 55)
