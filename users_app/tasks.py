from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def send_activation_email(user):
    print("📨 send_activation_email() wurde aufgerufen!")
    print("➡️ Mail geht an:", user.email)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"https://videoflix.patrickbatke.de/api/users/activate/{uid}/{token}/"

    subject = "Activate your Videoflix Account"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    # HTML-Inhalt aus dem Template
    html_content = render_to_string("emails/activation.html", {
        "user": user,
        "activation_link": activation_link
    })

    # Fallback-Text für einfache Mail-Clients
    text_content = f"Hello,\nPlease activate your account using this link:\n{activation_link}"

    # Mail zusammensetzen und senden
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

