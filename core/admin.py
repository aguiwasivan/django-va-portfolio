from django.contrib import admin
from .models import Profile, Skill, ContactMessage

admin.site.site_header = 'Portfolio studio'
admin.site.site_title = 'Portfolio admin'
admin.site.index_title = 'Your content, organized.'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','professional_title','availability_status']
    def has_add_permission(self,request):
        return super().has_add_permission(request) and not Profile.objects.exists()

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name','category','display_order']
    list_editable = ['display_order']
    list_filter = ['category']
    search_fields = ['name', 'description', 'detailed_description', 'practical_tasks']
    fieldsets = [
        (None, {'fields': ('name', 'category', 'icon', 'display_order')}),
        ('Card content', {'fields': ('description', 'detailed_description', 'practical_tasks', 'related_tools')}),
    ]

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject','email','created_at','is_read']
    list_filter = ['is_read','created_at']
    search_fields = ['name','email','subject']
    readonly_fields = ['name','email','subject','message','created_at']
    actions = ['mark_read','mark_unread']
    def has_add_permission(self,request): return False
    @admin.action(description='Mark selected messages as read')
    def mark_read(self,request,queryset): queryset.update(is_read=True)
    @admin.action(description='Mark selected messages as unread')
    def mark_unread(self,request,queryset): queryset.update(is_read=False)
