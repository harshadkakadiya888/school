from django.urls import path
from . import views

urlpatterns = [
    path('', views.fees_list, name='fees-list'),
    path('api/<int:student_id>/', views.fees_detail, name='fees-detail'),
    path('api/<int:student_id>/pay/', views.add_payment, name='add-payment'),
]
