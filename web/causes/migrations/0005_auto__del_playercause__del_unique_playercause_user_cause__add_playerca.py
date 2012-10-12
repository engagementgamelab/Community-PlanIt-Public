# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PlayerCause', fields ['user', 'cause']
        db.delete_unique('causes_playercause', ['user_id', 'cause_id'])

        # Deleting model 'PlayerCause'
        db.delete_table('causes_playercause')

        # Adding model 'PlayerCauseTransaction'
        db.create_table('causes_playercausetransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['causes.Cause'])),
            ('coins', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('causes', ['PlayerCauseTransaction'])

        # Adding unique constraint on 'PlayerCauseTransaction', fields ['user', 'cause']
        db.create_unique('causes_playercausetransaction', ['user_id', 'cause_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PlayerCauseTransaction', fields ['user', 'cause']
        db.delete_unique('causes_playercausetransaction', ['user_id', 'cause_id'])

        # Adding model 'PlayerCause'
        db.create_table('causes_playercause', (
            ('coins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['causes.Cause'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('causes', ['PlayerCause'])

        # Adding unique constraint on 'PlayerCause', fields ['user', 'cause']
        db.create_unique('causes_playercause', ['user_id', 'cause_id'])

        # Deleting model 'PlayerCauseTransaction'
        db.delete_table('causes_playercausetransaction')


    models = {
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
        'causes.cause': {
            'Meta': {'object_name': 'Cause'},
            'cause_type': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'causes'", 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'facebook_group_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'causes'", 'to': "orm['instances.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'causes.playercausetransaction': {
            'Meta': {'unique_together': "(('user', 'cause'),)", 'object_name': 'PlayerCauseTransaction'},
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['causes.Cause']"}),
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.basetreenode': {
            'Meta': {'object_name': 'BaseTreeNode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('polymorphic_tree.models.PolymorphicTreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['instances.BaseTreeNode']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_instances.basetreenode_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'instances.instance': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Instance', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'city': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True'}),
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'days_for_mission': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'is_disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['causes']