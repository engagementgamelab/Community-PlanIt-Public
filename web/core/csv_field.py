from django.db import models

class CSVField(models.TextField):

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.delimeter = kwargs.pop("delimeter", ',')
        super(CSVField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        return value.split(self.delimeter)

    def get_db_prep_value(self, value, connection, prepared=False):
        return self.delimeter.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([
    ([CSVField], [],{},),
], ["^web\.core\.csv_field\.CSVField"])

