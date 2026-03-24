# from django.contrib import admin 
# from .models import Student


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'phone', 'standard', 'admission_date')


# class ExamAdmin(admin.ModelAdmin):
#     list_display = ('name', 'date', 'total_marks')
    
# admin.site.register(Student, StudentAdmin)



from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'standard', 'admission_date', 'discount')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('standard',)