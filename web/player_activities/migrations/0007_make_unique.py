# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'PlayerActivity', fields ['type', 'name', 'mission']
        db.create_unique('player_activities_playeractivity', ['type_id', 'name', 'mission_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PlayerActivity', fields ['type', 'name', 'mission']
        db.delete_unique('player_activities_playeractivity', ['type_id', 'name', 'mission_id'])


    models = {
        'attachments.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']", 'null': 'True', 'blank': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_validity_check': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
        },
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'process_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'process_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'missions.mission': {
            'Meta': {'object_name': 'Mission'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'missions'", 'to': "orm['instances.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'video': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'player_activities.multichoiceactivity': {
            'Meta': {'object_name': 'MultiChoiceActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'player_activities.playeractivity': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'mission', 'type'),)", 'object_name': 'PlayerActivity'},
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': "orm['missions.Mission']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivityType']"})
        },
        'player_activities.playeractivitytype': {
            'Meta': {'object_name': 'PlayerActivityType'},
            'defaultPoints': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'displayType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'player_activities.playerempathyactivity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PlayerEmpathyActivity', '_ormbases': ['player_activities.PlayerActivity']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'playeractivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['player_activities.PlayerActivity']", 'unique': 'True', 'primary_key': 'True'})
        },
        'player_activities.playermapactivity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PlayerMapActivity', '_ormbases': ['player_activities.PlayerActivity']},
            'maxNumMarkers': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'playeractivity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['player_activities.PlayerActivity']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['player_activities']
