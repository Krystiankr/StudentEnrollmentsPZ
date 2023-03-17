from django.contrib.auth.models import AbstractUser
from django.db import models


class Grupy(models.Model):
    ID = models.AutoField(primary_key=True)
    Nazwa = models.CharField(max_length=32)

    def __str__(self):
        return str(self.Nazwa)


class Studenci(models.Model):
    ID_studenta = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    mail = models.CharField(max_length=50, unique=True)
    ID_grupy = models.ForeignKey(Grupy, on_delete=models.CASCADE, related_name='id_grupy')

    def __str__(self):
        return f"[{self.ID_grupy}] {self.imie} {self.nazwisko}"

class Transfer(models.Model):
    ID_transfer = models.AutoField(primary_key=True)
    requester_student_ID = models.ForeignKey(Studenci, on_delete=models.CASCADE, related_name='requested_transfers')
    exchanger_student_ID = models.ForeignKey(Studenci, on_delete=models.CASCADE, related_name='exchanged_transfers')
    approved = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.ID_transfer} ({self.requester_student_ID} - {self.exchanger_student_ID})"

class CzatOgolny(models.Model):
    ID_wiadomosci = models.AutoField(primary_key=True)
    tresc_wiadomosci = models.CharField(max_length=255, null=True)
    data_wiadomosci = models.DateField(null=True)
    ID_studenta = models.ForeignKey(Studenci, on_delete=models.CASCADE)


class CzatPrywatny(models.Model):
    ID_wiadomosci = models.AutoField(primary_key=True)
    tresc_wiadomosci = models.CharField(max_length=255, null=True)
    data_wiadomosci = models.DateField(null=True)
    ID_studenta_nadawcy = models.ForeignKey(Studenci, on_delete=models.CASCADE, related_name='nadawca')
    ID_studenta_odbiorcy = models.ForeignKey(Studenci, on_delete=models.CASCADE, related_name='odbiorca')

class Request(models.Model):
    sender = models.ForeignKey(
        Studenci, on_delete=models.CASCADE, related_name="sender_requests"
    )
    recipient = models.ForeignKey(
        Studenci, on_delete=models.CASCADE, related_name="recipient_requests"
    )
    status = models.CharField(max_length=50)
