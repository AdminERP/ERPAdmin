from unittest import TestCase

from django.test import TestCase
from django.test import Client


# Create your tests here.
class TestRegistrar_pregunta(TestCase):
    def test_create_questions_with_str(self):
        client = Client()
        """
        Register a question in database.
        Check if it redirects after POST.
        """
        response = self.response = client.post('/registrar-pregunta',
                                               {'question_statement': 'Test question?'})
        self.assertEqual(response.status_code, 302)
        message = response.wsgi_request._messages._queued_messages[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("La pregunta ha sido guardada correctamente." in message.message)


    def test_create_questions_empty(self):
        client = Client()
        """
        Register a question in database.
        Check if it redirects after POST.
        """
        response = self.response = client.post('/registrar-pregunta',
                                               {'question_statement': ''})
        self.assertEqual(response.status_code, 200)
        message = response.wsgi_request._messages._loaded_messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Por favor verificar los campos en rojo." in message.message)

