from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_activation_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://localhost:8000/api/users/activate/{uid}/{token}/"

    subject = "Aktiviere deinen Videoflix-Account"
    message = f"Hallo,\nBitte aktiviere deinen Account über diesen Link: {activation_link}"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
