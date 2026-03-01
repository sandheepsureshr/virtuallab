from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import (Subject, Chapter, Topic, QuizQuestion, Enrollment,
                     ChapterProgress, QuizResult, StudentProfile, Announcement,
                     Certificate)
from .forms import (StudentRegistrationForm, SubjectForm, ChapterForm,
                    TopicForm, QuizQuestionForm, ProfileForm, AnnouncementForm)
from .decorators import admin_required, student_required


# helper to create a certificate whenever an enrollment completes all chapters

def ensure_certificate(enrollment):
    """Generate or update a Certificate record for the given enrollment.

    Certificates are created only when:
    1. Enrollment has 100% progress (all chapters done)
    2. Average quiz score is >= 60%
    """
    if not enrollment:
        return
    # check both conditions
    if enrollment.progress_percent() == 100 and enrollment.average_score() >= 60:
        avg = enrollment.average_score()
        cert, created = Certificate.objects.get_or_create(
            enrollment=enrollment,
            defaults={'average_score': avg},
        )
        if not created and cert.average_score != avg:
            cert.average_score = avg
            cert.save()


# ─── Public Views ───────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    subjects = Subject.objects.filter(is_active=True)[:6]
    return render(request, 'lab/home.html', {'subjects': subjects})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to VirtualLab, {user.first_name}!')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'lab/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try with email
        if not user:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user:
            if hasattr(user, 'profile') and user.profile.is_blocked:
                messages.error(request, 'Your account has been blocked.')
                return render(request, 'lab/auth/login.html')
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username/email or password.')
    return render(request, 'lab/auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ─── Student Views ───────────────────────────────────────────────────────────────

@student_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(
        student=request.user, is_active=True
    ).select_related('subject').prefetch_related('chapter_progresses')

    recent_results = QuizResult.objects.filter(
        enrollment__student=request.user
    ).select_related('chapter__subject').order_by('-attempted_at')[:5]

    announcements = Announcement.objects.filter(is_active=True)[:3]

    stats = {
        'total_subjects': enrollments.count(),
        'completed_chapters': sum(e.completed_chapters() for e in enrollments),
        'total_quizzes': QuizResult.objects.filter(enrollment__student=request.user).count(),
        'avg_score': request.user.profile.overall_average() if hasattr(request.user, 'profile') else 0,
        'certificates': Certificate.objects.filter(enrollment__student=request.user).count(),
    }

    context = {
        'enrollments': enrollments,
        'recent_results': recent_results,
        'announcements': announcements,
        'stats': stats,
    }
    return render(request, 'lab/student/dashboard.html', context)


@student_required
def student_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    # compile list of completed enrollments for certificates
    completed_enrollments = []
    for e in Enrollment.objects.filter(student=request.user, is_active=True):
        if e.progress_percent() == 100:
            completed_enrollments.append(e)

    completed_enrollments.sort(
        key=lambda e: e.certificate.completed_at if hasattr(e, 'certificate') else timezone.now(),
        reverse=True,
    )
    last_completed = completed_enrollments[0] if completed_enrollments else None

    return render(request, 'lab/student/profile.html', {
        'form': form,
        'profile': profile,
        'completed_enrollments': completed_enrollments,
        'last_completed': last_completed,
    })


@student_required
def subject_list(request):
    subjects = Subject.objects.filter(is_active=True)
    
    # Filter by category if provided
    category = request.GET.get('cat', '')
    if category:
        subjects = subjects.filter(category=category)
    
    enrolled_ids = Enrollment.objects.filter(
        student=request.user, is_active=True
    ).values_list('subject_id', flat=True)
    return render(request, 'lab/student/subject_list.html', {
        'subjects': subjects, 'enrolled_ids': list(enrolled_ids), 'selected_category': category
    })


@student_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, is_active=True)
    enrollment = Enrollment.objects.filter(student=request.user, subject=subject).first()

    chapters = subject.chapters.filter(is_active=True)
    chapter_data = []

    for i, chapter in enumerate(chapters):
        progress = None
        quiz_result = None
        is_unlocked = (i == 0)  # First chapter always unlocked

        if enrollment:
            progress = ChapterProgress.objects.filter(enrollment=enrollment, chapter=chapter).first()
            quiz_result = QuizResult.objects.filter(enrollment=enrollment, chapter=chapter).first()

            # Unlock if previous chapter quiz was passed
            if i > 0:
                prev_chapter = chapters[i - 1]
                prev_result = QuizResult.objects.filter(
                    enrollment=enrollment, chapter=prev_chapter
                ).first()
                is_unlocked = prev_result is not None and prev_result.passed()

        chapter_data.append({
            'chapter': chapter,
            'progress': progress,
            'quiz_result': quiz_result,
            'is_unlocked': is_unlocked,
            'index': i + 1,
        })

    certificate = None
    if enrollment and hasattr(enrollment, 'certificate'):
        certificate = enrollment.certificate

    return render(request, 'lab/student/subject_detail.html', {
        'subject': subject,
        'enrollment': enrollment,
        'chapter_data': chapter_data,
        'certificate': certificate,
    })


@student_required
@require_POST
def enroll_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, is_active=True)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user, subject=subject,
        defaults={'is_active': True}
    )
    if not created:
        enrollment.is_active = True
        enrollment.save()
    messages.success(request, f'Successfully enrolled in {subject.title}!')
    return redirect('subject_detail', subject_id=subject_id)


@student_required
def chapter_detail(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, is_active=True)
    enrollment = Enrollment.objects.filter(student=request.user, subject=chapter.subject, is_active=True).first()
    if not enrollment:
        messages.error(request, 'You must enroll in this subject first.')
        return redirect('subject_detail', subject_id=chapter.subject.id)

    # Check unlock status
    chapters = list(chapter.subject.chapters.filter(is_active=True))
    chapter_index = next((i for i, c in enumerate(chapters) if c.id == chapter.id), 0)
    is_unlocked = chapter_index == 0

    if chapter_index > 0:
        prev_chapter = chapters[chapter_index - 1]
        prev_result = QuizResult.objects.filter(enrollment=enrollment, chapter=prev_chapter).first()
        is_unlocked = prev_result is not None and prev_result.passed()

    if not is_unlocked:
        messages.warning(request, 'Complete the previous chapter quiz to unlock this chapter.')
        return redirect('subject_detail', subject_id=chapter.subject.id)

    progress, _ = ChapterProgress.objects.get_or_create(enrollment=enrollment, chapter=chapter)
    topics = chapter.topics.filter(is_active=True).order_by('order')
    
    # Determine unlocked topics - sequential unlocking
    topic_data = []
    viewed_topic_ids = set(progress.topics_viewed.values_list('id', flat=True))
    
    for i, topic in enumerate(topics):
        is_topic_unlocked = (i == 0)  # First topic always unlocked
        if i > 0:
            # Unlock only if previous topic is viewed
            prev_topic = topics[i - 1]
            is_topic_unlocked = prev_topic.id in viewed_topic_ids
        
        topic_data.append({
            'topic': topic,
            'is_unlocked': is_topic_unlocked,
            'is_viewed': topic.id in viewed_topic_ids,
            'index': i,
        })
    
    # Handle topic selection from URL parameter
    selected_topic_index = request.GET.get('topic')
    current_topic = None
    
    if selected_topic_index is not None:
        try:
            selected_topic_index = int(selected_topic_index)
            # Find the selected topic
            for item in topic_data:
                if item['index'] == selected_topic_index and item['is_unlocked']:
                    current_topic = item
                    break
        except (ValueError, TypeError):
            pass
    
    if current_topic is None:
        # Find the current topic to show (first unlocked topic that hasn't been viewed)
        all_topics_viewed = len(viewed_topic_ids) == len(topics)
        
        if not all_topics_viewed:
            for item in topic_data:
                if item['is_unlocked'] and not item['is_viewed']:
                    current_topic = item
                    break
        # If all topics are viewed, current_topic remains None (will show completion message)
    
    quiz_result = QuizResult.objects.filter(enrollment=enrollment, chapter=chapter).first()

    return render(request, 'lab/student/chapter_detail.html', {
        'chapter': chapter,
        'topic_data': topic_data,
        'current_topic': current_topic if 'current_topic' in locals() else None,
        'progress': progress,
        'quiz_result': quiz_result,
        'enrollment': enrollment,
        'subject': chapter.subject,
    })


@student_required
@require_POST
def mark_topic_viewed(request, topic_id):
    print(f"DEBUG: mark_topic_viewed called with topic_id={topic_id}")
    print(f"DEBUG: User={request.user}, method={request.method}")
    print(f"DEBUG: POST data={dict(request.POST)}")
    
    topic = get_object_or_404(Topic, id=topic_id)
    print(f"DEBUG: Found topic: {topic.title}")
    
    enrollment = Enrollment.objects.filter(student=request.user, subject=topic.chapter.subject, is_active=True).first()
    if not enrollment:
        print("DEBUG: No enrollment found")
        messages.error(request, 'You must enroll in this subject first.')
        return redirect('subject_detail', subject_id=topic.chapter.subject.id)
    
    print(f"DEBUG: Found enrollment: {enrollment}")
    progress, _ = ChapterProgress.objects.get_or_create(enrollment=enrollment, chapter=topic.chapter)
    progress.topics_viewed.add(topic)
    print(f"DEBUG: Added topic to viewed topics")

    # Auto-complete chapter if all topics viewed and quiz passed
    total_topics = topic.chapter.topics.filter(is_active=True).count()
    viewed = progress.topics_viewed.count()
    quiz_result = QuizResult.objects.filter(enrollment=enrollment, chapter=topic.chapter).first()

    # determine whether quiz requirement is satisfied (chapters w/o quiz are
    # auto-passed)
    chapter = topic.chapter
    has_quiz = chapter.has_quiz()
    passed_quiz = (quiz_result and quiz_result.passed()) or (not has_quiz)

    if viewed >= total_topics and passed_quiz and not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        # once a chapter gets marked complete we may have finished the course
        ensure_certificate(enrollment)

    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'viewed': viewed, 'total': total_topics})
    
    # For form submission, redirect back to chapter with the next topic
    next_topic_index = request.POST.get('next_topic_index')
    print(f"DEBUG: next_topic_index = {next_topic_index}")
    
    if next_topic_index:
        try:
            next_index = int(next_topic_index) + 1
            redirect_url = f"{reverse('chapter_detail', args=[topic.chapter.id])}?topic={next_index}"
            print(f"DEBUG: Redirecting to: {redirect_url}")
            return redirect(redirect_url)
        except (ValueError, TypeError) as e:
            print(f"DEBUG: Error parsing next_topic_index: {e}")
            pass
    
    # Default redirect to chapter detail
    print(f"DEBUG: Default redirect to chapter {topic.chapter.id}")
    return redirect('chapter_detail', chapter_id=topic.chapter.id)


@student_required
def take_quiz(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    enrollment = Enrollment.objects.filter(student=request.user, subject=chapter.subject, is_active=True).first()
    if not enrollment:
        messages.error(request, 'You must enroll in this subject first.')
        return redirect('subject_detail', subject_id=chapter.subject.id)
    questions = chapter.questions.all()

    if not questions.exists():
        messages.warning(request, 'No quiz available for this chapter yet.')
        return redirect('chapter_detail', chapter_id=chapter_id)

    existing_result = QuizResult.objects.filter(enrollment=enrollment, chapter=chapter).first()

    return render(request, 'lab/student/quiz.html', {
        'chapter': chapter,
        'questions': questions,
        'existing_result': existing_result,
    })


@student_required
@require_POST
def submit_quiz(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    enrollment = Enrollment.objects.filter(student=request.user, subject=chapter.subject, is_active=True).first()
    if not enrollment:
        messages.error(request, 'You must enroll in this subject first.')
        return redirect('subject_detail', subject_id=chapter.subject.id)
    questions = chapter.questions.all()

    # Validate that all questions are answered
    unanswered_questions = []
    for question in questions:
        answer = request.POST.get(f'q_{question.id}', '').strip()
        if not answer:
            unanswered_questions.append(f"Question {questions.filter(id__lte=question.id).count()}")

    if unanswered_questions:
        messages.error(request, f'Please answer all questions before submitting. Unanswered: {", ".join(unanswered_questions)}')
        return redirect('take_quiz', chapter_id=chapter_id)

    score = 0
    total_marks = 0
    answers = {}

    for question in questions:
        total_marks += question.marks
        chosen = request.POST.get(f'q_{question.id}', '')
        answers[str(question.id)] = chosen
        if chosen.upper() == question.correct_answer.upper():
            score += question.marks

    time_taken = int(request.POST.get('time_taken', 0))

    # Allow retaking quiz - create new result
    result = QuizResult.objects.create(
        enrollment=enrollment,
        chapter=chapter,
        score=score,
        total_marks=total_marks,
        answers=answers,
        time_taken_seconds=time_taken,
    )

    # Auto-complete chapter if quiz passed
    if result.passed():
        progress, _ = ChapterProgress.objects.get_or_create(enrollment=enrollment, chapter=chapter)
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, f'Congratulations! You passed with {result.percentage()}%!')
        # check for course completion
        ensure_certificate(enrollment)
    else:
        messages.warning(request, f'You scored {result.percentage()}%. Need 60% to pass. Try again!')

    return redirect('quiz_result_detail', result_id=result.id)


@student_required
def quiz_result_detail(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, enrollment__student=request.user)
    questions = result.chapter.questions.all()

    question_results = []
    for q in questions:
        chosen = result.answers.get(str(q.id), '')
        question_results.append({
            'question': q,
            'chosen': chosen,
            'is_correct': chosen.upper() == q.correct_answer.upper(),
        })

    return render(request, 'lab/student/quiz_result.html', {
        'result': result,
        'question_results': question_results,
    })


@student_required
def certificate_view(request, subject_id):
    """Display certificate details for a completed subject."""
    subject = get_object_or_404(Subject, id=subject_id, is_active=True)
    enrollment = get_object_or_404(Enrollment, student=request.user, subject=subject, is_active=True)
    cert = getattr(enrollment, 'certificate', None)
    if not cert:
        messages.error(request, 'Certificate not available yet.')
        return redirect('subject_detail', subject_id=subject_id)
    
    stats = cert.get_completion_stats()
    
    return render(request, 'lab/student/certificate.html', {
        'enrollment': enrollment,
        'certificate': cert,
        'stats': stats,
    })


@student_required
def certificate_pdf(request, subject_id):
    """Render the certificate page as a PDF using WeasyPrint.

    This will produce a faithful copy of the HTML template including all
    CSS decorations.  If WeasyPrint isn't installed, fall back to the
    simple ReportLab generator in the model.
    """
    from django.http import HttpResponse
    from django.template.loader import render_to_string

    subject = get_object_or_404(Subject, id=subject_id, is_active=True)
    enrollment = get_object_or_404(Enrollment, student=request.user, subject=subject, is_active=True)
    cert = getattr(enrollment, 'certificate', None)
    if not cert:
        raise Http404

    filename = f"{subject.title.replace(' ', '_')}-certificate.pdf"
    stats = cert.get_completion_stats()

    try:
        # try HTML->PDF conversion for full styling
        from weasyprint import HTML
        html_string = render_to_string('lab/student/certificate.html', {
            'enrollment': enrollment,
            'certificate': cert,
            'stats': stats,
            'request': request,  # ensure site_name etc available
        })
        pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    except ImportError:
        # backup to the old reportlab method
        pdf_bytes = cert.generate_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# ─── Admin Views ─────────────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    stats = {
        'total_students': User.objects.filter(is_staff=False).count(),
        'total_subjects': Subject.objects.count(),
        'total_chapters': Chapter.objects.count(),
        'total_enrollments': Enrollment.objects.filter(is_active=True).count(),
        'total_quizzes': QuizResult.objects.count(),
        'avg_score': QuizResult.objects.aggregate(avg=Avg('score'))['avg'] or 0,
    }
    recent_enrollments = Enrollment.objects.select_related('student', 'subject').order_by('-enrolled_at')[:8]
    recent_results = QuizResult.objects.select_related(
        'enrollment__student', 'chapter__subject'
    ).order_by('-attempted_at')[:8]
    subjects = Subject.objects.annotate(enroll_count=Count('enrollments')).order_by('-enroll_count')[:5]

    return render(request, 'lab/admin/dashboard.html', {
        'stats': stats,
        'recent_enrollments': recent_enrollments,
        'recent_results': recent_results,
        'subjects': subjects,
    })


@admin_required
def admin_students(request):
    query = request.GET.get('q', '')
    students = User.objects.filter(is_staff=False).select_related('profile')
    if query:
        students = students.filter(
            Q(username__icontains=query) | Q(email__icontains=query) |
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    return render(request, 'lab/admin/students.html', {'students': students, 'query': query})


@admin_required
def toggle_block_student(request, student_id):
    student = get_object_or_404(User, id=student_id, is_staff=False)
    profile, _ = StudentProfile.objects.get_or_create(user=student)
    profile.is_blocked = not profile.is_blocked
    profile.save()
    status = 'blocked' if profile.is_blocked else 'unblocked'
    messages.success(request, f'Student {student.username} has been {status}.')
    return redirect('admin_students')


@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(User, id=student_id, is_staff=False)
    username = student.username
    student.delete()
    messages.success(request, f'Student {username} deleted successfully.')
    return redirect('admin_students')


@admin_required
def admin_student_progress(request, student_id):
    student = get_object_or_404(User, id=student_id, is_staff=False)
    enrollments = Enrollment.objects.filter(student=student, is_active=True).select_related('subject')
    results = QuizResult.objects.filter(enrollment__student=student).select_related('chapter__subject')
    return render(request, 'lab/admin/student_progress.html', {
        'student': student, 'enrollments': enrollments, 'results': results
    })


@admin_required
def admin_subjects(request):
    subjects = Subject.objects.annotate(
        chapter_count=Count('chapters'),
        enroll_count=Count('enrollments')
    )
    return render(request, 'lab/admin/subjects.html', {'subjects': subjects})


@admin_required
def admin_subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('admin_subjects')
    else:
        form = SubjectForm()
    return render(request, 'lab/admin/subject_form.html', {'form': form, 'action': 'Add'})


@admin_required
def admin_subject_edit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('admin_subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'lab/admin/subject_form.html', {'form': form, 'action': 'Edit', 'subject': subject})


@admin_required
def admin_subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject deleted.')
    return redirect('admin_subjects')


@admin_required
def admin_chapters(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    chapters = subject.chapters.annotate(topic_count=Count('topics'), q_count=Count('questions'))
    return render(request, 'lab/admin/chapters.html', {'subject': subject, 'chapters': chapters})


@admin_required
def admin_chapter_add(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.subject = subject
            chapter.save()
            messages.success(request, 'Chapter created!')
            return redirect('admin_chapters', subject_id=subject_id)
    else:
        form = ChapterForm()
    return render(request, 'lab/admin/chapter_form.html', {'form': form, 'subject': subject, 'action': 'Add'})


@admin_required
def admin_chapter_edit(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter updated!')
            return redirect('admin_chapters', subject_id=chapter.subject.id)
    else:
        form = ChapterForm(instance=chapter)
    return render(request, 'lab/admin/chapter_form.html', {
        'form': form, 'subject': chapter.subject, 'chapter': chapter, 'action': 'Edit'
    })


@admin_required
def admin_chapter_delete(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    subject_id = chapter.subject.id
    chapter.delete()
    messages.success(request, 'Chapter deleted.')
    return redirect('admin_chapters', subject_id=subject_id)


@admin_required
def admin_topics(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    topics = chapter.topics.all()
    return render(request, 'lab/admin/topics.html', {'chapter': chapter, 'topics': topics})


@admin_required
def admin_topic_add(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.chapter = chapter
            topic.save()
            messages.success(request, 'Topic created!')
            return redirect('admin_topics', chapter_id=chapter_id)
    else:
        form = TopicForm()
    return render(request, 'lab/admin/topic_form.html', {'form': form, 'chapter': chapter, 'action': 'Add'})


@admin_required
def admin_topic_edit(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated!')
            return redirect('admin_topics', chapter_id=topic.chapter.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'lab/admin/topic_form.html', {
        'form': form, 'chapter': topic.chapter, 'topic': topic, 'action': 'Edit'
    })


@admin_required
def admin_topic_delete(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    chapter_id = topic.chapter.id
    topic.delete()
    messages.success(request, 'Topic deleted.')
    return redirect('admin_topics', chapter_id=chapter_id)


@admin_required
def admin_quiz(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    questions = chapter.questions.all()
    return render(request, 'lab/admin/quiz.html', {'chapter': chapter, 'questions': questions})


@admin_required
def admin_question_add(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.chapter = chapter
            q.save()
            messages.success(request, 'Question added!')
            return redirect('admin_quiz', chapter_id=chapter_id)
    else:
        form = QuizQuestionForm()
    return render(request, 'lab/admin/question_form.html', {'form': form, 'chapter': chapter, 'action': 'Add'})


@admin_required
def admin_question_edit(request, question_id):
    question = get_object_or_404(QuizQuestion, id=question_id)
    if request.method == 'POST':
        form = QuizQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated!')
            return redirect('admin_quiz', chapter_id=question.chapter.id)
    else:
        form = QuizQuestionForm(instance=question)
    return render(request, 'lab/admin/question_form.html', {
        'form': form, 'chapter': question.chapter, 'question': question, 'action': 'Edit'
    })


@admin_required
def admin_question_delete(request, question_id):
    question = get_object_or_404(QuizQuestion, id=question_id)
    chapter_id = question.chapter.id
    question.delete()
    messages.success(request, 'Question deleted.')
    return redirect('admin_quiz', chapter_id=chapter_id)


@admin_required
def admin_analytics(request):
    subject_stats = []
    for subject in Subject.objects.filter(is_active=True):
        enrollments = Enrollment.objects.filter(subject=subject)
        results = QuizResult.objects.filter(chapter__subject=subject)
        subject_stats.append({
            'subject': subject,
            'enrollments': enrollments.count(),
            'avg_score': results.aggregate(avg=Avg('score'))['avg'] or 0,
            'completions': ChapterProgress.objects.filter(
                chapter__subject=subject, is_completed=True
            ).count(),
        })

    top_students = User.objects.filter(is_staff=False).annotate(
        quiz_count=Count('enrollments__quiz_results')
    ).order_by('-quiz_count')[:10]

    return render(request, 'lab/admin/analytics.html', {
        'subject_stats': subject_stats,
        'top_students': top_students,
    })


@admin_required
def admin_announcements(request):
    announcements = Announcement.objects.all()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.created_by = request.user
            ann.save()
            messages.success(request, 'Announcement posted!')
            return redirect('admin_announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'lab/admin/announcements.html', {
        'announcements': announcements, 'form': form
    })
