from users.models import AllUser
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Prescription(models.Model):
    doctor = models.ForeignKey(
        AllUser, on_delete=models.CASCADE, related_name='prescriptions_written', null=True)
    patient_need = models.TextField(null=True)
    patient_condition = models.TextField(null=True)

    def __str__(self):
        return str(self.id)


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name='ID')
    appointment_date = models.DateField(null=True)
    appointment_time = models.TimeField(null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(AllUser, on_delete=models.Case, null=True, related_name='approved_by')
    prescription = models.OneToOneField(
        'Prescription', on_delete=models.CASCADE, null=True)
    reject = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment with {self.phone_number} on {self.appointment_date} at {self.appointment_time}'