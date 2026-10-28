from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from pathlib import Path
from core.validators import validate_file, validate_image

class Project(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=80, db_index=True)
    description = models.TextField()
    detailed_content = models.TextField()
    thumbnail = models.ImageField(upload_to='projects/', blank=True, validators=[validate_image])
    tools_used = models.TextField(help_text='One tool per line.')
    demonstrated_skills = models.TextField(help_text='One skill per line.')
    is_sample = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    display_order = models.PositiveIntegerField(default=0)
    preview_type = models.CharField(max_length=20, choices=[('generic','Text'),('spreadsheet','Spreadsheet'),('calendar','Calendar'),('email','Email'),('agenda','Agenda')], default='generic')
    preview_data = models.JSONField(default=dict, blank=True, help_text='Structured demonstration data. Keep default keys when editing seeded examples.')
    class Meta: ordering = ['display_order','title']
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('projects:detail', kwargs={'slug':self.slug})
    @property
    def tools(self): return self.tools_used.splitlines()
    @property
    def skills(self): return self.demonstrated_skills.splitlines()

class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/', validators=[validate_file])
    label = models.CharField(max_length=150)
    file_type = models.CharField(max_length=10, choices=[('csv','CSV'),('pdf','PDF')])
    class Meta: constraints = [models.UniqueConstraint(fields=['project','label'], name='unique_project_attachment')]
    def __str__(self): return self.label
    def clean(self):
        super().clean()
        if self.file and Path(self.file.name).suffix.lower() != '.' + self.file_type:
            raise ValidationError({'file_type':'Choose the type matching the uploaded document.'})
