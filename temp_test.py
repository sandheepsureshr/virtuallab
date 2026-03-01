import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','virtuallab.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from lab.models import Subject, Enrollment, Certificate, StudentProfile

client = Client()
user = User.objects.get(username='testuser')
enrollment = Enrollment.objects.filter(student=user).first()
subject = enrollment.subject
cert = enrollment.certificate
print('have cert', cert)
client.login(username='testuser', password='pwd')
response = client.get(f'/subject/{subject.id}/certificate/download/')
print('status', response.status_code, response['Content-Type'], 'len', len(response.content))
