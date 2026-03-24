from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Fees, FeePayment
from students.models import Student


@api_view(['GET', 'POST'])
def fees_list(request):
    if request.method == 'GET':
        fees = Fees.objects.select_related('student').all()

        data = []
        for f in fees:
            payments = FeePayment.objects.filter(student=f.student)
            total_paid = sum(p.amount for p in payments)
            pending = f.total_fees - (total_paid + f.discount)

            data.append({
                "student_id": f.student.id,
                "student": f.student.name,
                "total_fees": f.total_fees,
                "discount": f.discount,
                "paid_fees": total_paid,
                "pending_fees": pending
            })

        return Response(data)

    if request.method == 'POST':
        try:
            student_id = request.data.get('student')
            total_fees = int(request.data.get('total_fees', 0))
            discount = int(request.data.get('discount', 0))

            student = Student.objects.get(id=student_id)

            if Fees.objects.filter(student=student).exists():
                return Response({"error": "Fees already added for this student"}, status=400)

            Fees.objects.create(
                student=student,
                total_fees=student.standard.total_fees,
                paid_fees=0
            )

            return Response({"message": "Fees added successfully ✅"})

        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def fees_detail(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)

    try:
        fees = Fees.objects.get(student=student)
    except Fees.DoesNotExist:
        return Response({"error": "Fees not found"}, status=404)

    payments = FeePayment.objects.filter(student=student).order_by('date', 'id')

    history = []
    total_paid = 0

    for p in payments:
        total_paid += p.amount
        history.append({
            "id": p.id,
            "amount": p.amount,
            "date": str(p.date)
        })

    pending = fees.total_fees - (total_paid + fees.discount)

    data = {
        "student_id": student.id,
        "student": student.name,
        "total_fees": fees.total_fees,
        "discount": fees.discount,
        "paid_fees": total_paid,
        "pending_fees": pending,
        "history": history
    }

    return Response(data)


@api_view(['POST'])
def add_payment(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)

    try:
        amount = int(request.data.get('amount', 0))

        if amount <= 0:
            return Response({"error": "Amount must be greater than 0"}, status=400)

        if not Fees.objects.filter(student=student).exists():
            return Response({"error": "First add fees record for this student"}, status=400)

        payment = FeePayment.objects.create(
            student=student,
            amount=amount
        )

        return Response({
            "message": "Payment added successfully ✅",
            "payment_id": payment.id,
            "amount": payment.amount,
            "date": str(payment.date)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@property
def pending(self):
    payments_total = sum(p.amount for p in self.student.feepayment_set.all())
    return self.total_fees - (payments_total + self.discount)