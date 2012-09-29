# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attachment'
        #db.create_table('attachments_attachment', (
        #    ,
        #))
        #db.send_create_signal('attachment_types', ['Attachment'])

        # Adding model 'AttachmentHyperlink'
        db.create_table('attachment_types_attachmenthyperlink', (
            ('attachment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['attachments.Attachment'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('attachment_types', ['AttachmentHyperlink'])


        # Changing field 'AttachmentVideo.url'
        db.alter_column('attachment_types_attachmentvideo', 'url', self.gf('django.db.models.fields.URLField')(default='http://nodomain.com', max_length=200))

    def backwards(self, orm):
        # Deleting model 'Attachment'
        db.delete_table('attachments_attachment')

        # Deleting model 'AttachmentHyperlink'
        db.delete_table('attachment_types_attachmenthyperlink')


        # Changing field 'AttachmentVideo.url'
        db.alter_column('attachment_types_attachmentvideo', 'url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    models = {
        'attachment_types.attachment': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Attachment', 'db_table': "'attachments_attachment'", '_ormbases': ['attachments.Attachment'], 'proxy': 'True'}
        },
        'attachment_types.attachmenthyperlink': {
            'Meta': {'ordering': "['-created']", 'object_name': 'AttachmentHyperlink', '_ormbases': ['attachment_types.Attachment']},
            'attachment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['attachments.Attachment']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'attachment_types.attachmentvideo': {
            'Meta': {'ordering': "['-created']", 'object_name': 'AttachmentVideo', '_ormbases': ['attachment_types.Attachment']},
            'attachment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['attachments.Attachment']", 'unique': 'True', 'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'attachment_types.attachmentwiththumbnail': {
            'Meta': {'ordering': "['-created']", 'object_name': 'AttachmentWithThumbnail', '_ormbases': ['attachment_types.Attachment']},
            'attachment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['attachments.Attachment']", 'unique': 'True', 'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'attachments.attachment': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Attachment'},
            'attachment_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_attachments'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['attachment_types']
