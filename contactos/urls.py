from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'contactos'

urlpatterns = [
    path('', views.lista_contactos, name='lista_contactos'),
    path('nuevo/', views.crear_contacto, name='crear_contacto'),
    path('<int:pk>/', views.detalle_contacto, name='detalle_contacto'),
    path('<int:pk>/editar/', views.editar_contacto, name='editar_contacto'),
    path('<int:pk>/eliminar/', views.eliminar_contacto, name='eliminar_contacto'),
    path('<int:pk>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('buscar/', views.buscar_contactos, name='buscar_contactos'),
    path('exportar/', views.exportar_contactos, name='exportar_contactos'),
    path('logout/', views.custom_logout, name='logout'),
]


urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]