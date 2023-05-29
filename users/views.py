from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrasiForm, UserUpdateForm

def registrasi(request):
    if request.method == 'POST':
        form = UserRegistrasiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Akun berhasil dibuat, silahkan masuk untuk melanjutkan!')
            return redirect('masuk')
    else:
        form = UserRegistrasiForm()
    return render(request, 'users/registrasi.html', {'form':form})

@login_required
def akun (request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Akun berhasil diperbarui!')
            return redirect ('akun')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'users/akun.html', context)
