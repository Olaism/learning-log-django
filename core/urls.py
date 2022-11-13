from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('logs/', include('logs.urls', namespace='logs')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls', namespace='users')),
    path('', TemplateView.as_view(template_name='home.html', extra_context={'section': 'home'}), name='home')
]
