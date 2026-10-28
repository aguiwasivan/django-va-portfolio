from django.conf import settings
from .models import Profile

def portfolio(request):
    return {'profile':Profile.objects.first(), 'canonical_url':settings.SITE_URL + request.path, 'site_url':settings.SITE_URL}
