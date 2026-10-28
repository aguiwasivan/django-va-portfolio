from django.db import models
from .validators import validate_image, validate_resume

class Profile(models.Model):
    full_name = models.CharField(max_length=120, default='Your Name')
    professional_title = models.CharField(max_length=180, default='Aspiring Virtual Administrative Assistant')
    biography = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', blank=True, validators=[validate_image])
    email = models.EmailField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, validators=[validate_resume])
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    availability_status = models.CharField(max_length=160, default='Open to remote opportunities')
    def __str__(self): return self.full_name

class Skill(models.Model):
    CATEGORY_CHOICES = [('administrative','Administrative skills'),('tools','Digital tools')]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, db_index=True)
    icon = models.CharField(max_length=40, default='check-check')
    description = models.CharField(max_length=250, blank=True)
    detailed_description = models.TextField(blank=True)
    practical_tasks = models.TextField(blank=True, help_text='One practical task or use case per line.')
    related_tools = models.TextField(blank=True, help_text='One commonly used tool per line. These are examples, not claims of proficiency.')
    seed_baseline = models.JSONField(default=dict, blank=True, editable=False)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['display_order','name']
    def __str__(self): return self.name

    @property
    def task_list(self):
        return [line.strip() for line in self.practical_tasks.splitlines() if line.strip()]

    @property
    def tool_list(self):
        return [line.strip() for line in self.related_tools.splitlines() if line.strip()]

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return self.subject

class ContactRateLimit(models.Model):
    key = models.CharField(max_length=64, unique=True)
    window_start = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
