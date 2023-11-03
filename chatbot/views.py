import os
import json
from glob import glob
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

os.makedirs("temp", exist_ok=True)

@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        # username = request.user.username
        json_f = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        # 'date_joined': user.date_joined,
        'user_type': user.user_type,
        'gender': user.gender,
        'phone': user.phone,
        'emergency_contact_number': user.emergency_contact_number,
        'current_address': user.current_address,
        # 'permanent_address': user.permanent_address,
        'id_number': user.id_number,
        # 'note': user.note
    }
        json_object = json.dumps(json_f, indent=4)
        # Writing to sample.json
        with open("temp/temp.json", "w") as outfile:
            outfile.write(json_object)
    return render(request, 'chatbot/home.html')

@login_required
def medical_history(request):
    return render(request, 'chatbot/medical_history.html')

@login_required
def trote(request):
    #with open("chatbot/trote.png", 'rb') as f:
    #    return HttpResponse(f.read(), content_type='image/png')
    #    # return render(request, 'chatbot/trote.png')
    return FileResponse(open('chatbot/trote.png', 'rb'), content_type='image/png')

@login_required
def caminata(request):
    #with open("chatbot/caminata.png", 'rb') as f:
    #    return HttpResponse(f.read(), content_type='image/png')
    #    # return render(request, 'chatbot/caminata.png')
    return FileResponse(open('chatbot/caminata', 'rb'), content_type='image/png')

@login_required
def flexiones(request):
    print(glob("*/*"))
    #with open("chatbot/flexiones.png", 'rb') as f:
    #    return HttpResponse(f.read(), content_type='image/png')
    #    # return render(request, 'chatbot/flexiones.png')
    return FileResponse(open('chatbot/flexiones.png', 'rb'), content_type='image/png')

@login_required
def get_username(request):
    if request.user.is_authenticated:
        user = request.user
        # username = request.user.username
        json_f = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        # 'date_joined': user.date_joined,
        'user_type': user.user_type,
        'gender': user.gender,
        'phone': user.phone,
        'emergency_contact_number': user.emergency_contact_number,
        'current_address': user.current_address,
        # 'permanent_address': user.permanent_address,
        'id_number': user.id_number,
        # 'note': user.note
    }
        json_object = json.dumps(json_f, indent=4)
        # Writing to sample.json
        with open("temp/temp.json", "w") as outfile:
            outfile.write(json_object)
        return JsonResponse(json_f)
    else:
        return JsonResponse({'error': 'User not authenticated'})
