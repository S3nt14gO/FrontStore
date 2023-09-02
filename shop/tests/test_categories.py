from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from shop.models import Category , Product
from model_bakery import baker

# @pytest.mark.django_db
# # @pytest.mark.skip
# class TestCreateCategory:
#     def test_if_user_is_anonymous_returns_401(self):
#         #arrange


#         #act
#         client = APIClient()
#         response = client.post('/store/categories/', {'title': 'a'})

#         #assert 
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         # assert response.status_code != status.HTTP_401_UNAUTHORIZED
# @pytest.fixture
# def create_category(api_client):
#     def do_create_category(category):
#         return api_client.post('/store/categories/', category)
#     return do_create_category


# @pytest.mark.django_db
# class TestCreateCategory:
#     def test_if_user_is_anonymous_returns_403(self, authenticate, create_category):
#         # client = APIClient()
#         # api_client.force_authenticate(user={})
#         authenticate()
#         # response = api_client.post('/store/categories/', {'title': 'a'})
#         response = create_category({'title': 'a'})

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
#         # client = APIClient()
#         # api_client.force_authenticate(user=User(is_staff=True))
#         authenticate(is_staff=True)
#         response = create_category({'title': ''})
#         # response = api_client.post('/store/categories/',{'title': ''})
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['title'] is not None

#     def test_if_data_is_valid_returns_201(self, authenticate, create_category):
#         # client = APIClient()
#         authenticate(is_staff=True)
#         # api_client.force_authenticate(user=User(is_staff=True))
#         # response = api_client.post('/store/categories/', {'title': 'a'})
#         response = create_category({'title': 'a'})
        
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCategory:
    def test_if_category_exists_returns_200(self,api_client):
        #arrange
        # Category.objects.create(title='a')
        category = baker.make(Category)
        response = api_client.get(f'/store/categories/{category.id}/'), 
        # category = baker.make(Product, _quantity=77)
        # print(category.__dict__)

        assert response.status_code == status.HTTP_200_OK
        # assert response.data['id'] == category.id
        # assert response.data['title'] == category.title
        assert response.data == {
            'id': category.id,
            'title': category.title
        }

