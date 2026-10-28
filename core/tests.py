from io import StringIO
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .forms import ContactForm
from .models import Profile, ContactMessage, Skill
from .validators import validate_file, validate_image, validate_resume
from projects.models import Project, ProjectAttachment

@override_settings(SECURE_SSL_REDIRECT=False, STORAGES={'default':{'BACKEND':'django.core.files.storage.InMemoryStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_portfolio', stdout=StringIO())

    def payload(self):
        return {'name':'Test Person','email':'person@example.com','subject':'Remote opportunity','message':'I would like to discuss a role.','website':''}

    def test_home_and_public_pages(self):
        for path in ['/','/about/','/skills/','/contact/','/projects/','/robots.txt','/sitemap.xml']:
            with self.subTest(path=path): self.assertEqual(self.client.get(path).status_code,200)
        self.assertContains(self.client.get('/'),'Aspiring Virtual Administrative Assistant')

    def test_invalid_form(self):
        form = ContactForm({'name':'','email':'invalid','subject':'','message':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors), {'name','email','subject','message'})
        data = self.payload(); data['message'] = 'a' * 5001
        self.assertFalse(ContactForm(data).is_valid())

    def test_contact_submission_and_success(self):
        response = self.client.post('/contact/',self.payload(),follow=True)
        self.assertContains(response,'Your message has been received')
        self.assertEqual(ContactMessage.objects.count(),1)
        self.assertFalse(ContactMessage.objects.get().is_read)

    def test_honeypot(self):
        data = self.payload(); data['website'] = 'https://spam.example'
        self.client.post('/contact/',data)
        self.assertFalse(ContactMessage.objects.exists())

    def test_rate_limit(self):
        for _ in range(5): self.assertEqual(self.client.post('/contact/',self.payload()).status_code,302)
        self.assertEqual(self.client.post('/contact/',self.payload()).status_code,429)
        self.assertEqual(ContactMessage.objects.count(),5)

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/contact/',self.payload()).status_code,403)
        client.get('/contact/')
        self.assertEqual(client.post('/contact/',self.payload(),HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value).status_code,302)

    @override_settings(EMAIL_HOST='smtp.example.com',CONTACT_NOTIFICATION_EMAIL='owner@example.com')
    @patch('core.views.EmailMessage.send')
    def test_smtp_notification(self,send):
        self.client.post('/contact/',self.payload())
        send.assert_called_once()

    @override_settings(
        EMAIL_HOST='smtp.example.com',
        CONTACT_NOTIFICATION_EMAIL='owner@example.com',
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    )
    def test_notification_contains_actual_form_message(self):
        from django.core import mail

        data = self.payload()
        data['message'] = 'Hello Ivan,\nWe would like to discuss an assistant role.\nAre you available?'
        self.assertEqual(self.client.post('/contact/', data).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        notification = mail.outbox[0]
        self.assertTrue(notification.body.startswith(data['message'] + '\n\n'))
        self.assertIn(data['name'], notification.body)
        self.assertIn(data['email'], notification.body)
        self.assertEqual(notification.subject, 'Portfolio inquiry: ' + data['subject'])
        self.assertEqual(notification.to, ['owner@example.com'])
        self.assertEqual(notification.reply_to, [data['email']])

    @override_settings(EMAIL_HOST='smtp.example.com',CONTACT_NOTIFICATION_EMAIL='owner@example.com')
    @patch('core.views.EmailMessage.send',side_effect=OSError('SMTP unavailable'))
    def test_smtp_failure_does_not_lose_message(self,send):
        with self.assertLogs('core.views',level='ERROR'):
            self.assertEqual(self.client.post('/contact/',self.payload()).status_code,302)
        self.assertEqual(ContactMessage.objects.count(),1)

    def test_resume_opens_inline(self):
        self.assertEqual(self.client.get('/resume/').status_code,404)
        profile = Profile.objects.first()
        profile.resume.save('resume.pdf',ContentFile(b'%PDF-1.4\nTest sample'))
        response = self.client.get('/resume/')
        self.assertEqual(response.status_code,200)
        self.assertIn('inline;',response['Content-Disposition'])
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(b''.join(response.streaming_content).startswith(b'%PDF'))

    def test_admin_permissions(self):
        self.assertEqual(self.client.get('/admin/core/contactmessage/').status_code,302)
        user = get_user_model().objects.create_user(username='ordinary',password='test-pass-long')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/admin/').status_code,302)
        user.is_staff = True; user.save()
        self.assertEqual(self.client.get('/admin/core/contactmessage/').status_code,403)
        user.is_superuser = True; user.save()
        self.assertEqual(self.client.get('/admin/core/contactmessage/').status_code,200)

    def test_seed_is_idempotent_and_preserves_edits(self):
        profile = Profile.objects.first(); profile.full_name='Edited Name'; profile.save()
        project = Project.objects.first(); project.title='Edited project'; project.save()
        call_command('seed_portfolio', stdout=StringIO())
        self.assertEqual(Profile.objects.count(),1)
        self.assertEqual(Skill.objects.count(),20)
        self.assertEqual(Project.objects.count(),4)
        self.assertEqual(ProjectAttachment.objects.count(),2)
        profile.refresh_from_db(); project.refresh_from_db()
        self.assertEqual(profile.full_name,'Edited Name')
        self.assertEqual(project.title,'Edited project')

    def test_upload_validation(self):
        for name,content in [('bad.exe',b'test'),('bad.pdf',b'not a pdf'),('bad.csv',b'\xff\x00'),('huge.pdf',b'%PDF-'+b'x'*5242880)]:
            with self.subTest(name=name),self.assertRaises(ValidationError):
                validate_file(SimpleUploadedFile(name,content))
        with self.assertRaises(ValidationError): validate_image(SimpleUploadedFile('fake.png',b'not image'))
        with self.assertRaises(ValidationError): validate_resume(SimpleUploadedFile('file.csv',b'a,b\n1,2'))
        with self.assertRaises(ValidationError): validate_image(SimpleUploadedFile('image.html',b'not image'))

    def test_skills_details_render_from_database(self):
        skill = Skill.objects.get(name='Data Entry')
        skill.detailed_description = 'A unique learning approach from the database.'
        skill.practical_tasks = 'First practice task\n\n Second practice task '
        skill.related_tools = 'Example tool\nAnother tool'
        skill.save()
        response = self.client.get('/skills/')
        self.assertContains(response, skill.detailed_description)
        self.assertContains(response, 'Second practice task')
        self.assertContains(response, 'Example tool')
        self.assertContains(response, '<details class="skill-details">', count=20)
        self.assertContains(response, 'View Details', count=20)
        self.assertContains(response, 'Show Less', count=20)
        for item in Skill.objects.all():
            self.assertContains(response, item.name)
            self.assertTrue(item.detailed_description)
            self.assertTrue(item.task_list)
        self.assertEqual(skill.task_list, ['First practice task', 'Second practice task'])

    def test_theme_controls_and_early_script_on_public_pages(self):
        paths = ['/', '/about/', '/skills/', '/projects/', '/contact/']
        paths += [project.get_absolute_url() for project in Project.objects.all()]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, 'data-theme-toggle', count=1)
                self.assertContains(response, 'data-lucide="moon"')
                self.assertContains(response, 'data-lucide="sun"')
                html = response.content.decode()
                self.assertLess(html.index('js/theme.js'), html.index('css/theme.css'))
                self.assertIn('<script src="/static/js/theme.js"></script>', html)

    def test_error_pages_support_theme_without_database_for_500(self):
        from django.template.loader import render_to_string
        with self.assertNumQueries(0):
            html = render_to_string('500.html')
        self.assertIn('js/theme.js', html)
        self.assertIn('data-theme-toggle', html)
        with self.settings(DEBUG=False):
            self.assertContains(self.client.get('/missing-page/'), 'data-theme-toggle', status_code=404)

    def test_seed_upgrades_only_legacy_defaults(self):
        from core.skill_content import seed_skills, LEGACY_DESCRIPTIONS
        untouched = Skill.objects.get(name='Data Entry')
        customized = Skill.objects.get(name='Email Management')
        for item in [untouched, customized]:
            item.seed_baseline = {}
            item.detailed_description = ''
            item.practical_tasks = ''
            item.related_tools = ''
        untouched.description = LEGACY_DESCRIPTIONS['administrative']
        untouched.save()
        customized.description = 'My own custom short description.'
        customized.save()
        seed_skills()
        untouched.refresh_from_db()
        customized.refresh_from_db()
        self.assertNotEqual(untouched.description, LEGACY_DESCRIPTIONS['administrative'])
        self.assertEqual(customized.description, 'My own custom short description.')
        self.assertTrue(customized.detailed_description)

    def test_seed_preserves_custom_details_and_intentionally_cleared_fields(self):
        from core.skill_content import seed_skills
        skill = Skill.objects.get(name='Data Entry')
        skill.detailed_description = 'My own practice process.'
        skill.practical_tasks = ''
        skill.related_tools = 'Custom tool'
        skill.icon = 'star'
        skill.display_order = 99
        skill.save()
        seed_skills()
        seed_skills()
        skill.refresh_from_db()
        self.assertEqual(skill.detailed_description, 'My own practice process.')
        self.assertEqual(skill.practical_tasks, '')
        self.assertEqual(skill.related_tools, 'Custom tool')
        self.assertEqual(skill.icon, 'star')
        self.assertEqual(skill.display_order, 99)
        self.assertEqual(Skill.objects.count(), 20)

    def test_seed_refreshes_untouched_previous_version(self):
        from core.skill_content import seed_skills
        skill = Skill.objects.get(name='Data Entry')
        expected = skill.detailed_description
        skill.detailed_description = 'An earlier default.'
        skill.seed_baseline['detailed_description'] = 'An earlier default.'
        skill.save()
        seed_skills()
        skill.refresh_from_db()
        self.assertEqual(skill.detailed_description, expected)

    def test_admin_can_edit_skill_detail_fields(self):
        user = get_user_model().objects.create_superuser('editor', 'editor@example.com', 'test-pass-long')
        self.client.force_login(user)
        skill = Skill.objects.get(name='Data Entry')
        url = reverse('admin:core_skill_change', args=[skill.pk])
        response = self.client.post(url, {
            'name': skill.name, 'category': skill.category, 'icon': skill.icon,
            'display_order': skill.display_order, 'description': skill.description,
            'detailed_description': 'Admin-edited learning details.',
            'practical_tasks': 'Review records\nCheck dates',
            'related_tools': 'Microsoft Excel\nGoogle Sheets', '_save': 'Save',
        })
        self.assertEqual(response.status_code, 302)
        skill.refresh_from_db()
        self.assertEqual(skill.detailed_description, 'Admin-edited learning details.')
        self.assertContains(self.client.get('/skills/'), skill.detailed_description)

    @override_settings(SECURE_SSL_REDIRECT=True, SECURE_HSTS_SECONDS=31536000)
    def test_production_security_headers(self):
        self.assertEqual(self.client.get('/').status_code,301)
        response = self.client.get('/',secure=True)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response['X-Content-Type-Options'],'nosniff')
        self.assertEqual(response['X-Frame-Options'],'DENY')
        self.assertIn('max-age=31536000',response['Strict-Transport-Security'])

    @override_settings(DEBUG=False)
    def test_custom_404(self):
        self.assertContains(self.client.get('/not-a-page/'),'This page isn',status_code=404)
