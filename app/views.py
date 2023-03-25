from datetime import date

from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from reportlab.lib.pagesizes import A4
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from StudentsEnrollments_25_03.enums import SettingsEnum
from .forms import CzatOgolnyForm, LoginForm, NewUserForm
from .models import Grupy, Studenci, CzatOgolny, CzatPrywatny, Transfer
from django.conf import settings
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


class RegisterView(View):
    def get(self, request):
        form = NewUserForm()
        context = {"form": form}
        return render(request, "accounts/register.html", context)

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            print("form save..")
        context = {"form": form}
        return render(request, "accounts/login.html", context)


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print("auth..")
        if user is not None:
            print("ok..")
            login(request, user)
            return redirect("index")
        else:
            print(f"nie ok err:{form.errors}")
            return render(
                request,
                "accounts/login.html",
                {"error": "Login lub hasło nieprawidłowe.", "form": form},
            )

    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "app/logowanie.html"


class ProfileLogout(LoginRequiredMixin, TemplateView):
    template_name = "app/index.html"

    def get(self, request):
        logout(request)
        return redirect("login")


class IndexView(View):
    def get(self, request):
        studenci = Studenci.objects.all()  # query all students
        print(studenci.query)
        context = {"studenci": studenci}  # create a dictionary with the query results
        print(f"Username: {request.user.username}, id={request.user.id}")
        return render(request, "app/index.html", context)  #


def send_message(request):
    if request.method == "POST":
        form = CzatOgolnyForm(request.POST)
        if form.is_valid():
            czat = form.save(commit=False)
            czat.ID_studenta = (
                request.user
            )  # or however you want to set the foreign key
            czat.save()
            return redirect(
                "chat"
            )  # or wherever you want to redirect after successful submission
    else:
        form = CzatOgolnyForm()
    print("ok")
    return render(request, "send_message.html", {"form": form})


class StudentsView(View):
    def get(self, request):
        studenci = Studenci.objects.all()  # query all students
        print(studenci.query)
        context = {"studenci": studenci}  # create a dictionary with the query results
        return render(request, "app/students.html", context)  #

    def post(self, request):
        context = {}
        return render(request, "app/students.html", context)  #


class ChatMain(View):
    def get(self, request):
        chat_messages = CzatOgolny.objects.all()
        return render(request, "app/chat_main.html", {"chat_messages": chat_messages})

    def post(self, request):
        form = CzatOgolnyForm(request.POST)
        groups = Grupy.objects.all()  # query all students
        chat_messages = CzatOgolny.objects.all()
        print(f"Form type: {request.POST.get('transfer_form')}")
        if form.is_valid():
            czat = form.save(commit=False)
            czat.data_wiadomosci = date.today()
            student = Studenci.objects.get(user__id=request.user.id)
            czat.ID_studenta = student  # or however you want to set the foreign key
            czat.save()
            print(f"User id = {request.user.id}")
            print("Save new record")
        else:
            print("Error with validation data")
        print(f"Errors = {form.errors}")
        context = {
            "groups": groups,
            "students_min": SettingsEnum.STUDENTS_MIN_THRESHOLD,
            "chat_messages": chat_messages,
            "students_max": SettingsEnum.STUDENTS_MAX_THRESHOLD,
            "messages": "ok",
        }  # create a dictionary with the query results
        return render(request, "app/chat_main.html", context)  #


class ChatPrivate(View):
    def get(self, request):
        chat_messages = CzatOgolny.objects.all()
        return render(
            request, "app/chat_private.html", {"chat_messages": chat_messages}
        )


class GroupsView(View):
    def get(self, request):
        # groups = Grupy.objects.all()  # query all students
        groups = Grupy.objects.all().prefetch_related(
            Prefetch("id_grupy", queryset=Studenci.objects.order_by("imie"))
        )
        chat_messages = CzatOgolny.objects.all()
        transfers = Transfer.objects.filter(approved=None)
        transfer_approved = Transfer.objects.filter(approved__isnull=False)
        try:
            my_group_nr = Studenci.objects.get(user__id=request.user.id).ID_grupy
        except Exception:
            my_group_nr = 0
        print(groups.query)
        context = {
            "transfer_approved": transfer_approved,
            "transfers": transfers,
            "groups": groups,
            "students_min": SettingsEnum.STUDENTS_MIN_THRESHOLD,
            "students_max": SettingsEnum.STUDENTS_MAX_THRESHOLD,
            "messages": "",
            "chat_messages": chat_messages,
            "my_group_nr": my_group_nr if my_group_nr else "brak",
        }  # create a dictionary with the query results
        return render(request, "app/groups.html", context)  #

    def post(self, request):
        form = CzatOgolnyForm(request.POST)
        groups = Grupy.objects.all()  # query all students
        chat_messages = CzatOgolny.objects.all()
        transfers = Transfer.objects.filter(approved=None)
        transfer_approved = Transfer.objects.filter(approved__isnull=False)
        my_group_nr = Studenci.objects.get(user__id=request.user.id).ID_grupy
        print(f"Form type: {request.POST.get('transfer_form')}")
        if request.POST.get("transfer_form") == "transfer_form":
            print("transfer")
            requester_student_ID = request.POST.get("requester_student_ID")
            exchanger_student_ID = request.POST.get("exchanger_student_ID")

            req_student = Studenci.objects.get(user__id=requester_student_ID)
            exch_student = Studenci.objects.get(user__id=exchanger_student_ID)
            # Create a new Transfer object
            transfer = Transfer(
                requester_student_ID=req_student,
                exchanger_student_ID=exch_student,
                approved=None,
            )

            transfer.save()
        elif request.POST.get("transfer_form") == "approve_form":
            transfer_id = request.POST.get("transfer_id")
            print(
                f"transfer_form = {request.POST.get('transfer_form')} id={transfer_id}"
            )
            transfer_item = Transfer.objects.get(ID_transfer=transfer_id)
            transfer_item.approved = True
            transfer_item.save()

            previous = transfer_item.exchanger_student_ID.ID_grupy
            transfer_item.exchanger_student_ID.ID_grupy = (
                transfer_item.requester_student_ID.ID_grupy
            )
            transfer_item.requester_student_ID.ID_grupy = previous

            transfer_item.requester_student_ID.save()
            transfer_item.exchanger_student_ID.save()

        elif request.POST.get("transfer_form") == "reject_form":
            transfer_id = request.POST.get("transfer_id")
            print(
                f"transfer_form = {request.POST.get('transfer_form')} id={transfer_id}"
            )
            exch_student = Transfer.objects.get(ID_transfer=transfer_id)
            exch_student.approved = False
            exch_student.save()
        elif request.POST.get("transfer_form") == "join_to_group":
            print("join")
            group_id = request.POST.get("group_id")
            my_group = Grupy.objects.get(ID=group_id)
            my_student = Studenci.objects.get(user__id=request.user.id)
            my_student.ID_grupy = my_group
            my_student.save()
        else:
            print("not transfer")
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
        try:
            my_group_nr = Studenci.objects.get(user__id=request.user.id).ID_grupy
        except Exception:
            my_group_nr = 0
        context = {
            "transfer_approved": transfer_approved,
            "transfers": transfers,
            "groups": groups,
            "students_min": SettingsEnum.STUDENTS_MIN_THRESHOLD,
            "students_max": SettingsEnum.STUDENTS_MAX_THRESHOLD,
            "messages": "ok",
            "chat_messages": chat_messages,
            "my_group_nr": my_group_nr if my_group_nr else "brak",
        }  # create a dictionary with the query results
        return render(request, "app/groups.html", context)  #


def grupy(request):
    grupy = Grupy.objects.all()
    return render(request, "grupy.html", {"grupy": grupy})


def studenci(request):
    studenci = Studenci.objects.all()
    return render(request, "studenci.html", {"studenci": studenci})


def group_report(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    groups = Grupy.objects.all().prefetch_related(
        Prefetch("id_grupy", queryset=Studenci.objects.order_by("imie"))
    )

    page_height = A4[1]
    top_margin = 50
    bottom_margin = 50
    y = page_height - top_margin
    line_height = 20
    gap_between_groups = 40

    for group in groups:
        # Check if the group name and at least one student fit on the current page
        if y - (line_height * (len(group.id_grupy.all()) + 2)) < bottom_margin:
            p.showPage()
            y = page_height - top_margin

        p.drawString(100, y, f"Grupa {group.Nazwa}")
        y -= line_height
        for student in group.id_grupy.all():
            p.drawString(
                120, y, f"{student.ID_studenta} {student.imie} {student.nazwisko}"
            )
            y -= line_height

        y -= gap_between_groups

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="group_report.pdf")
