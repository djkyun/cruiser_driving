from django.test import RequestFactory
from django.urls import reverse
from website.views import about_us,contact,register
import pytest

@pytest.mark.django_db
class TestViews:

    def test_about_us(self):
        path = reverse('about_us', kwargs = {})
        request = RequestFactory().get(path)
        
        response = about_us(request)        
        assert response.status_code == 200
        
    def test_contact(self):
        path = reverse('contact', kwargs = {})
        request = RequestFactory().get(path)
        
        response = contact(request)        
        assert response.status_code == 200
        
    def test_register(self):
        path = reverse('register', kwargs = {})
        request = RequestFactory().get(path)
        
        response = register(request)        
        assert response.status_code == 200        
   