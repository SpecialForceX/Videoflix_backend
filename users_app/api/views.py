from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users_app.api.serializers import RegistrationSerializer
from users_app.tasks import send_activation_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from users_app.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect



class RegistrationView(APIView):
    """
    API endpoint for user registration.

    Accepts user data (like email and password), validates it using the
    RegistrationSerializer, and sends an activation email upon success.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.

        If the data is valid, the user is created and an activation email is sent.
        Returns a success message or an error message.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(user) 
            return Response({"detail": "Bitte bestätige deine E-Mail-Adresse."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Bitte überprüfe deine Eingaben und versuche es erneut."}, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    """
    API endpoint for account activation via email confirmation.

    This view is accessed through a link sent to the user's email.
    It checks the token and activates the user account if valid.
    """
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        """
        Activate user account.

        Decodes the user ID, validates the token, and activates the user if valid.
        Redirects to frontend with query parameter indicating activation status.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("https://patrickbatke.de/videoflix/login?activated=true")
        else:
            return redirect("https://patrickbatke.de/videoflix/login?activated=false")


class PasswordResetRequestView(APIView):
    """
    API endpoint for initiating a password reset.

    Accepts an email address and sends a password reset link if the user exists and is active.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Send password reset email.

        If the email exists and belongs to an active user, a password reset link is emailed.
        Always returns a generic message for security reasons.
        """
        email = request.data.get("email")
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    reset_link = f"https://patrickbatke.de/videoflix/reset-password/{uid}/{token}/"


                    subject = "Setze dein Videoflix-Passwort zurück"
                    text_content = f"Setze dein Passwort zurück: {reset_link}"
                    html_content = render_to_string("emails/password_reset.html", {
                        "reset_link": reset_link,
                        "user": user,
                    })

                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

            except CustomUser.DoesNotExist:
                pass 

        return Response({"detail": "If the email exists, a reset link has been sent."})
    
class PasswordResetConfirmView(APIView):
    """
    API endpoint for setting a new password using a reset link.

    Verifies the token and user ID from the URL, and resets the password if valid.
    """
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        """
        Reset the user's password.

        Requires matching 'password' and 'password2' in the request body.
        If valid, sets the new password for the user.
        """
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response({"detail": "Passwords do not match."}, status=400)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({"detail": "Password has been reset successfully."})
        except Exception:
            pass

        return Response({"detail": "Invalid or expired reset link."}, status=400)