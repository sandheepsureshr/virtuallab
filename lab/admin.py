from django.contrib import admin
from .models import (Subject, Chapter, Topic, QuizQuestion, Enrollment,
                     ChapterProgress, QuizResult, StudentProfile, Announcement,
                     Certificate)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active', 'total_chapters', 'enrolled_count']
    list_filter = ['category', 'is_active']
    search_fields = ['title']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'order', 'is_active']
    list_filter = ['subject', 'is_active']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'chapter', 'order', 'is_active']
    list_filter = ['chapter__subject']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'chapter', 'correct_answer', 'marks']
    list_filter = ['chapter__subject']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'enrolled_at', 'is_active']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'chapter', 'score', 'total_marks', 'attempted_at']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'is_blocked', 'joined_at']
    list_filter = ['is_blocked']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'completed_at', 'average_score']
    list_filter = ['completed_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_active']
