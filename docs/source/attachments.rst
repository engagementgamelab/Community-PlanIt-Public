############
Attachments
############


Requirements
------------

* `django-attachments`_

* `django-model-utils`_

.. note:: 

    forked version of `django-attachments`_ with an added dependency for django-model-utils.     AttachmentManager extends model_utils.managers.InheritanceManager. 
    https://github.com/bartTC/django-attachments



.. _django-attachments: https://github.com/psychotechnik/django-attachments
.. _django-model-utils: http://pypi.python.org/pypi/django-model-utils

************
Upgrade Instructions from Community PlanIt V2
************

the legacy attachments app was renamed to attachments_v2 until the
datamigration will be completed and ran. After which the app will be
removed.

the legacy attachments table was renamed to attachments_v2_attachment.
this needs to be done manually.

    ALTER TABLE attachments_attachment RENAME TO attachments_v2_attachment;

Usage
-----
the new attachment-types defines attachment models that inherit from
attachments.Attachment. Inlines in use by the admin are defined for each
of the new attachment models are defined as well.


To query for the new attachment subclasses use ``model_utils.managers.InheritanceManager.select_subclasses``::

Example::

    Attachment.objects.filter().select_subclasses('attachmentvideo')

************
Attachments
************

