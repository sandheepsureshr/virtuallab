from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student Dashboard
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('profile/', views.student_profile, name='profile'),

    # Subjects & Learning
    path('subjects/', views.subject_list, name='subject_list'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:subject_id>/enroll/', views.enroll_subject, name='enroll_subject'),
    path('chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    path('topic/<int:topic_id>/viewed/', views.mark_topic_viewed, name='mark_topic_viewed'),

    # Quiz
    path('chapter/<int:chapter_id>/quiz/', views.take_quiz, name='take_quiz'),
    path('chapter/<int:chapter_id>/quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/result/<int:result_id>/', views.quiz_result_detail, name='quiz_result_detail'),

    # Admin Panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/students/', views.admin_students, name='admin_students'),
    path('admin-panel/student/<int:student_id>/toggle-block/', views.toggle_block_student, name='toggle_block_student'),
    path('admin-panel/student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('admin-panel/student/<int:student_id>/progress/', views.admin_student_progress, name='admin_student_progress'),

    path('admin-panel/subjects/', views.admin_subjects, name='admin_subjects'),
    path('admin-panel/subject/add/', views.admin_subject_add, name='admin_subject_add'),
    path('admin-panel/subject/<int:subject_id>/edit/', views.admin_subject_edit, name='admin_subject_edit'),
    path('admin-panel/subject/<int:subject_id>/delete/', views.admin_subject_delete, name='admin_subject_delete'),

    path('admin-panel/subject/<int:subject_id>/chapters/', views.admin_chapters, name='admin_chapters'),
    path('admin-panel/subject/<int:subject_id>/chapter/add/', views.admin_chapter_add, name='admin_chapter_add'),
    path('admin-panel/chapter/<int:chapter_id>/edit/', views.admin_chapter_edit, name='admin_chapter_edit'),
    path('admin-panel/chapter/<int:chapter_id>/delete/', views.admin_chapter_delete, name='admin_chapter_delete'),

    path('admin-panel/chapter/<int:chapter_id>/topics/', views.admin_topics, name='admin_topics'),
    path('admin-panel/chapter/<int:chapter_id>/topic/add/', views.admin_topic_add, name='admin_topic_add'),
    path('admin-panel/topic/<int:topic_id>/edit/', views.admin_topic_edit, name='admin_topic_edit'),
    path('admin-panel/topic/<int:topic_id>/delete/', views.admin_topic_delete, name='admin_topic_delete'),

    path('admin-panel/chapter/<int:chapter_id>/quiz/', views.admin_quiz, name='admin_quiz'),
    path('admin-panel/chapter/<int:chapter_id>/quiz/add/', views.admin_question_add, name='admin_question_add'),
    path('admin-panel/question/<int:question_id>/edit/', views.admin_question_edit, name='admin_question_edit'),
    path('admin-panel/question/<int:question_id>/delete/', views.admin_question_delete, name='admin_question_delete'),

    path('admin-panel/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-panel/announcements/', views.admin_announcements, name='admin_announcements'),

    # Chatbot API
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]
