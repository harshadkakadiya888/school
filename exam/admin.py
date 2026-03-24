from django.contrib import admin
from .models import Exam

admin.site.register(Exam)

class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'standard', 'date', 'course', 'total_marks']
    list_filter = ['standard', 'date']
    search_fields = ['name', 'standard__name', 'course']