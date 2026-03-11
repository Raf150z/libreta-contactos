from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contactos import views as contactos_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', contactos_views.home, name='home'),
    path('registrar/', contactos_views.registrar, name='registrar'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('contactos/', include('contactos.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
