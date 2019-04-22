from unittest import TestCase

from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy

from apps.employees_and_jobs.models import Job, Employee
from apps.evaluaciones.models import Question

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
    client = Client()
    def setUp(self):

        """
        Test: Register an evaluation in database.
        Necessary: register an employee, 2 questions and create the evaluation to that job (employee)

        Check if it redirects after POST.
        """

        self.job = Job.objects.create(name='JobTest',
                                      description='Description job test',
                                      functions='functions job test')
        Employee.objects.create(id= '1',name= 'EmployeeTest',
                                id_type=['CC'],
                                identification='111',
                                address='Address test 1',
                                telephone='1234567',
                                eps='EPSTest',
                                pension_fund='PensionFundTest',
                                severance_fund='SeveranceFundTest',
                                bank=['DAVIVIENDA'],
                                account_number='1234567890',
                                salary='1000000',
                                cargo=self.job,
                                status='True')

        Question.objects.create(question_statement='Test question1?')
        Question.objects.create(question_statement='Test question2?')
        self.client.get('/crear-evaluacion/1')

    def test_registrar_evaluacion(self):

        response = self.client.post(reverse_lazy('registrar_evaluacion', kwargs={'id': 1}),
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

    def test_registrar_evaluacion_without_observations(self):

        response = self.client.post(reverse_lazy('registrar_evaluacion', kwargs={'id': 1}),
                               {'form-0-score': ['0'], 'form-0-observation': [''], 'form-0-id': ['1'],
                                'form-1-score': ['4'], 'form-1-observation': ['Observation test2'], 'form-1-id': ['2'],
                                'form-TOTAL_FORMS': ['2'], 'form-INITIAL_FORMS': ['2'], 'form-MIN_NUM_FORMS': ['0'],
                                'form-MAX_NUM_FORMS': ['2']})
        self.assertEqual(response.status_code, 200)
        message = response.wsgi_request._messages._loaded_messages[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Por favor verificar los campos en rojo." in message.message)
