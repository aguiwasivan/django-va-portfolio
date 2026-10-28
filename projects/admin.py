from django.contrib import admin
from .models import Project, ProjectAttachment

class AttachmentInline(admin.TabularInline):
    model = ProjectAttachment
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title','category','is_sample','featured','display_order']
    list_editable = ['featured','display_order']
    list_filter = ['category','is_sample','featured']
    search_fields = ['title','description']
    prepopulated_fields = {'slug':('title',)}
    inlines = [AttachmentInline]
