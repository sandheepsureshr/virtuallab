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
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text='Upload video file')
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


class Certificate(models.Model):
    """Represents a course completion certificate for a student.

    A certificate is generated when the related enrollment has finished all
    chapters in the subject and the student's average quiz score is >= 60%.
    """
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='certificate',
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    average_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.enrollment.student.username} – {self.enrollment.subject.title}"

    def get_certificate_id(self):
        """Generate unique cert ID: VRL + 8-digit user ID (e.g., VRL000000064)."""
        user_id = self.enrollment.student.id
        return f"VRL{user_id:08d}"

    def get_completion_stats(self):
        """Return dict of completion statistics for this certificate."""
        enrollment = self.enrollment
        chapters = enrollment.subject.chapters.filter(is_active=True).count()
        completed_chapters = ChapterProgress.objects.filter(
            enrollment=enrollment, is_completed=True
        ).count()
        
        # total topics across all chapters
        all_topics = Topic.objects.filter(
            chapter__subject=enrollment.subject,
            is_active=True
        ).count()
        viewed_topics = ChapterProgress.objects.filter(
            enrollment=enrollment
        ).values_list('topics_viewed', flat=True).distinct().count()
        
        quiz_results = QuizResult.objects.filter(enrollment=enrollment)
        total_quizzes = quiz_results.count()
        passed_quizzes = sum(1 for r in quiz_results if r.passed())
        
        return {
            'total_chapters': chapters,
            'completed_chapters': completed_chapters,
            'total_topics': all_topics,
            'viewed_topics': viewed_topics,
            'total_quizzes': total_quizzes,
            'passed_quizzes': passed_quizzes,
            'avg_quiz_score': round(self.enrollment.average_score(), 1),
        }

    def generate_pdf(self):
        """Build a simple PDF version of the certificate and return bytes.

        Uses :mod:`reportlab` so you'll need to add ``reportlab`` to
        ``requirements.txt`` before migrating.
        """
        # import inside method to avoid requiring reportlab unless this is used
        from io import BytesIO
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas

        buffer = BytesIO()
        width, height = letter
        c = canvas.Canvas(buffer, pagesize=letter)

        # draw decorative border
        c.setStrokeColorRGB(0.3, 0.5, 1)
        c.setLineWidth(6)
        margin = 0.5 * inch
        c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

        # title
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(width / 2, height - 2 * inch, "Certificate of Completion")

        # student and course
        c.setFont("Helvetica", 14)
        name = self.enrollment.student.get_full_name() or self.enrollment.student.username
        course = self.enrollment.subject.title
        c.drawCentredString(width / 2, height - 2.8 * inch, f"This is to certify that {name}")
        c.drawCentredString(width / 2, height - 3.4 * inch, f"has successfully completed the course")
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 4.0 * inch, course)

        # details
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 4.8 * inch, f"Completion date: {self.completed_at.strftime('%B %d, %Y')}")
        c.drawCentredString(width / 2, height - 5.4 * inch, f"Overall score: {self.average_score}%")

        # signature lines
        c.line(width*0.2, margin + inch, width*0.4, margin + inch)
        c.drawString(width*0.2, margin + inch - 12, "Instructor")
        c.line(width*0.6, margin + inch, width*0.8, margin + inch)
        c.drawString(width*0.6, margin + inch - 12, "Date")

        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


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
