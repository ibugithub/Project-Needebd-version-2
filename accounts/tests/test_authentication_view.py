from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from accounts.utils import generate_token


class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('tregister')
        self.user={
            'email':'testemail@gmail.com',
            'phone': '024343',
            'username':'username',
            'password':'password',
            'password2':'password',
            
        }

        return super().setUp()

class RegisterTest(BaseTest):
   def test_can_view_page_correctly(self):
       response=self.client.get(self.register_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'accounts/register.html')

   def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)


       


