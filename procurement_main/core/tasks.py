from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_email(order_id, email):
    send_mail(
        "Заказ подтвержден",
        f"Ваш заказ №{order_id}",
        "noreply@test.com",
        [email]
    )