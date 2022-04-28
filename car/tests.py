from django.test import TestCase

# Create your tests here.
import datetime

from django.test import TestCase
from django.urls import reverse
from django.test.client import Client

from car.models import Car, User


class UnitTest(TestCase):

    def create_car(self):
        Car.objects.create(
            modal='Top',
            make='X7',
            condition='good',
            price=2000,
            seller=self.user,
            description='test',
            year=datetime.datetime.now()
        )

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testUser',
            first_name='test',
            last_name='user',
            email='testuser@gmail.com',
            mobile='123456789'
        )
        self.user.set_password('Testing#123')
        self.user.save()
        self.create_car()

    def test_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_POST(self):
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_invalid_login_POST(self):
        response = self.client.post('/login/', {'username': 'test123', 'password': 'test@123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be '
                                      'case-sensitive.')

    def test_valid_login_POST(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)

    def test_signup_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_list_car_page(self):
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_list.html')

    def test_add_valid_car_data(self):
        response = self.client.post('/add/', data={
            "modal": 'Top',
            "make": 'X7',
            "condition": 'good',
            "price": 2000,
            "seller": self.user,
            "description": 'test',
            "year": datetime.datetime.now()
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_car.html')

    def test_add_invalid_car_data(self):
        response = self.client.post('/add/', data={
            "modal": 'Top',
            "make": 'X7',
            "condition": 'good',
            "price": 99,
            "seller": self.user,
            "description": 'test',
            "year": datetime.datetime.now()
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_car.html')
        self.assertContains(response, 'Enter valid price')

    def test_car_buy(self):
        response = self.client.post('/car/1', data={
            "modal": 'Top',
            "make": 'X7',
            "condition": 'good',
            "price": 2000,
            "seller": self.user,
            "description": 'test',
            "year": datetime.datetime.now()
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_details.html')
