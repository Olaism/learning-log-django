from django.urls import path

from .views import UserCreationView

app_name = 'users'

urlpatterns = [
    path('signup/', UserCreationView.as_view(), name='signup'),
]