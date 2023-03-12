from datetime import date

from django.shortcuts import render, redirect
from django.views import View

from StudentEnrollmentsPZ.enums import SettingsEnum
from .forms import CzatOgolnyForm
from .models import Grupy, Studenci, CzatOgolny, CzatPrywatny
from django.conf import settings


class IndexView(View):
    def get(self, request):
        studenci = Studenci.objects.all()  # query all students
        print(studenci.query)
        context = {'studenci': studenci}  # create a dictionary with the query results
        return render(request, 'app/index.html', context)  #


def send_message(request):
    if request.method == 'POST':
        form = CzatOgolnyForm(request.POST)
        if form.is_valid():
            czat = form.save(commit=False)
            czat.ID_studenta = request.user  # or however you want to set the foreign key
            czat.save()
            return redirect('chat')  # or wherever you want to redirect after successful submission
    else:
        form = CzatOgolnyForm()
    print('ok')
    return render(request, 'send_message.html', {'form': form})


class StudentsView(View):
    def get(self, request):
        studenci = Studenci.objects.all()  # query all students
        print(studenci.query)
        context = {'studenci': studenci}  # create a dictionary with the query results
        return render(request, 'app/students.html', context)  #

    def post(self, request):
        context = {}
        return render(request, 'app/students.html', context)  #


class GroupsView(View):
    def get(self, request):
        groups = Grupy.objects.all()  # query all students
        chat_messages = CzatOgolny.objects.all()
        print(groups.query)
        context = {'groups': groups, 'students_min': SettingsEnum.STUDENTS_MIN_THRESHOLD,
                   'students_max': SettingsEnum.STUDENTS_MAX_THRESHOLD, 'messages':'', 'chat_messages': chat_messages}  # create a dictionary with the query results
        return render(request, 'app/groups.html', context)  #

    def post(self, request):
        form = CzatOgolnyForm(request.POST)
        if form.is_valid():
            czat = form.save(commit=False)
            czat.data_wiadomosci = date.today()
            student = Studenci.objects.get(ID_studenta=22)
            czat.ID_studenta = student  # or however you want to set the foreign key
            czat.save()
            print("Save new record")
        else:
            print("Error with validation data")
        print(f"Errors = {form.errors}")
        form = CzatOgolnyForm()
        context = {'students_min': SettingsEnum.STUDENTS_MIN_THRESHOLD,
                   'students_max': SettingsEnum.STUDENTS_MAX_THRESHOLD, 'messages': 'ok'}  # create a dictionary with the query results
        return render(request, 'app/groups.html', context)  #


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
