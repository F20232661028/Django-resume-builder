from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = "Welcome to ProResume Builder!"
    message = render_to_string("emails/welcome.txt", {"user": user})
    html_message = render_to_string("emails/welcome.html", {"user": user})
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message,
    ) 