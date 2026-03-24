from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/', views.student_detail),
    path('api/bulk-marks/', views.bulk_marks_api, name='bulk-marks'),
    path('api/student-marks/', views.student_with_marks, name='student-marks'),
    path('api/exams/', views.exam_list, name='exam-list'),
    path('api/percentage/', views.student_percentage, name='student-percentage'),
    path('list/',views.student_list,name='student-list'),
    
]
