from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student
from exam.models import Exam
from marks.models import Marks
from rest_framework import status

@api_view(['GET'])
def student_list(request):
    data = []

    students = Student.objects.all()

    for student in students:
        total_fees = 0
        discount = 0
        paid_fees = 0
        pending_fees = 0

        if hasattr(student, 'fees'):
            total_fees = student.fees.total_fees
            discount = student.fees.discount
            paid_fees = sum(p.amount for p in student.feepayment_set.all())
            pending_fees = total_fees - (paid_fees + discount)

        data.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "standard": student.standard.name if student.standard else None,
            "total_fees": total_fees,
            "discount": discount,
            "paid_fees": paid_fees,
            "pending_fees": pending_fees,
        })

    return Response(data)

@api_view(['POST'])
def bulk_marks_api(request):
    exam_id = request.data.get('exam')
    marks_data = request.data.get('marks')

    try:
        exam = Exam.objects.get(id=exam_id)   # ✅ ahiya
    except Exam.DoesNotExist:
        return Response({"error": "Exam not found"}, status=404)

    for item in marks_data:
        student_id = item.get('student_id')
        marks_value = item.get('marks')

        try:
            student = Student.objects.get(id=student_id, standard=exam.standard)   # ✅ ahiya main use
        except Student.DoesNotExist:
            return Response(
                {"error": f"Student {student_id} aa standard ma nathi"},
                status=400
            )

        Marks.objects.create(
            student=student,
            exam=exam,
            marks=marks_value
        )

    return Response({"message": "Marks added successfully"})

@api_view(['GET'])
def student_with_marks(request):
    student_id = request.GET.get('student')
    exam_id = request.GET.get('exam')
    subject = request.GET.get('subject')
    min_marks = request.GET.get('min')
    max_marks = request.GET.get('max')

    students = Student.objects.all()

    data = []

    for student in students:
        marks_qs = Marks.objects.filter(student=student)

        # 🔥 filters apply karo
        if student_id:
            if str(student.id) != student_id:
                continue

        if exam_id:
            marks_qs = marks_qs.filter(exam_id=exam_id)

        if subject:
            marks_qs = marks_qs.filter(subject__iexact=subject)

        if min_marks:
            marks_qs = marks_qs.filter(marks__gte=min_marks)

        if max_marks:
            marks_qs = marks_qs.filter(marks__lte=max_marks)

        marks_list = []
        for m in marks_qs:
            marks_list.append({
                "exam": m.exam.name,
                "subject": m.subject,
                "marks": m.marks,
                "total": m.exam.total_marks 
            })

        data.append({
            "id": student.id,
            "name": student.name,
            "marks": marks_list
        })

    return Response(data)

# exam list ke liye 

@api_view(['GET'])
def exam_list(request):
    exams = Exam.objects.all()

    data = []
    for exam in exams:
        data.append({
            "id": exam.id,
            "name": exam.name,
            "date": exam.date,
            "total_marks": exam.total_marks
        })

    return Response(data)

@api_view(['GET'])
def student_percentage(request):
    exam_id = request.GET.get('exam')
    marks_data = Marks.objects.select_related('student', 'exam').all()

    #filters apply karo
    if exam_id:
        marks_data = marks_data.filter(exam_id=exam_id)


    data = []

    for m in marks_data:
        total = m.exam.total_marks if m.exam.total_marks else 0

        percentage = 0
        if total > 0:
            percentage = (m.marks / total) * 100 

        data.append({
            "student": m.student.name,
            "exam": m.exam.name,
            "marks": m.marks,
            "total_marks": total,
            "percentage": f"{round(percentage, 2)}%"
        })

    return Response(data)

@api_view(['GET'])
def student_detail(request, id):
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    total_fees = 0
    discount = 0
    paid_fees = 0
    pending_fees = 0

    if hasattr(student, 'fees'):
        total_fees = student.fees.total_fees
        discount = student.fees.discount

        if hasattr(student, 'feepayment_set'):
            paid_fees = sum(p.amount for p in student.feepayment_set.all())

        pending_fees = total_fees - (paid_fees + discount)

    data = {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "phone": student.phone,
        "standard": student.standard.name if student.standard else None,
        "total_fees": total_fees,
        "discount": discount,
        "paid_fees": paid_fees,
        "pending_fees": pending_fees,
    }

    return Response(data)