from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Subject, Chapter, Topic, QuizQuestion, StudentProfile, Announcement


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    institution = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                institution=self.cleaned_data.get('institution', '')
            )
        return user


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'description', 'category', 'thumbnail', 'icon', 'color', 'is_active', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'description', 'order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'video_url', 'video_file', 'order', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12, 'class': 'rich-editor'}),
        }


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question_text', 'question_type', 'option_a', 'option_b', 'option_c',
                  'option_d', 'correct_answer', 'explanation', 'marks', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 2}),
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = StudentProfile
        fields = ['bio', 'avatar', 'institution']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'subject', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
