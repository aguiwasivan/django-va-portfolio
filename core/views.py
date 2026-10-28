import logging
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import F
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.views.decorators.http import require_GET, require_http_methods
from .forms import ContactForm
from .models import Profile, Skill, ContactRateLimit
from projects.models import Project

def home(request):
    return render(request,'core/home.html',{'featured_projects':Project.objects.filter(featured=True)[:4], 'skills':Skill.objects.filter(category='administrative')[:4]})

def about(request): return render(request,'core/about.html')

def skills(request):
    return render(request,'core/skills.html',{'admin_skills':Skill.objects.filter(category='administrative'),'tools':Skill.objects.filter(category='tools')})

def rate_limited(request):
    # Do not trust spoofable forwarding headers. Configure the proxy to supply REMOTE_ADDR.
    key = salted_hmac('contact-rate', request.META.get('REMOTE_ADDR','unknown')).hexdigest()
    now = timezone.now()
    with transaction.atomic():
        ContactRateLimit.objects.filter(window_start__lt=now-timedelta(days=1)).delete()
        bucket, _ = ContactRateLimit.objects.get_or_create(key=key, defaults={'window_start':now})
        ContactRateLimit.objects.filter(pk=bucket.pk, window_start__lt=now-timedelta(hours=1)).update(attempts=0,window_start=now)
        return not ContactRateLimit.objects.filter(pk=bucket.pk, attempts__lt=5).update(attempts=F('attempts')+1)

@require_http_methods(['GET','POST'])
def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if rate_limited(request):
            form.add_error(None, 'Too many attempts. Please try again in an hour.')
            return render(request,'core/contact.html',{'form':form},status=429)
        if form.is_valid():
            submission = form.save()
            if settings.EMAIL_HOST and settings.CONTACT_NOTIFICATION_EMAIL:
                try:
                    EmailMessage(
                        subject='Portfolio inquiry: ' + submission.subject,
                        body=(
                            f'{submission.message}\n\n'
                            '---\n'
                            f'Sent by: {submission.name}\n'
                            f'Email: {submission.email}\n'
                            f'Subject: {submission.subject}'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[settings.CONTACT_NOTIFICATION_EMAIL],
                        reply_to=[submission.email],
                    ).send()
                except Exception:
                    logging.getLogger(__name__).exception('Contact notification failed; message is saved in admin.')
            messages.success(request,'Thank you! Your message has been received.')
            return redirect('contact')
    return render(request,'core/contact.html',{'form':form})

def download_file(field, *, as_attachment=True):
    if not field:
        raise Http404('File not available')
    try:
        response = FileResponse(
            field.open('rb'),
            as_attachment=as_attachment,
            filename=Path(field.name).name,
        )
    except (FileNotFoundError, OSError):
        raise Http404('File not available')
    response['X-Content-Type-Options'] = 'nosniff'
    if as_attachment:
        response['Content-Security-Policy'] = "default-src 'none'; sandbox"
    return response

@require_GET
def resume(request):
    profile = Profile.objects.first()
    if not profile: raise Http404
    response = download_file(profile.resume, as_attachment=False)
    response['Content-Type'] = 'application/pdf'
    return response

def robots(request):
    return HttpResponse(f'User-agent: *\nAllow: /\nDisallow: /{settings.ADMIN_URL}\nSitemap: {settings.SITE_URL}/sitemap.xml\n',content_type='text/plain')
