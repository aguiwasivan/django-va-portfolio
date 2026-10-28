from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from projects.models import Project

class PageSitemap(Sitemap):
    changefreq = 'monthly'
    def items(self): return ['home','about','skills','projects:list','contact']
    def location(self,item): return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    def items(self): return Project.objects.all()
