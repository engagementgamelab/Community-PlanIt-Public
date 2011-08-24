# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PlayerActivityType'
        db.create_table('player_activities_playeractivitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('displayType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('defaultPoints', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('player_activities', ['PlayerActivityType'])

        # Adding model 'PlayerActivityTranslation'
        db.create_table('player_activities_playeractivitytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('addInstructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['player_activities.PlayerActivity'])),
        ))
        db.send_create_signal('player_activities', ['PlayerActivityTranslation'])

        # Adding unique constraint on 'PlayerActivityTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_playeractivitytranslation', ['language_code', 'master_id'])

        # Adding model 'PlayerActivity'
        db.create_table('player_activities_playeractivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('creationUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_activities_playeractivity_related', to=orm['missions.Mission'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.PlayerActivityType'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('player_activities', ['PlayerActivity'])

        # Adding M2M table for field attachment on 'PlayerActivity'
        db.create_table('player_activities_playeractivity_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playeractivity', models.ForeignKey(orm['player_activities.playeractivity'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('player_activities_playeractivity_attachment', ['playeractivity_id', 'attachment_id'])

        # Adding model 'PlayerMapActivityTranslation'
        db.create_table('player_activities_playermapactivitytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('addInstructions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['player_activities.PlayerMapActivity'])),
        ))
        db.send_create_signal('player_activities', ['PlayerMapActivityTranslation'])

        # Adding unique constraint on 'PlayerMapActivityTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_playermapactivitytranslation', ['language_code', 'master_id'])

        # Adding model 'PlayerMapActivity'
        db.create_table('player_activities_playermapactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('creationUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_activities_playermapactivity_related', to=orm['missions.Mission'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.PlayerActivityType'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('maxNumMarkers', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('player_activities', ['PlayerMapActivity'])

        # Adding M2M table for field attachment on 'PlayerMapActivity'
        db.create_table('player_activities_playermapactivity_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playermapactivity', models.ForeignKey(orm['player_activities.playermapactivity'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('player_activities_playermapactivity_attachment', ['playermapactivity_id', 'attachment_id'])

        # Adding model 'PlayerEmpathyActivityTranslation'
        db.create_table('player_activities_playerempathyactivitytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['player_activities.PlayerEmpathyActivity'])),
        ))
        db.send_create_signal('player_activities', ['PlayerEmpathyActivityTranslation'])

        # Adding unique constraint on 'PlayerEmpathyActivityTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_playerempathyactivitytranslation', ['language_code', 'master_id'])

        # Adding model 'PlayerEmpathyActivity'
        db.create_table('player_activities_playerempathyactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('creationUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_activities_playerempathyactivity_related', to=orm['missions.Mission'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.PlayerActivityType'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('player_activities', ['PlayerEmpathyActivity'])

        # Adding M2M table for field attachment on 'PlayerEmpathyActivity'
        db.create_table('player_activities_playerempathyactivity_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playerempathyactivity', models.ForeignKey(orm['player_activities.playerempathyactivity'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('player_activities_playerempathyactivity_attachment', ['playerempathyactivity_id', 'attachment_id'])

        # Adding model 'MultiChoiceActivityTranslation'
        db.create_table('player_activities_multichoiceactivitytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['player_activities.MultiChoiceActivity'])),
        ))
        db.send_create_signal('player_activities', ['MultiChoiceActivityTranslation'])

        # Adding unique constraint on 'MultiChoiceActivityTranslation', fields ['language_code', 'master']
        db.create_unique('player_activities_multichoiceactivitytranslation', ['language_code', 'master_id'])

        # Adding model 'MultiChoiceActivity'
        db.create_table('player_activities_multichoiceactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.PlayerActivity'])),
        ))
        db.send_create_signal('player_activities', ['MultiChoiceActivity'])

    def backwards(self, orm):
        
        # Removing unique constraint on 'MultiChoiceActivityTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_multichoiceactivitytranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'PlayerEmpathyActivityTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_playerempathyactivitytranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'PlayerMapActivityTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_playermapactivitytranslation', ['language_code', 'master_id'])

        # Removing unique constraint on 'PlayerActivityTranslation', fields ['language_code', 'master']
        db.delete_unique('player_activities_playeractivitytranslation', ['language_code', 'master_id'])

        # Deleting model 'PlayerActivityType'
        db.delete_table('player_activities_playeractivitytype')

        # Deleting model 'PlayerActivityTranslation'
        db.delete_table('player_activities_playeractivitytranslation')

        # Deleting model 'PlayerActivity'
        db.delete_table('player_activities_playeractivity')

        # Removing M2M table for field attachment on 'PlayerActivity'
        db.delete_table('player_activities_playeractivity_attachment')

        # Deleting model 'PlayerMapActivityTranslation'
        db.delete_table('player_activities_playermapactivitytranslation')

        # Deleting model 'PlayerMapActivity'
        db.delete_table('player_activities_playermapactivity')

        # Removing M2M table for field attachment on 'PlayerMapActivity'
        db.delete_table('player_activities_playermapactivity_attachment')

        # Deleting model 'PlayerEmpathyActivityTranslation'
        db.delete_table('player_activities_playerempathyactivitytranslation')

        # Deleting model 'PlayerEmpathyActivity'
        db.delete_table('player_activities_playerempathyactivity')

        # Removing M2M table for field attachment on 'PlayerEmpathyActivity'
        db.delete_table('player_activities_playerempathyactivity_attachment')

        # Deleting model 'MultiChoiceActivityTranslation'
        db.delete_table('player_activities_multichoiceactivitytranslation')

        # Deleting model 'MultiChoiceActivity'
        db.delete_table('player_activities_multichoiceactivity')

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
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'missions.mission': {
            'Meta': {'object_name': 'Mission'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'missions'", 'to': "orm['instances.Instance']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'video': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'player_activities.multichoiceactivity': {
            'Meta': {'object_name': 'MultiChoiceActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'player_activities.multichoiceactivitytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'MultiChoiceActivityTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['player_activities.MultiChoiceActivity']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'player_activities.playeractivity': {
            'Meta': {'object_name': 'PlayerActivity'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_activities_playeractivity_related'", 'to': "orm['missions.Mission']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivityType']"})
        },
        'player_activities.playeractivitytranslation': {
            'Meta': {'ordering': "['name']", 'unique_together': "[('language_code', 'master')]", 'object_name': 'PlayerActivityTranslation'},
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['player_activities.PlayerActivity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'player_activities.playeractivitytype': {
            'Meta': {'object_name': 'PlayerActivityType'},
            'defaultPoints': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'displayType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'player_activities.playerempathyactivity': {
            'Meta': {'object_name': 'PlayerEmpathyActivity'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_activities_playerempathyactivity_related'", 'to': "orm['missions.Mission']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivityType']"})
        },
        'player_activities.playerempathyactivitytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'PlayerEmpathyActivityTranslation'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['player_activities.PlayerEmpathyActivity']"})
        },
        'player_activities.playermapactivity': {
            'Meta': {'object_name': 'PlayerMapActivity'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxNumMarkers': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_activities_playermapactivity_related'", 'to': "orm['missions.Mission']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivityType']"})
        },
        'player_activities.playermapactivitytranslation': {
            'Meta': {'ordering': "['name']", 'unique_together': "[('language_code', 'master')]", 'object_name': 'PlayerMapActivityTranslation'},
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': "orm['player_activities.PlayerMapActivity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['player_activities']
