from django.shortcuts import render, redirect
from .forms import SuscripcionForm


def inicio(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/?suscrito=ok#canastos')
        return render(request, 'index.html', {'form': form, 'modal_abierto': True})
    form = SuscripcionForm()
    suscrito = request.GET.get('suscrito') == 'ok'
    return render(request, 'index.html', {'form': form, 'suscrito': suscrito})
