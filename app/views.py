# views.py
from django.views import View
from django.shortcuts import render

class LoginView(View):
    def get(self, request):
        # Logowanie bez rejestracji
        return render(request, 'app/logowanie.html')

class ChangePasswordView(View):
    def post(self, request):
        # Zmiana hasła
        pass

class ChangeGroupView(View):
    def post(self, request):
        # Zamiana grup
        pass

class RequestsListView(View):
    def get(self, request):
        # Lista z requestami
        pass

class ChatView(View):
    def get(self, request):
        # Czat ogólny
        pass

class PrivateChatView(View):
    def get(self, request):
        # Czat prywatny
        pass

class NotificationView(View):
    def get(self, request):
        # Dzwoneczek powiadomień
        pass

class PrintView(View):
    def get(self, request):
        # Drukowanie listy grup-studentów do PDF
        pass

class DeleteStudentView(View):
    def post(self, request):
        # Usunięcie studenta przez Dziekana
        pass

class AcceptRequestView(View):
    def post(self, request):
        # Akceptacja zamiany
class RejectRequestView(View):
    def post(self, request):

# Odrzucenie zamiany
        pass

class MoveStudentView(View):
    def post(self, request):

# Przemieszczenie studenta między grupami
        pass

class ConfirmActionView(View):
    def get(self, request):
        pass