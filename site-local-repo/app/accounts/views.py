import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import User
from .forms import EmailForm, CodeForm, RegisterForm


def login_or_register(request):
    #  Handle manual reset from query (?login=1 or ?register=1)
    if "login" in request.GET:
        request.session["auth_step"] = "email"
        return redirect("login")
    if "register" in request.GET:
        request.session["auth_step"] = "register"
        return redirect("login")

    step = request.session.get("auth_step", "email")

    # --- STEP 1: EMAIL LOGIN ---
    if step == "email":
        form = EmailForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                email = form.cleaned_data["email"].strip().lower()
                user = User.objects.filter(email=email).first()

                if not user:
                    messages.error(request, "Email not found. Please register first.")
                    return redirect("login")

                # Generate verification code
                code = f"{random.randint(100000, 999999)}"
                user.verification_code = code
                user.save()
                send_mail(
                    "Your Login Code",
                    f"Your code: {code}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                request.session["pending_email"] = email
                request.session["auth_step"] = "code"
                messages.success(request, "Verification code sent to your email.")
                return redirect("login")
            else:
                messages.error(request, "Enter a valid email address.")

        return render(request, "accounts/login_email.html", {"form": form})

    # --- STEP 2: REGISTER NEW USER ---
    if step == "register":
        form = RegisterForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower().strip()
            code = f"{random.randint(100000, 999999)}"
            user.verification_code = code
            user.save()
            send_mail(
                "Verify your email",
                f"Your code: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            request.session["pending_email"] = user.email
            request.session["auth_step"] = "code"
            messages.success(request, "Check your email for the code.")
            return redirect("login")
        return render(request, "accounts/register.html", {"form": form})

    # --- STEP 3: VERIFY CODE ---
    if step == "code":
        email = request.session.get("pending_email")
        form = CodeForm(request.POST or None)
        if request.method == "POST" and form.is_valid() and email:
            code = form.cleaned_data["code"]
            user = User.objects.filter(email=email, verification_code=code).first()
            if user:
                user.is_verified = True
                user.verification_code = ""
                user.save()
                login(request, user)
                request.session.pop("auth_step", None)
                request.session.pop("pending_email", None)
                messages.success(request, f"Welcome back, {user.first_name or 'user'}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid code. Please try again.")
        return render(request, "accounts/enter_code.html", {"form": form, "email": email})

    # fallback
    request.session["auth_step"] = "email"
    return redirect("login")


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("home")
