from django.db import models


class Grupy(models.Model):
    ID = models.IntegerField(primary_key=True)
    Nazwa = models.CharField(max_length=32)


class Studenci(models.Model):
    ID_studenta = models.IntegerField(primary_key=True)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    ID_grupy = models.ForeignKey(Grupy, on_delete=models.CASCADE)


class CzatOgolny(models.Model):
    ID_wiadomosci = models.IntegerField(primary_key=True)
    tresc_wiadomosci = models.CharField(max_length=255, null=True)
    data_wiadomosci = models.DateField(null=True)
    ID_studenta = models.ForeignKey(Studenci, on_delete=models.CASCADE)


class CzatPrywatny(models.Model):
    ID_wiadomosci = models.IntegerField(primary_key=True)
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
