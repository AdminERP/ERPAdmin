from unittest import TestCase

from django.http import JsonResponse
from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
# Create your tests here.
from apps.employees_and_jobs.models import Job, Employee
import json

class TestGenerar_nomina(TestCase):
    client = Client()
    def setUp(self):

        """
        Test: Generate a payroll and register it in the database.
        Necessary: register an employee

        """

        self.job = Job.objects.create(name='JobTest',
                                      description='Description job test',
                                      functions='functions job test')
        Employee.objects.create(id= '1',name= 'EmployeeTest',
                                id_type=['CC'],
                                identification='111',
                                email='jhonier.calero@correounivalle.edu.co',
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


    def test_generar_nomina(self):

        response = self.client.post(reverse_lazy('creacion_nomina'))
        print(response)
        print(response.content)
        response_message = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_message['type'], "success")
        self.assertTrue("La nomina ha sido registrada correctamente para cada colaborador."
                        in response_message['message'])
