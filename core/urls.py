from django.urls import path
from . import views
urlpatterns = [path('',views.home,name='home'),path('about/',views.about,name='about'),path('skills/',views.skills,name='skills'),path('contact/',views.contact,name='contact'),path('resume/',views.resume,name='resume'),path('robots.txt',views.robots,name='robots')]
