from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token


def send_login_email(request: HttpRequest):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login") + "?token=" + str(token.uid))
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        "Your login link from Superlists",
        message_body,
        "noreply@superlists",
        [email],
    )
    messages.success(
        request, "Check your email, we've sent you a link you can use to login."
    )
    return redirect("/")


def login(request):
    user = auth.authenticate(uid=request.GET.get("token"))
    if user:
        auth.login(request, user)
    return redirect("/")


def logout(request):
    auth.logout(request)
    return redirect("/")
