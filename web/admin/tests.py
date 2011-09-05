from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from instances.models import Instance
from values.models import Value
from admin.fixtures import create_fixtures
from admin.forms import ValueForm


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
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))    
        
    def _get_value_context(self, test_instance):
        context = {'coins': 10,
                   'instance': test_instance.pk}
        for lang in test_instance.languages.all():
            lang_code = lang.code
            context['language_code_%s' % lang_code] = lang_code
            context['message_%s' % lang_code] = 'test'            
        return context    
        
    def test_new_value(self):
        test_instance = Instance.objects.untranslated().get(pk=1)
        
        response = self.client.post('/en/admin/value/%s/new/' % test_instance.pk, 
                                    self._get_value_context(test_instance))        
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/en/admin/value/%s/" % test_instance.pk, 
                         response.get('location', ''))
        
    def test_edit_value(self):
        test_instance = Instance.objects.untranslated().get(pk=1)
        test_value = Value.objects.untranslated().get(pk=1)      
        self.assertEqual(0, test_value.coins)
        
        response = self.client.post('/en/admin/value/%s/edit/%s/' % (test_instance.pk, test_value.pk), 
                                    self._get_value_context(test_instance))        
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/en/admin/value/%s/" % test_instance.pk, 
                         response.get('location', ''))
        
        test_value = Value.objects.untranslated().get(pk=1)      
        self.assertEqual(10, test_value.coins)
        
    def test_edit_value_is_not_pollute(self):
        """
        Ensure that new value instance is not created
        """  
        test_instance = Instance.objects.untranslated().get(pk=1)
        test_value = Value.objects.untranslated().get(pk=1)      
        self.assertEqual(1, Value.objects.untranslated().all().count())
        
        response = self.client.post('/en/admin/value/%s/edit/%s/' % (test_instance.pk, test_value.pk), 
                                    self._get_value_context(test_instance))        
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/en/admin/value/%s/" % test_instance.pk, 
                         response.get('location', ''))
        
        self.assertEqual(1, Value.objects.untranslated().all().count())
        
        
class ValueFormTest(TestCase):
    """
    Value Form tests.
    """
    def setUp(self):
        create_fixtures()
        
    def test_form_inner_forms_count(self):        
        test_instance = Instance.objects.untranslated().get(pk=1)        
        form = ValueForm(value_instance=test_instance)
        
        self.assertEqual(1, test_instance.languages.all().count())
        self.assertEqual(1, len(form.inner_trans_forms))
        
        