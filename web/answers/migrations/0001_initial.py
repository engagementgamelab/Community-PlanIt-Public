# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Answer'
        db.create_table('answers_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['player_activities.PlayerActivity'])),
            ('answerUser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['auth.User'])),
            ('createDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('answers', ['Answer'])

        # Adding model 'AnswerSingleResponse'
        db.create_table('answers_answersingleresponse', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['answers.Answer'], unique=True, primary_key=True)),
            ('selected', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.MultiChoiceActivity'])),
        ))
        db.send_create_signal('answers', ['AnswerSingleResponse'])

        # Adding model 'AnswerMap'
        db.create_table('answers_answermap', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['answers.Answer'], unique=True, primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
        ))
        db.send_create_signal('answers', ['AnswerMap'])

        # Adding model 'AnswerMultiChoice'
        db.create_table('answers_answermultichoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.MultiChoiceActivity'])),
        ))
        db.send_create_signal('answers', ['AnswerMultiChoice'])

    def backwards(self, orm):
        
        # Deleting model 'Answer'
        db.delete_table('answers_answer')

        # Deleting model 'AnswerSingleResponse'
        db.delete_table('answers_answersingleresponse')

        # Deleting model 'AnswerMap'
        db.delete_table('answers_answermap')

        # Deleting model 'AnswerMultiChoice'
        db.delete_table('answers_answermultichoice')

    models = {
        'answers.answer': {
            'Meta': {'object_name': 'Answer'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['player_activities.PlayerActivity']"}),
            'answerUser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['auth.User']"}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'answers.answermap': {
            'Meta': {'object_name': 'AnswerMap', '_ormbases': ['answers.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['answers.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'map': ('gmapsfield.fields.GoogleMapsField', [], {})
        },
        'answers.answermultichoice': {
            'Meta': {'object_name': 'AnswerMultiChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.MultiChoiceActivity']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'answers.answersingleresponse': {
            'Meta': {'object_name': 'AnswerSingleResponse', '_ormbases': ['answers.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['answers.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'selected': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.MultiChoiceActivity']"})
        },
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
        'comments.comment': {
            'Meta': {'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'content_type_set_for_comment'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['instances.Instance']"}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_comments'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'object_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        'player_activities.playeractivitytype': {
            'Meta': {'object_name': 'PlayerActivityType'},
            'defaultPoints': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'displayType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['answers']
