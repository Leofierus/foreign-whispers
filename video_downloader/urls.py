from django.urls import path
from . import views

urlpatterns = [
    path('download/', views.download_video, name='download_video'),
    path('data/<video_id>/', views.download_status, name='download_status'),
    path('download_subtitle/<str:video_id>/<str:language>/', views.download_subtitle, name='download_subtitle')
]