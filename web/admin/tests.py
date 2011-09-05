from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from instances.models import Instance
from admin.fixtures import create_fixtures


class InstanceTestCase(TestCase):
    """
    Instances Administration Tests
    """    
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))    
        
    def _test_new_instance_fail(self):        
        """
        Check that new instance creation with no data specified returns error code 200.
        """
        response = self.client.post('/en/admin/instance/new/', {})
        self.assertEqual(200, response.status_code)
        
    def _get_instance_context(self):
        context = {'title': 'Test Title',
                   'city': 'Los Angeles',
                   'state': 'CA',
                   'days_for_mission': 7,
                   'start_date': '2011-09-05 00:48:40',
                   'curators': 1,
                   'languages': '1',
                   'map': '{"coordinates":[0,0],"zoom":16,"markers":[{"coordinates":[0,0]}],"type":"Point"}',
                   }
        for lang_code, _lang_name in settings.LANGUAGES:
            context['language_code_%s' % lang_code] = lang_code
            context['name_%s' % lang_code] = 'test name'
            context['description_%s' % lang_code] = 'test description'
        return context
    
    def test_new_instance_succeed(self):                    
        response = self.client.post('/en/admin/instance/new/', 
                                    self._get_instance_context())        
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/en/admin/", 
                         response.get('location', ''))
        
    def test_instance_edit(self):        
        test_instance =  Instance.objects.untranslated().get(pk=1)
        self.assertEqual("Test Title", test_instance.title)
        
        context = self._get_instance_context()
        context['title'] = 'New Title'
        context['name_es'] = 'amigo'
        context['name_ht'] = 'translated to ht'
        
        response = self.client.post('/en/admin/instance/edit/1/', 
                                    context)        
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/en/admin/", 
                         response.get('location', ''))
        
        test_instance =  Instance.objects.language('es').get(pk=1)
        self.assertEqual("New Title", test_instance.title)
        self.assertEqual("amigo", test_instance.name)
        
        test_instance =  Instance.objects.language('ht').get(pk=1)
        self.assertEqual("translated to ht", test_instance.name)        
        
        
class ValuesTest(TestCase):
    """
    Values Administration Tests
    """
    def setUp(self):
        self.client = Client()
        
    def test_new_value(self):
        print "To be implemented..."