from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages


def registerUser(request):

    if request.method == 'POST':

        form = UserForm(request.POST)
        if form.is_valid():

            # O método save() do form já cuida de setar a senha
            user = form.save(commit=False)
            
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully.')
            return redirect('registerUser')  # Ou redirecione para login
        else:
            print("Invalid form")
            print(form.errors)
    else:
        form = UserForm()
    
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
