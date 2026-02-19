from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('database', 'Database'),
        ('algorithms', 'Algorithms'),
        ('networking', 'Networking'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    icon = models.CharField(max_length=50, default='book', help_text='Icon name (e.g. database, code, cpu)')
    color = models.CharField(max_length=7, default='#4f46e5')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def total_chapters(self):
        return self.chapters.count()

    def enrolled_count(self):
        return self.enrollments.count()


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

    def has_quiz(self):
        return self.questions.exists()


class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='HTML content for study notes')
    video_url = models.URLField(blank=True, null=True, help_text='YouTube embed URL or direct video URL')
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('truefalse', 'True/False'),
    ]
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300, blank=True)
    option_d = models.CharField(max_length=300, blank=True)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    explanation = models.TextField(blank=True, help_text='Explanation shown after quiz')
    marks = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q: {self.question_text[:60]}..."

    def get_options(self):
        opts = [('A', self.option_a), ('B', self.option_b)]
        if self.option_c:
            opts.append(('C', self.option_c))
        if self.option_d:
            opts.append(('D', self.option_d))
        return opts


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.username} → {self.subject.title}"

    def progress_percent(self):
        total = self.subject.chapters.filter(is_active=True).count()
        if total == 0:
            return 0
        completed = ChapterProgress.objects.filter(
            enrollment=self,
            is_completed=True
        ).count()
        return int((completed / total) * 100)

    def completed_chapters(self):
        return ChapterProgress.objects.filter(enrollment=self, is_completed=True).count()

    def average_score(self):
        results = QuizResult.objects.filter(enrollment=self)
        if not results.exists():
            return 0
        total = sum(r.percentage() for r in results)
        return round(total / results.count(), 1)


class ChapterProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='chapter_progresses')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    topics_viewed = models.ManyToManyField(Topic, blank=True)

    class Meta:
        unique_together = ('enrollment', 'chapter')

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.chapter.title}"

    def topics_viewed_count(self):
        return self.topics_viewed.count()

    def topics_total(self):
        return self.chapter.topics.filter(is_active=True).count()


class QuizResult(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='quiz_results')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    answers = models.JSONField(default=dict, help_text='Dict of question_id: chosen_answer')
    attempted_at = models.DateTimeField(auto_now_add=True)
    time_taken_seconds = models.IntegerField(default=0)

    class Meta:
        ordering = ['-attempted_at']

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.chapter.title}: {self.score}/{self.total_marks}"

    def percentage(self):
        if self.total_marks == 0:
            return 0
        return round((self.score / self.total_marks) * 100, 1)

    def passed(self):
        return self.percentage() >= 60


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True)
    is_blocked = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def total_subjects(self):
        return self.user.enrollments.filter(is_active=True).count()

    def total_quizzes(self):
        return QuizResult.objects.filter(enrollment__student=self.user).count()

    def overall_average(self):
        results = QuizResult.objects.filter(enrollment__student=self.user)
        if not results.exists():
            return 0
        return round(sum(r.percentage() for r in results) / results.count(), 1)


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
