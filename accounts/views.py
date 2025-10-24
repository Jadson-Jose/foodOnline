from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from vendor.forms import VendorForm

from .forms import UserForm
from .models import User, UserProfile


def registerUser(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration for customers.
    """
    if request.method == "POST":
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
    if request.method == "POST":
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
