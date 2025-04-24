from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def send_activation_email(user):
    """
    Sends an account activation email to the specified user.

    The email includes a unique activation link constructed using a token and
    a base64-encoded user ID. The HTML content is rendered from a template,
    with a plain text fallback for email clients that do not support HTML.

    Args:
        user (CustomUser): The user instance to whom the activation email will be sent.

    Returns:
        None
    """
    print("📨 send_activation_email() wurde aufgerufen!")
    print("➡️ Mail geht an:", user.email)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"https://videoflix.patrickbatke.de/api/users/activate/{uid}/{token}/"

    subject = "Activate your Videoflix Account"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    html_content = render_to_string("emails/activation.html", {
        "user": user,
        "activation_link": activation_link
    })

    text_content = f"Hello,\nPlease activate your account using this link:\n{activation_link}"

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

