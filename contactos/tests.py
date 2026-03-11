from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Contacto

class ContactoModelTest(TestCase):
    """Pruebas para el modelo Contacto"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.contacto = Contacto.objects.create(
            usuario=self.usuario,
            nombre='Juan Pérez',
            telefono='555-123-4567',
            email='juan@example.com',
            direccion='Calle Principal 123'
        )
    
    def test_creacion_contacto(self):
        """Probar que el contacto se crea correctamente"""
        self.assertEqual(self.contacto.nombre, 'Juan Pérez')
        self.assertEqual(self.contacto.usuario.username, 'testuser')
        self.assertTrue(isinstance(self.contacto, Contacto))
    
    def test_string_representation(self):
        """Probar la representación en string"""
        self.assertEqual(
            str(self.contacto),
            f"{self.contacto.nombre} - {self.usuario.username}"
        )
    
    def test_contacto_pertenece_usuario(self):
        """Probar que el contacto pertenece al usuario correcto"""
        self.assertEqual(self.contacto.usuario, self.usuario)

class ContactoViewsTest(TestCase):
    """Pruebas para las vistas de contactos"""
    
    def setUp(self):
        """Configurar cliente de prueba y datos"""
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.contacto = Contacto.objects.create(
            usuario=self.usuario,
            nombre='Juan Pérez',
            telefono='555-123-4567',
            email='juan@example.com'
        )
    
    def test_lista_contactos_requiere_login(self):
        """Probar que la lista requiere autenticación"""
        response = self.client.get(reverse('contactos:lista_contactos'))
        self.assertNotEqual(response.status_code, 200)
    
    def test_lista_contactos_con_login(self):
        """Probar lista de contactos con usuario autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('contactos:lista_contactos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
    
    def test_usuario_solo_ve_sus_contactos(self):
        """Probar que un usuario solo ve sus propios contactos"""
        otro_usuario = User.objects.create_user(
            username='otro',
            password='testpass123'
        )
        Contacto.objects.create(
            usuario=otro_usuario,
            nombre='María García'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('contactos:lista_contactos'))
        
        self.assertContains(response, 'Juan Pérez')
        self.assertNotContains(response, 'María García')
    
    def test_crear_contacto(self):
        """Probar creación de contacto"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('contactos:crear_contacto'), {
            'nombre': 'Nuevo Contacto',
            'telefono': '555-987-6543',
            'email': 'nuevo@example.com'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertTrue(Contacto.objects.filter(nombre='Nuevo Contacto').exists())
    
    def test_editar_contacto(self):
        """Probar edición de contacto"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('contactos:editar_contacto', args=[self.contacto.id]),
            {
                'nombre': 'Juan Actualizado',
                'telefono': self.contacto.telefono,
                'email': self.contacto.email
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.contacto.refresh_from_db()
        self.assertEqual(self.contacto.nombre, 'Juan Actualizado')
    
    def test_eliminar_contacto(self):
        """Probar eliminación de contacto"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('contactos:eliminar_contacto', args=[self.contacto.id])
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contacto.objects.filter(id=self.contacto.id).exists())
    
    def test_no_editar_contacto_de_otro(self):
        """Probar que no se puede editar contacto de otro usuario"""
        otro_usuario = User.objects.create_user(
            username='otro',
            password='testpass123'
        )
        otro_contacto = Contacto.objects.create(
            usuario=otro_usuario,
            nombre='Contacto Ajeno'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('contactos:editar_contacto', args=[otro_contacto.id])
        )
        
        self.assertEqual(response.status_code, 404)

class AutenticacionTest(TestCase):
    """Pruebas para el sistema de autenticación"""
    
    def setUp(self):
        self.client = Client()
    
    def test_registro_usuario(self):
        """Probar registro de nuevo usuario"""
        response = self.client.post(reverse('registrar'), {
            'username': 'nuevousuario',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='nuevousuario').exists())
    
    def test_login(self):
        """Probar inicio de sesión"""
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirección
    
    def test_logout(self):
        """Probar cierre de sesión"""
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        
        self.assertEqual(response.status_code, 302)