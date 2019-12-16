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

    # Test the GET of all sites
    def test_site_get_list(self):
        response = self.client.get('/item/')
        response_data = response.data

        self.assertTrue(response_data[0]['active'])
        self.assertEquals(response_data[0]['name'], 'Test')
        self.assertEquals(response_data[0]['url'][0]['description'], 'test.com')
        self.assertEquals(response_data[0]['category'][0]['description'], 'test')

        self.assertFalse(response_data[1]['active'])
        self.assertEquals(response_data[1]['name'], 'Test 2')
        self.assertEquals(response_data[1]['url'][0]['description'], 'test2.com')
        self.assertEquals(response_data[1]['category'][0]['description'], 'test2')

    # Test the GET of one site with passed id
    def test_site_get_existing_id(self):
        response = self.client.get('/item/1')
        response_data = response.data

        self.assertTrue(response_data['active'])
        self.assertEquals(response_data['name'], 'Test')
        self.assertEquals(response_data['url'][0]['description'], 'test.com')
        self.assertEquals(response_data['category'][0]['description'], 'test')

    
    # Test the GET of a site with an id that doesnt exist
    def test_site_get_not_existing_id(self):
        response = self.client.get('/item/5')
        
        self.assertEquals(str(response.data['detail']), 'Not found.')

    # Test the DELETE of a site with an id
    def test_site_delete(self):
        sites_list = Sites.objects.all()

        self.assertEquals(2, len(sites_list))
        self.client.delete('/item/1')

        sites_list = Sites.objects.all()

        self.assertEquals(1, len(sites_list))
        self.assertEquals(sites_list[0].name, 'Test 2')

    # Test the DELETE of a site with an in that doesnt exist
    def test_site_delete_not_exist(self):

        sites_list = Sites.objects.all()

        self.assertEquals(2, len(sites_list))
        response = self.client.delete('/item/100')

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

    # Test the POST to create a new active site
    def test_site_create_active(self):
        body = self.base_body

        request = self.client.post('/item/', body, format='json')
        
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

    # Test the POST to create a new site that is inactive
    def test_site_create_inactive(self):
        body = self.base_body
        body['active'] = False

        request = self.client.post('/item/', body, format='json')
        
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

    # Test the POST to create a site passing multiples URLs
    def test_site_create_active_multiple_url(self):
        body = self.base_body
        body['url'].append({'description': 'newsite.com/new'})

        request = self.client.post('/item/', body, format='json')
        
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

    # Test the POST to create a site passing multiples Categories
    def test_site_create_active_multiple_category(self):
        body = self.base_body
        body['category'].append({'description': 'newsite2'})

        request = self.client.post('/item/', body, format='json')
        
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

    # Test if the new Category is created with the POST
    def test_site_create_new_category(self):
        body = self.base_body

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.post('/item/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(3, len(categories))

    # Test if the category is not created with the POST when the category already exists
    def test_site_create_existing_category(self):
        body = self.base_body
        body['category'][0]['description'] = 'test'

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.post('/item/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

    
    # Test if the URL is created with the POST
    def test_site_create_new_url(self):
        body = self.base_body

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.post('/item/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        urls = SiteURL.objects.all()

        self.assertEquals(3, len(urls))

    # Test if the URL is not created with the POST when the URL already exists
    def test_site_create_existing_url(self):
        body = self.base_body
        body['url'][0]['description'] = 'test.com'

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.post('/item/', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        
        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

    # Test if the a new Site is not created when data is empty
    def test_site_create_empty(self):
        request = self.client.post('/item/', {}, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name'][0]), 'This field is required.')
        self.assertEquals(str(request.data['url'][0]), 'This field is required.')
        self.assertEquals(str(request.data['category'][0]), 'This field is required.')

        sites = Sites.objects.all()
        self.assertEquals(len(sites), 2)
        
    # Test if the a new Site is not created when data is missing the category
    def test_site_create_missing_category(self):
        body = self.base_body
        del body['category']
        request = self.client.post('/item/', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['category'][0]), 'This field is required.')

    # Test if the a new Site is not created when data is missing the url
    def test_site_create_missing_url(self):
        body = self.base_body
        del body['url']
        request = self.client.post('/item/', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['url'][0]), 'This field is required.')

    # Test if the a new Site is not created when the url data is empty
    def test_site_create_empty_url(self):
        body = self.base_body
        body['url'] = []

        request = self.client.post('/item/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['url']), 'At least one URL is required')

    # Test if the a new Site is not created when the category data is empty
    def test_site_create_empty_category(self):
        body = self.base_body
        body['category'] = []

        request = self.client.post('/item/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['category']), 'At least one Category is required')

    # Test if it allow to create a site with the same name
    def test_site_create_name_already_exist(self):
        body = self.base_body
        body['name'] = 'Test'

        request = self.client.post('/item/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name']), 'This name already exists')

    # Test required field in URL    
    def test_site_create_wrong_field_name_url(self):
        body = self.base_body
        body['url'][0] = {'field_name': 'teste'}

        request = self.client.post('/item/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(str(request.data['url'][0]['description'][0]), 'This field is required.')

    # Test required field in Category
    def test_site_create_wrong_field_name_url(self):
        body = self.base_body
        body['category'][0] = {'field_name': 'teste'}

        request = self.client.post('/item/', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(str(request.data['category'][0]['description'][0]), 'This field is required.')

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


    # Test the PATCH to update a site
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

        request = self.client.patch('/item/1', body, format='json')
        
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

    # Test the PATCH to update a site to inactive
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

        request = self.client.patch('/item/1', body, format='json')
        
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

    # Test the PATCH to update a site passing multiples URLs
    def test_site_update_active_multiple_url(self):
        body = self.base_body
        body['url'].append({'description': 'newsite.com/new'})

        request = self.client.patch('/item/1', body, format='json')
        
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

    # Test the PATCH to update a site passing multiples Categories
    def test_site_update_active_multiple_category(self):
        body = self.base_body
        body['category'].append({'description': 'newsite2'})

        request = self.client.patch('/item/1', body, format='json')
        
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

    # Test if the category is updated with the POST
    def test_site_update_new_category(self):
        body = self.base_body

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.patch('/item/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(3, len(categories))

    # Test if the URL is not updated with the POST when the Category already exists
    def test_site_update_existing_category(self):
        body = self.base_body
        body['category'][0]['description'] = 'test'

        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

        request = self.client.patch('/item/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        categories = SiteCategory.objects.all()

        self.assertEquals(2, len(categories))

    # Test if the URL is updated with the PATCH
    def test_site_update_new_url(self):
        body = self.base_body

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.patch('/item/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        urls = SiteURL.objects.all()

        self.assertEquals(3, len(urls))

    # Test if the URL is not updated with the PATCH when the URL already exists
    def test_site_update_existing_url(self):
        body = self.base_body
        body['url'][0]['description'] = 'test.com'

        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

        request = self.client.patch('/item/1', body, format='json')
        
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        
        urls = SiteURL.objects.all()

        self.assertEquals(2, len(urls))

    # Test if the a new Site is not updated when the data is empty
    def test_site_update_empty(self):
        request = self.client.patch('/item/1', {}, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name'][0]), 'This field is required.')
        self.assertEquals(str(request.data['url'][0]), 'This field is required.')
        self.assertEquals(str(request.data['category'][0]), 'This field is required.')
        
    # Test if the a new Site is not updated when the category is missing
    def test_site_update_missing_category(self):
        body = self.base_body
        del body['category']
        request = self.client.patch('/item/1', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['category'][0]), 'This field is required.')

    # Test if the a new Site is not updated when the url is missing
    def test_site_update_missing_url(self):
        body = self.base_body
        del body['url']
        request = self.client.patch('/item/1', body, format='json')

        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['url'][0]), 'This field is required.')

    # Test if the a new Site is not updated when the url data is empty
    def test_site_update_empty_url(self):
        body = self.base_body
        body['url'] = []

        request = self.client.patch('/item/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['url']), 'At least one URL is required')

    # Test if the a new Site is not updated when the category data is empty
    def test_site_update_empty_category(self):
        body = self.base_body
        body['category'] = []

        request = self.client.patch('/item/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['errors'][0]['category']), 'At least one Category is required')

    # Test PATCH using a name that already exist
    def test_site_update_name_already_exist(self):
        body = self.base_body
        body['name'] = 'Test 2'

        request = self.client.patch('/item/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(str(request.data['name']), 'This name already exists')

    # Test PATCH without changing the name
    def test_site_update_name_already_exist_same_object(self):
        body = self.base_body
        body['name'] = 'Test'

        site = Sites.objects.get(id=1)
        self.assertEquals(site.name, 'Test')

        urls = site.url.all()

        self.assertEquals(urls[0].description, 'test.com')

        request = self.client.patch('/item/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_200_OK)

        self.assertEquals(str(request.data['name']), 'Test')

        site = Sites.objects.get(id=1)
        self.assertEquals(site.name, 'Test')

        urls = site.url.all()

        self.assertEquals(urls[0].description, 'newsite.com')

    # Test required field in URL    
    def test_site_update_wrong_field_name_url(self):
        body = self.base_body
        body['url'][0] = {'field_name': 'teste'}

        request = self.client.patch('/item/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(str(request.data['url'][0]['description'][0]), 'This field is required.')

    # Test required field in Category
    def test_site_update_wrong_field_name_url(self):
        body = self.base_body
        body['category'][0] = {'field_name': 'teste'}

        request = self.client.patch('/item/1', body, format='json')
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(str(request.data['category'][0]['description'][0]), 'This field is required.')
