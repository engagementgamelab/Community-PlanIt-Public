############
Attachments
############


************
Requirements
************

`django-attachments` - forked version of `django-attachments` with an added dependency for django-model-utils. AttachmentManager extends model_utils.managers.InheritanceManager. https://github.com/bartTC/django-attachments

`django-model-utils`

************
Upgrade Instructions from cpi version 2
************

the legacy attachments app was renamed to attachments_v2 until the
datamigration will be completed and ran. After which the app will be
removed.

the legacy attachments table was renamed to attachments_v2_attachment.
this needs to be done manually.

    ALTER TABLE attachments_attachment RENAME TO attachments_v2_attachment

the new attachment-types defines attachment models that inherit from
attachments.Attachment. Inlines in use by the admin are defined for each
of the new attachment models are defined as well.


************
Attachments
************

.. _django-attachments: https://github.com/psychotechnik/django-attachments
.. _django-model-utils: http://pypi.python.org/pypi/django-model-utils
