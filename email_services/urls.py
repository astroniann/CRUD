from django.urls import path
from . import views

urlpatterns = [
    path('', views.campaigns, name='campaigns'),
    path('delete_campaign/<int:id>/', views.delete_campaign, name='delete_campaign'),
    path('update_campaign/<int:id>/', views.update_campaign, name='update_campaign'),
    path('send_campaign/<int:id>/', views.send_test_email, name='send_campaign'),
]
