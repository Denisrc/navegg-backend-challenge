from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from sites.models import Sites, SiteCategory, SiteURL

# Test the GET and the DELETE methods
class SiteGetDeleteTestCase(APITestCase):
    def setUp(self):
        url_test = SiteURL.objects.create(description='test.com')
        url_test2 = SiteURL.objects.create(description='test2.com')
        
        category_test = SiteCategory.objects.create(description='test')
        category_test2 = SiteCategory.objects.create(description='test2')

        site = Sites.objects.create(name="Test", active=True)
        site.url.set([url_test])
        site.category.set([category_test])
        site.save()

        site2 = Sites.objects.create(name="Test 2", active=False)
        site2.url.set([url_test2])
        site2.category.set([category_test2])
        site2.save()

    def test_site_get_list(self):
        response = self.client.get('/api/site/')
        response_data = response.data

        self.assertTrue(response_data[0]['active'])
        self.assertEquals(response_data[0]['name'], 'Test')
        self.assertEquals(response_data[0]['url'][0]['description'], 'test.com')
        self.assertEquals(response_data[0]['category'][0]['description'], 'test')

        self.assertFalse(response_data[1]['active'])
        self.assertEquals(response_data[1]['name'], 'Test 2')
        self.assertEquals(response_data[1]['url'][0]['description'], 'test2.com')
        self.assertEquals(response_data[1]['category'][0]['description'], 'test2')

    def test_site_get_existing_id(self):
        response = self.client.get('/api/site/1')
        response_data = response.data

        self.assertTrue(response_data['active'])
        self.assertEquals(response_data['name'], 'Test')
        self.assertEquals(response_data['url'][0]['description'], 'test.com')
        self.assertEquals(response_data['category'][0]['description'], 'test')

    
    def test_site_get_not_existing_id(self):
        response = self.client.get('/api/site/5')
        
        self.assertEquals(str(response.data['detail']), 'Not found.')

    def test_site_delete(self):
        sites_list = Sites.objects.all()

        self.assertEquals(2, len(sites_list))
        self.client.delete('/api/site/1')

        sites_list = Sites.objects.all()

        self.assertEquals(1, len(sites_list))
        self.assertEquals(sites_list[0].name, 'Test 2')

    def test_site_delete_not_exist(self):

        sites_list = Sites.objects.all()

        self.assertEquals(2, len(sites_list))
        response = self.client.delete('/api/site/100')

        sites_list = Sites.objects.all()

        self.assertEquals(2, len(sites_list))

        self.assertEquals(str(response.data['detail']), 'Not found.')

# Test the POST method
class SiteCreateTestCase(APITestCase):
    def setUp(self):
        url_test = SiteURL.objects.create(description='test.com')
        url_test2 = SiteURL.objects.create(description='test2.com')
        
        category_test = SiteCategory.objects.create(description='test')
        category_test2 = SiteCategory.objects.create(description='test2')

        site = Sites.objects.create(name="Test", active=True)
        site.url.set([url_test])
        site.category.set([category_test])
        site.save()

        site2 = Sites.objects.create(name="Test 2", active=False)
        site2.url.set([url_test2])
        site2.category.set([category_test2])
        site2.save()

        self.base_body = {
            'name': 'New Site',
            'url': [{'description': 'newsite.com'}],
            'category': [{'description': 'newsite'}]
        }

    def test_site_create_active(self):
        body = self.base_body

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        self.assertEquals(request.data['id'], 3)

        site = Sites.objects.get(id=3)

        self.assertEquals(site.name, 'New Site')
        self.assertTrue(site.active)

        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'newsite.com')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'newsite')

    def test_site_create_inactive(self):
        body = self.base_body
        body['active'] = False

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        self.assertEquals(request.data['id'], 3)

        site = Sites.objects.get(id=3)

        self.assertEquals(site.name, 'New Site')
        self.assertFalse(site.active)

        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'newsite.com')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'newsite')

    def test_site_create_active_multiple_url(self):
        body = self.base_body
        body['url'].append({'description': 'newsite.com/new'})

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        self.assertEquals(request.data['id'], 3)

        site = Sites.objects.get(id=3)

        self.assertEquals(site.name, 'New Site')
        self.assertTrue(site.active)
        
        urls = site.url.all()
        categories = site.category.all()

        self.assertEquals(len(urls), 2)
        self.assertEquals(urls[0].description, 'newsite.com')
        self.assertEquals(urls[1].description, 'newsite.com/new')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'newsite')

    def test_site_create_active_multiple_category(self):
        body = self.base_body
        body['category'].append({'description': 'newsite2'})

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        self.assertEquals(request.data['id'], 3)

        site = Sites.objects.get(id=3)

        self.assertEquals(site.name, 'New Site')
        self.assertTrue(site.active)
        
        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'newsite.com')

        self.assertEquals(len(categories), 2)
        self.assertEquals(categories[0].description, 'newsite')
        self.assertEquals(categories[1].description, 'newsite2')

    def test_site_create_new_category(self):
        body = self.base_body

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(3, len(categories))

    def test_site_create_existing_category(self):
        body = self.base_body
        body['category'][0]['description'] = 'test'

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

    
    def test_site_create_new_url(self):
        body = self.base_body

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        urls = SiteURL.objects.all()

        self.assertEquals(3, len(urls))

    def test_site_create_existing_url(self):
        body = self.base_body
        body['url'][0]['description'] = 'test.com'

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.post('/api/site/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

    def test_site_create_empty(self):
        request = self.client.post('/api/site/', {}, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name'][0]), 'This field is required.')
        self.assertEquals(str(request.data['url'][0]), 'This field is required.')
        self.assertEquals(str(request.data['category'][0]), 'This field is required.')
        
    def test_site_create_missing_category(self):
        body = self.base_body
        del body['category']
        request = self.client.post('/api/site/', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['category'][0]), 'This field is required.')

    def test_site_create_missing_url(self):
        body = self.base_body
        del body['url']
        request = self.client.post('/api/site/', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['url'][0]), 'This field is required.')

    
    def test_site_create_empty_url(self):
        body = self.base_body
        body['url'] = []

        request = self.client.post('/api/site/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['url']), 'At least one URL is required')

    def test_site_create_empty_category(self):
        body = self.base_body
        body['category'] = []

        request = self.client.post('/api/site/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['category']), 'At least one Category is required')

    def test_site_create_name_already_exist(self):
        body = self.base_body
        body['name'] = 'Test'

        request = self.client.post('/api/site/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name']), 'This name already exists')

# Test the PATCH method
class SiteUpdateTestCase(APITestCase):
    def setUp(self):
        url_test = SiteURL.objects.create(description='test.com')
        url_test2 = SiteURL.objects.create(description='test2.com')
        
        category_test = SiteCategory.objects.create(description='test')
        category_test2 = SiteCategory.objects.create(description='test2')

        site = Sites.objects.create(name="Test", active=True)
        site.url.set([url_test])
        site.category.set([category_test])
        site.save()

        site2 = Sites.objects.create(name="Test 2", active=False)
        site2.url.set([url_test2])
        site2.category.set([category_test2])
        site2.save()

        self.base_body = {
            'name': 'New Site',
            'url': [{'description': 'newsite.com'}],
            'category': [{'description': 'newsite'}]
        }

    def test_site_update_active(self):
        body = self.base_body

        site = Sites.objects.get(id=1)
        self.assertEquals(site.name, 'Test')
        self.assertTrue(site.active)

        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'test.com')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'test')

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(request.data['id'], 1)

        site = Sites.objects.get(id=1)

        self.assertEquals(site.name, 'New Site')
        self.assertTrue(site.active)

        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'newsite.com')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'newsite')

    def test_site_update_inactive(self):
        body = self.base_body
        body['active'] = False

        site = Sites.objects.get(id=1)
        self.assertEquals(site.name, 'Test')
        self.assertTrue(site.active)

        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'test.com')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'test')

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(request.data['id'], 1)

        site = Sites.objects.get(id=1)

        self.assertEquals(site.name, 'New Site')
        self.assertFalse(site.active)

        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'newsite.com')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'newsite')

    def test_site_update_active_multiple_url(self):
        body = self.base_body
        body['url'].append({'description': 'newsite.com/new'})

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(request.data['id'], 1)

        site = Sites.objects.get(id=1)

        self.assertEquals(site.name, 'New Site')
        self.assertTrue(site.active)
        
        urls = site.url.all()
        categories = site.category.all()

        self.assertEquals(len(urls), 2)
        self.assertEquals(urls[0].description, 'newsite.com')
        self.assertEquals(urls[1].description, 'newsite.com/new')

        self.assertEquals(len(categories), 1)
        self.assertEquals(categories[0].description, 'newsite')

    def test_site_update_active_multiple_category(self):
        body = self.base_body
        body['category'].append({'description': 'newsite2'})

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(request.data['id'], 1)

        site = Sites.objects.get(id=1)

        self.assertEquals(site.name, 'New Site')
        self.assertTrue(site.active)
        
        urls = site.url.all()
        categories = site.category.all()
        
        self.assertEquals(len(urls), 1)
        self.assertEquals(urls[0].description, 'newsite.com')

        self.assertEquals(len(categories), 2)
        self.assertEquals(categories[0].description, 'newsite')
        self.assertEquals(categories[1].description, 'newsite2')

    def test_site_update_new_category(self):
        body = self.base_body

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(3, len(categories))

    def test_site_update_existing_category(self):
        body = self.base_body
        body['category'][0]['description'] = 'test'

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

    
    def test_site_update_new_url(self):
        body = self.base_body

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        urls = SiteURL.objects.all()

        self.assertEquals(3, len(urls))

    def test_site_update_existing_url(self):
        body = self.base_body
        body['url'][0]['description'] = 'test.com'

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.patch('/api/site/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

    def test_site_update_empty(self):
        request = self.client.patch('/api/site/1', {}, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name'][0]), 'This field is required.')
        self.assertEquals(str(request.data['url'][0]), 'This field is required.')
        self.assertEquals(str(request.data['category'][0]), 'This field is required.')
        
    def test_site_update_missing_category(self):
        body = self.base_body
        del body['category']
        request = self.client.patch('/api/site/1', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['category'][0]), 'This field is required.')

    def test_site_update_missing_url(self):
        body = self.base_body
        del body['url']
        request = self.client.patch('/api/site/1', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['url'][0]), 'This field is required.')

    
    def test_site_update_empty_url(self):
        body = self.base_body
        body['url'] = []

        request = self.client.patch('/api/site/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['url']), 'At least one URL is required')

    def test_site_update_empty_category(self):
        body = self.base_body
        body['category'] = []

        request = self.client.patch('/api/site/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['category']), 'At least one Category is required')

    def test_site_update_name_already_exist(self):
        body = self.base_body
        body['name'] = 'Test 2'

        request = self.client.patch('/api/site/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name']), 'This name already exists')


    def test_site_update_name_already_exist_same_object(self):
        body = self.base_body
        body['name'] = 'Test'

        request = self.client.patch('/api/site/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_200_OK)

        self.assertEquals(str(request.data['name']), 'Test')
