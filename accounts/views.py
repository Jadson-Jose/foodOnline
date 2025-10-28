from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from vendor.forms import VendorForm

from .forms import UserForm
from .models import User, UserProfile
from .utils import detectUser


def registerUser(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration for customers.
    """
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("dashboard")

    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()

            messages.success(request, "Your account has been registered successfully!")
            return redirect("registerUser")
        else:
            print("Form validation failed:")
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserForm()

    context = {"form": form}
    return render(request, "accounts/registerUser.html", context)


def registerVendor(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("dashboard")

    elif request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = User.VENDOR
                user.save()
                user_profile = UserProfile.objects.get(user=user)

                # Criar o vendor
                vendor = v_form.save(commit=False)
                vendor.user = user
                vendor.user_profile = user_profile
                vendor.save()

                messages.success(
                    request,
                    "Your vendor account has been created successfully! Please wait for the approval.",
                )
                return redirect("registerVendor")

            except UserProfile.DoesNotExist:
                # Se chegou aqui, o signal NÃO funcionou
                messages.error(
                    request, "Error creating vendor profile. Please try again."
                )
                print("ERROR: UserProfile was not created by signal!")

        else:
            print("Invalid form")
            print("User form errors:", form.errors)
            print("Vendor form errors:", v_form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {"form": form, "v_form": v_form}
    return render(request, "accounts/registerVendor.html", context)


def login(request):
    # Se o usuário já está autenticado, redireciona para a conta apropriada
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("myAccount")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Validação
        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect("login")

        print(f"Login attempt for email: {email}")  # Debug

        try:
            # Tenta autenticar o usuário
            user = auth.authenticate(request, username=email, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(
                    request, f"Welcome back, {user.first_name or user.username}!"
                )
                print(f"Login successful for: {email}")  # Debug

                # Redireciona para a próxima URL ou para myAccount
                next_url = (
                    request.POST.get("next") or request.GET.get("next") or "myAccount"
                )
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                print(f"Login failed for: {email}")  # Debug
                return redirect("login")

        except Exception as e:
            messages.error(request, "An error occurred during login. Please try again.")
            print(f"Login error: {e}")  # Debug
            return redirect("login")

    # Mostra o formulário de login para GET requests
    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required(login_url="login")
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)


@login_required(login_url="login")
def custDashboard(request):
    print(f"Usuário acessando dashboard: {request.user}")  # Debug
    print(f"Usuário autenticado: {request.user.is_authenticated}")  # Debug

    context = {
        "user": request.user,
    }
    return render(request, "accounts/custDashboard.html", context)


@login_required(login_url="login")
def vendorDashboard(request):
    print(f"Usuário acessando dashboard: {request.user}")  # Debug
    print(f"Usuário autenticado: {request.user.is_authenticated}")  # Debug

    context = {
        "user": request.user,
    }
    return render(request, "accounts/vendorDashboard.html", context)
