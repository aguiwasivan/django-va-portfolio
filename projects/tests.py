import csv
import io
from django.test import TestCase, override_settings
from django.core.management import call_command
from .models import Project, ProjectAttachment

@override_settings(SECURE_SSL_REDIRECT=False, STORAGES={'default':{'BACKEND':'django.core.files.storage.InMemoryStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class ProjectTests(TestCase):
    def setUp(self):
        call_command('seed_portfolio',stdout=io.StringIO())

    def test_listing(self):
        response = self.client.get('/projects/')
        self.assertEqual(len(response.context['projects']),4)
        self.assertContains(response,'Practice Project',count=4)

    def test_details_and_unknown_slug(self):
        for project in Project.objects.all():
            response = self.client.get(project.get_absolute_url())
            self.assertEqual(response.status_code,200)
            self.assertContains(response,'Demonstration only')
        self.assertEqual(self.client.get('/projects/missing/').status_code,404)

    def test_category_filter(self):
        response = self.client.get('/projects/',{'category':'Scheduling'})
        self.assertEqual(list(response.context['projects'].values_list('category',flat=True)),['Scheduling'])
        self.assertContains(self.client.get('/projects/',{'category':'Unknown'}),'No projects in this category')

    def test_real_downloads(self):
        for attachment in ProjectAttachment.objects.all():
            response = self.client.get(f'/projects/download/{attachment.pk}/')
            self.assertEqual(response.status_code,200)
            self.assertIn('attachment;',response['Content-Disposition'])
            content = b''.join(response.streaming_content)
            if attachment.file_type == 'csv':
                records = list(csv.reader(io.StringIO(content.decode('utf-8-sig'))))
                self.assertEqual(len(records),16)
                self.assertEqual(len({row[0] for row in records[1:]}),15)
            else: self.assertTrue(content.startswith(b'%PDF-'))
        self.assertEqual(self.client.get('/projects/download/99999/').status_code,404)

    def test_calendar_and_email_data(self):
        data = Project.objects.get(preview_type='calendar').preview_data
        self.assertEqual(len(data['days']),5)
        for day in data['days']:
            previous = '00:00'
            for event in day['events']:
                start,end = event['time'].split('–')
                self.assertGreaterEqual(start,previous)
                self.assertGreater(end,start)
                previous = end
        self.assertEqual(len(Project.objects.get(preview_type='email').preview_data['emails']),3)
