from django.shortcuts import get_object_or_404, render, redirect
from .forms import AppointmentForm, PrescriptionForm
from .models import Appointment, Prescription


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient = request.user
            obj.save()
            return redirect(f'/appointments/appointments/{request.user.id}')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})


def appointments(request, **kwargs):
    if id_ := kwargs.pop('id', None):
        appointments = Appointment.objects.filter(patient__id=id_)
    else:
        appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'appointments': appointments})


def approve_appointment(request, appointment_id):

    prescription = Prescription()
    prescription.doctor = request.user
    prescription.save()
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.reject = False
    appointment.approved = True
    appointment.approved_by = request.user
    appointment.prescription = prescription
    appointment.save()

    
    return redirect(f'/appointments/appointments/{appointment.patient.id}')


def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.approved = False
    appointment.reject = True
    appointment.save()
    return redirect(f'/appointments/appointments/{appointment.patient.id}')


def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('appointments:appointments')


def prescription(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'prescription.html', {'appointment': appointment})


def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    prescription = appointment.prescription  # get the prescription associated with the appointment

    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)  # pass the instance to the form
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            appointment.prescription = prescription
            appointment.save()
            return redirect('appointments:appointments')
        else:
            print(f"Form errors: {form.errors}")

    return render(request, 'add_prescription.html', {'appointment': appointment})