from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from core.views import download_file
from .models import Project, ProjectAttachment

def listing(request):
    category = request.GET.get('category','')
    projects = Project.objects.all()
    if category: projects = projects.filter(category=category)
    categories = Project.objects.order_by('category').values_list('category',flat=True).distinct()
    return render(request,'projects/list.html',{'projects':projects,'categories':categories,'selected_category':category})

def detail(request, slug):
    return render(request,'projects/detail.html',{'project':get_object_or_404(Project.objects.prefetch_related('attachments'),slug=slug)})

@require_GET
def attachment(request, pk):
    return download_file(get_object_or_404(ProjectAttachment, pk=pk).file)
