from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Marks
from students.models import Student
from exam.models import Exam
from standard.models import Standard

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'marks']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-add/', self.admin_site.admin_view(self.bulk_add_marks), name='bulk-add-marks'),
        ]
        return custom_urls + urls

    def bulk_add_marks(self, request):
        standards = Standard.objects.all()
        exams = []
        students = []

        selected_standard = request.POST.get('standard') or request.GET.get('standard')
        selected_exam = request.POST.get('exam') or request.GET.get('exam')
        subject = request.POST.get('subject', '')

        if selected_standard:
            exams = Exam.objects.filter(standard_id=selected_standard)
            students = Student.objects.filter(standard_id=selected_standard)

        if request.method == 'POST' and 'save_bulk' in request.POST:
            if not selected_standard or not selected_exam or not subject:
                messages.error(request, "Standard, Exam and Subject required.")
            else:
                try:
                    exam = Exam.objects.get(id=selected_exam, standard_id=selected_standard)
                    students = Student.objects.filter(standard_id=selected_standard)

                    saved_count = 0

                    for student in students:
                        marks_value = request.POST.get(f'marks_{student.id}')
                        if marks_value not in [None, '']:
                            Marks.objects.update_or_create(
                                student=student,
                                exam=exam,
                                subject=subject,
                                defaults={'marks': marks_value}
                            )
                            saved_count += 1

                    messages.success(request, f"{saved_count} students na marks save thai gaya.")
                    return redirect("..")
                except Exam.DoesNotExist:
                    messages.error(request, "Selected exam invalid che.")

        context = {
            **self.admin_site.each_context(request),
            'title': 'Bulk Add Marks',
            'standards': standards,
            'exams': exams,
            'students': students,
            'selected_standard': selected_standard,
            'selected_exam': selected_exam,
            'subject': subject,
        }
        return render(request, 'admin/bulk_add_marks.html', context)