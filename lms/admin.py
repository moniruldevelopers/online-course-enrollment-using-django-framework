from django.contrib import admin
from .models import *
import csv
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext as _
from reportlab.pdfgen import canvas


from django.utils.html import format_html


#my customizations
admin.site.site_header = "UGV COURSES ADMIN PANEL"
admin.site.site_title = "UGV COURSES ADMIN PANEL"
admin.site.index_title = "Welcome to UGV COURSES  PORTAL"
# Register your models here.

admin.site.register(SiteInfo)

class VideoInline(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin): 
    def display_banner(self, obj):
        return format_html('<img src="{}" width="100" height="auto" />', obj.banner.url)

    display_banner.short_description = 'banner'
    inlines = [VideoInline]
    list_filter = ['author', 'category']
    search_fields = ['title', 'author__name']
    list_display = [ 'title','author', 'category','display_banner']
    list_per_page=100 


admin.site.register(Course, CourseAdmin)

admin.site.register(Author)
admin.site.register(Category)


class EnrollmentAdmin(ImportExportModelAdmin):     
    list_display = ["approved", "phone_number", "transaction_id","batch_no", "course_price", "user", "student_id", "department", "semester", "portal_screenshot", "course"]
    list_per_page=200     
    list_filter = ["batch_no","approved", "department", "semester", "course"]
    # Define the export action
    def export_selected(self, request, queryset):
        return super().export_action(request, queryset)
    export_selected.short_description = "Export selected Enrollers"

admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Wishlist)
admin.site.register(Team)
admin.site.register(Contact)