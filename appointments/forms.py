from django import forms
from .models import Appointment, Prescription

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['phone_number', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'})
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient_need', 'patient_condition']
