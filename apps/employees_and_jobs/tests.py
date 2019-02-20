from unittest import TestCase

from django.test import TestCase
from django.test import Client


# Create your tests here.
class TestRegistrar_cargo(TestCase):
    def test_create_jobs_with_str(self):
        client = Client()
        """
        Register a job in database.
        Check if it redirects after POST.
        """
        response = self.response = client.post('/registrar-cargo',
                                               {'name': 'JobTest', 'description': 'Description job test',
                                                'functions': 'functions job test'})
        self.assertEqual(response.status_code, 302)
        message = response.wsgi_request._messages._queued_messages[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("El cargo ha sido guardado correctamente." in message.message)


    def test_create_jobs_empty_name(self):
        client = Client()
        """
        Register a question in database.
        Check if it redirects after POST.
        """
        response = self.response = client.post('/registrar-cargo',
                                               {'name': '', 'description': 'Description job test',
                                                'functions': 'functions job test'})
        self.assertEqual(response.status_code, 200)
        message = response.wsgi_request._messages._loaded_messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Por favor verificar los campos en rojo." in message.message)

    def test_create_jobs_empty_description(self):
        client = Client()
        """
        Register a question in database.
        Check if it redirects after POST.
        """
        response = self.response = client.post('/registrar-cargo',
                                               {'name': 'Job test', 'description': '',
                                                'functions': 'functions job test'})
        self.assertEqual(response.status_code, 200)
        message = response.wsgi_request._messages._loaded_messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Por favor verificar los campos en rojo." in message.message)

    def test_create_jobs_empty_functions(self):
        client = Client()
        """
        Register a question in database.
        Check if it redirects after POST.
        """
        response = self.response = client.post('/registrar-cargo',
                                               {'name': 'Job test', 'description': 'Description job test',
                                                'functions': ''})
        self.assertEqual(response.status_code, 200)
        message = response.wsgi_request._messages._loaded_messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Por favor verificar los campos en rojo." in message.message)

