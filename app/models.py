# models.py
from django.db import models

class Supervisor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField("Student", blank=True, related_name='groups')
    supervisor = models.ForeignKey(
        "Supervisor", on_delete=models.CASCADE, blank=True, null=True
    )


class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    requests = models.ManyToManyField("Request", blank=True, related_name='students')

class Request(models.Model):
    sender = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="sender_requests"
    )
    recipient = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="recipient_requests"
    )
    status = models.CharField(max_length=50)
