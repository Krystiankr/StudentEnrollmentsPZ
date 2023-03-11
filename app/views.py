from django.shortcuts import render
from django.views import View

from .models import Grupy, Studenci, CzatOgolny, CzatPrywatny

from django.conf import settings


class IndexView(View):
    def get(self, request):
        studenci = Studenci.objects.all()  # query all students
        print(studenci.query)
        context = {'studenci': studenci}   # create a dictionary with the query results
        return render(request, 'app/index.html', context)  #
def grupy(request):
    grupy = Grupy.objects.all()
    return render(request, 'grupy.html', {'grupy': grupy})


def studenci(request):
    studenci = Studenci.objects.all()
    return render(request, 'studenci.html', {'studenci': studenci})


def czat_ogolny(request):
    wiadomosci = CzatOgolny.objects.all()
    return render(request, 'czat_ogolny.html', {'wiadomosci': wiadomosci})


def czat_prywatny(request):
    wiadomosci = CzatPrywatny.objects.all()
    return render(request, 'czat_prywatny.html', {'wiadomosci': wiadomosci})
