# 🧪 VirtualLab — Virtual Learning Platform

A complete, fully-functional **Django-based e-learning platform** for students to study
practical and theoretical subjects like Python Programming, DBMS, and Algorithms online.

---

## 📁 Project Structure

```
virtuallab/
│
├── manage.py                          # Django management entry point
├── requirements.txt                   # Python dependencies
├── setup.sh                           # Linux/macOS one-click setup
├── setup.bat                          # Windows one-click setup
├── db.sqlite3                         # SQLite database (auto-created)
│
├── virtuallab/                        # Django project settings package
│   ├── __init__.py
│   ├── settings.py                    # All project settings
│   ├── urls.py                        # Root URL configuration
│   └── wsgi.py                        # WSGI deployment entry point
│
└── lab/                               # Main application
    ├── __init__.py
    ├── apps.py                        # App configuration
    ├── models.py                      # ⭐ All database models
    ├── views.py                       # ⭐ All view logic (student + admin)
    ├── urls.py                        # ⭐ All URL routes
    ├── forms.py                       # Django forms
    ├── decorators.py                  # @admin_required, @student_required
    ├── admin.py                       # Django admin registrations
    │
    ├── management/
    │   └── commands/
    │       └── seed_data.py           # ⭐ Demo data seeder command
    │
    ├── templates/
    │   └── lab/
    │       ├── base.html              # ⭐ Master layout with full CSS design system
    │       ├── home.html              # Landing/home page
    │       │
    │       ├── auth/
    │       │   ├── login.html         # Login page
    │       │   └── register.html      # Registration page
    │       │
    │       ├── student/
    │       │   ├── dashboard.html     # Student dashboard
    │       │   ├── subject_list.html  # Browse all courses
    │       │   ├── subject_detail.html # Course overview + chapter list
    │       │   ├── chapter_detail.html # Topics viewer (notes + video)
    │       │   ├── quiz.html          # Interactive quiz
    │       │   ├── quiz_result.html   # Detailed quiz result + review
    │       │   └── profile.html       # Student profile editor
    │       │
    │       └── admin/
    │           ├── dashboard.html     # Admin overview + analytics
    │           ├── students.html      # Student management table
    │           ├── student_progress.html  # Individual student progress
    │           ├── subjects.html      # Subjects list
    │           ├── subject_form.html  # Add/edit subject
    │           ├── chapters.html      # Chapters list
    │           ├── chapter_form.html  # Add/edit chapter
    │           ├── topics.html        # Topics list
    │           ├── topic_form.html    # Add/edit topic (with HTML editor)
    │           ├── quiz.html          # Quiz questions list
    │           ├── question_form.html # Add/edit quiz question
    │           ├── analytics.html     # Platform-wide analytics
    │           └── announcements.html # Post announcements
    │
    ├── static/
    │   └── lab/                       # CSS, JS, images
    │
    └── migrations/
        └── __init__.py
```

---

## 🗄️ Database Models (models.py)

| Model | Description |
|-------|-------------|
| `Subject` | A course (e.g., Python Programming) with icon, color, category |
| `Chapter` | A chapter within a subject; unlocks sequentially |
| `Topic` | A lesson with HTML notes + video URL/file |
| `QuizQuestion` | MCQ question with 4 options, correct answer, and explanation |
| `Enrollment` | Links a student to a subject |
| `ChapterProgress` | Tracks which topics a student viewed; marks chapter complete |
| `QuizResult` | Stores a student's quiz attempt with score and per-question answers |
| `StudentProfile` | Extends Django's User with bio, institution, blocked status |
| `Announcement` | Admin notices shown on student dashboard |

---

## 🔗 URL Routes (urls.py)

### Public
| URL | View | Description |
|-----|------|-------------|
| `/` | `home` | Landing page |
| `/register/` | `register_view` | Student registration |
| `/login/` | `login_view` | Login |
| `/logout/` | `logout_view` | Logout |

### Student (requires login)
| URL | Description |
|-----|-------------|
| `/dashboard/` | Student home with stats and enrolled courses |
| `/profile/` | Edit profile |
| `/subjects/` | Browse all courses |
| `/subject/<id>/` | Course detail + chapter list |
| `/subject/<id>/enroll/` | Enroll in a course |
| `/chapter/<id>/` | Chapter topics viewer |
| `/topic/<id>/viewed/` | AJAX — mark topic as viewed |
| `/chapter/<id>/quiz/` | Take quiz |
| `/chapter/<id>/quiz/submit/` | Submit quiz |
| `/quiz/result/<id>/` | View quiz results + answer review |

### Admin (requires `is_staff=True`)
| URL | Description |
|-----|-------------|
| `/admin-panel/` | Admin dashboard |
| `/admin-panel/students/` | Manage students |
| `/admin-panel/student/<id>/progress/` | View individual student progress |
| `/admin-panel/student/<id>/toggle-block/` | Block/unblock student |
| `/admin-panel/student/<id>/delete/` | Delete student |
| `/admin-panel/subjects/` | List subjects |
| `/admin-panel/subject/add/` | Add subject |
| `/admin-panel/subject/<id>/edit/` | Edit subject |
| `/admin-panel/subject/<id>/chapters/` | Manage chapters |
| `/admin-panel/chapter/<id>/topics/` | Manage topics |
| `/admin-panel/topic/add/` (via chapter) | Add topic with HTML editor |
| `/admin-panel/chapter/<id>/quiz/` | Manage quiz questions |
| `/admin-panel/analytics/` | Platform analytics |
| `/admin-panel/announcements/` | Post announcements |

---

## ⚙️ Key Python Files

### `models.py` — All database models
Defines 9 models with relationships, helper methods like `progress_percent()`,
`average_score()`, `get_options()`, etc.

### `views.py` — All view logic
60+ view functions split into:
- **Public views**: home, register, login, logout
- **Student views**: dashboard, subject_list, subject_detail, chapter_detail,
  mark_topic_viewed, take_quiz, submit_quiz, quiz_result_detail, profile
- **Admin views**: dashboard, students, analytics, CRUD for subjects/chapters/topics/questions

### `forms.py` — Django forms
- `StudentRegistrationForm` — extends UserCreationForm with extra fields
- `SubjectForm`, `ChapterForm`, `TopicForm` — content management
- `QuizQuestionForm` — 4-option MCQ with explanation
- `ProfileForm`, `AnnouncementForm`

### `decorators.py` — Access control
- `@admin_required` — redirects non-staff users
- `@student_required` — redirects unauthenticated or blocked users

### `seed_data.py` — Demo data
Creates admin + student accounts, 3 subjects, 7 chapters, 14 topics,
and 30+ quiz questions with explanations.

---

## 🚀 Quick Start

### Linux / macOS
```bash
git clone <repo> virtuallab
cd virtuallab
chmod +x setup.sh
./setup.sh
python manage.py runserver
```

### Windows
```bat
cd virtuallab
setup.bat
python manage.py runserver
```

### Manual setup
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

---

## 🔑 Login Credentials (after seeding)

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Student | `student1` | `student123` |

---

## ✨ Features Summary

### Student Module
- ✅ Secure registration and login
- ✅ Dashboard with enrolled courses and stats
- ✅ Sequential chapter unlocking (pass quiz → unlock next)
- ✅ HTML study notes + embedded YouTube/video player per topic
- ✅ Mark topics as viewed (AJAX)
- ✅ Timed interactive quizzes with progress bar
- ✅ Automatic quiz scoring with detailed answer review + explanations
- ✅ Retake quizzes any time
- ✅ Profile page with learning statistics

### Admin Module
- ✅ Full CRUD for subjects, chapters, topics, quiz questions
- ✅ HTML editor for study notes with toolbar
- ✅ YouTube embed URL + video file upload support
- ✅ Student management (view, block/unblock, delete)
- ✅ Per-student progress and quiz history reports
- ✅ Platform analytics (subject enrollment, avg scores, top students)
- ✅ Announcement system (platform-wide or per-subject)
- ✅ Django built-in admin at `/django-admin/`

---

## 🔮 Future Enhancements
- Certificate generation (PDF) on course completion
- Discussion forums per chapter
- Live coding editor for Python topics
- Email notifications for announcements
- OAuth login (Google, GitHub)
- Mobile app (React Native / Flutter)
- AI-powered quiz generation from notes
- Multi-language support
