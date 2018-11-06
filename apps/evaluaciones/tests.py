from unittest import TestCase

from django.test import TestCase
from django.test import Client
from apps.prueba2.models import Job

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






class TestRegistrar_evaluacion(TestCase):
    def test_registrar_evaluacion(self):
        client = Client()
        """
        Test: Register an evaluation in database.
        Necessary: register a job (employee until merge), 2 questions and create the evaluation to that job (employee)
        
        Check if it redirects after POST.
        """
        client.post('/registrar-cargo',{'id':'1','name': 'JobTest1', 'description': 'Description job test',
                                                'functions': 'functions job test'})
        client.post('/registrar-pregunta',{'question_statement': 'Test question1?'})
        client.post('/registrar-pregunta', {'question_statement': 'Test question2?'})
        client.get('/crear-evaluacion/1')
        response = client.post('/registrar-evaluacion/1',
                               {'form-0-score': ['0'], 'form-0-observation': ['Observation test1'], 'form-0-id': ['1'],
                                'form-1-score': ['4'], 'form-1-observation': ['Observation test2'], 'form-1-id': ['2'],
                                'form-TOTAL_FORMS': ['2'], 'form-INITIAL_FORMS': ['2'], 'form-MIN_NUM_FORMS': ['0'],
                                'form-MAX_NUM_FORMS': ['2']})
        print(response)
        self.assertEqual(response.status_code, 302)
        message = response.wsgi_request._messages._queued_messages[0]
        print(message.message)
        self.assertEqual(message.tags, "success")
        self.assertTrue("La evaluacion ha sido guardada correctamente." in message.message)
