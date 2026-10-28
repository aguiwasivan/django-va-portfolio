from django.urls import path
from . import views
app_name = 'projects'
urlpatterns = [path('',views.listing,name='list'),path('download/<int:pk>/',views.attachment,name='download'),path('<slug:slug>/',views.detail,name='detail')]
