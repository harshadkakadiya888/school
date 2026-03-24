import csv
from io import StringIO

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from fees.models import Fees


class Command(BaseCommand):
    help = "Send one pending fees report email to admin"

    def handle(self, *args, **kwargs):
        fees = Fees.objects.select_related("student").all()

        rows = []
        for fee in fees:
            paid_fees = sum(payment.amount for payment in fee.student.feepayment_set.all())
            rows.append({
                "name": fee.student.name,
                "total_fees": fee.total_fees,
                "paid_fees": paid_fees,
                "discount": fee.discount,
                "pending": fee.pending,
            })

        html_body = render_to_string("emails/pending_fees_report.html", {
            "rows": rows
        })

        text_body = "All students pending fees report is attached and included in HTML format."

        email = EmailMultiAlternatives(
            subject="All Students Pending Fees Report",
            body=text_body,
            from_email="harshadkakadiya888@gmail.com",
            to=["harshadkakadiya888@gmail.com"],
        )

        # HTML body attach
        email.attach_alternative(html_body, "text/html")

        # CSV attachment create
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["No", "Student Name", "Total Fees", "Paid Fees", "Discount", "Pending Fees"])

        for index, row in enumerate(rows, start=1):
            writer.writerow([
                index,
                row["name"],
                row["total_fees"],
                row["paid_fees"],
                row["discount"],
                row["pending"],
            ])

        email.attach(
            "pending_fees_report.csv",
            csv_buffer.getvalue(),
            "text/csv",
        )

        email.send()

        self.stdout.write(self.style.SUCCESS("Report email sent successfully"))