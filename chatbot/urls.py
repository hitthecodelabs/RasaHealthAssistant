from django.urls import path
from . import views as chatbot_views
from django.views.generic.base import RedirectView

app_name = "chatbot"

urlpatterns = [
    path("", chatbot_views.home, name="home"),
    path('get_username/', chatbot_views.get_username, name='get_username'),
    path("medical_history/", chatbot_views.medical_history, name="medical_history"),

    #path("trote.png", chatbot_views.trote, name="trote.png"),
    #path('trote/', chatbot_views.trote),
    #path("caminata.png", chatbot_views.caminata, name="caminata.png"),
    #path('caminata/', chatbot_views.caminata),
    #path("flexiones.png", chatbot_views.flexiones, name="flexiones.png"),
    #path('flexiones/', chatbot_views.flexiones),

    # path('trote.png', RedirectView.as_view(url='/trote/', permanent=True)),
    # path('caminata.png', RedirectView.as_view(url='/caminata/', permanent=True)),
    # path('flexiones.png', RedirectView.as_view(url='/flexiones/', permanent=True)),
]
