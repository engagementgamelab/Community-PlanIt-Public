from django.contrib.auth.models import User
from instances.models import Instance, Language
from values.models import Value


def create_fixtures():
    """
    Create initial data for tests.
    """
    su = User.objects.get_or_create(
            email='admin@admin.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            username='admin',
    )[0]
    su.set_password('admin')
    su.save()
    
    language = Language.objects.create(code='en', name='English')
    
    en_instance = Instance.objects.language('en').create(
            slug='test',
            title='Test Title',
            city='Los Angeles',
            state='CA',
            start_date='2011-09-05 00:48:40',           
            location='{"coordinates":[0,0],"zoom":16,"markers":[{"coordinates":[0,0]}],"type":"Point"}',
            name='English',
            description='EnglishDesc'
    )     
    en_instance.languages = (language,)
    en_instance.save()  
    
    es_instance = en_instance.translate('es')
    es_instance.name = "Es test"
    es_instance.description = "Es test description"
    es_instance.save()
    
    ht_instance = en_instance.translate('ht')
    ht_instance.name = "Ht test"
    ht_instance.description = "Ht test description"
    ht_instance.save()    
    
    Value.objects.create(instance=en_instance, message="test")
    