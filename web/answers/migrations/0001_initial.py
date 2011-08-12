# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on = (
        ("player_activities", "0001_initial"),
    )

    def forwards(self, orm):
        
        # Adding model 'Answer'
        db.create_table('answers_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.PlayerActivity'])),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('addInstructions', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answerUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('answers', ['Answer'])

        # Adding model 'AnswerOpenEnded'
        db.create_table('answers_answeropenended', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['answers.Answer'], unique=True, primary_key=True)),
            ('answerbox', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('answers', ['AnswerOpenEnded'])

        # Adding model 'AnswerSingleResponse'
        db.create_table('answers_answersingleresponse', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['answers.Answer'], unique=True, primary_key=True)),
            ('selected', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player_activities.MultiChoiceActivity'])),
        ))
        db.send_create_signal('answers', ['AnswerSingleResponse'])

        # Adding model 'AnswerMap'
        db.create_table('answers_answermap', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['answers.Answer'], unique=True, primary_key=True)),
            ('answerBox', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maxNumMarkers', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('answers', ['AnswerMap'])

        # Adding model 'UserMapPoints'
        db.create_table('answers_usermappoints', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['answers.AnswerMap'])),
            ('point', self.gf('gmapsfield.fields.GoogleMapsField')()),
        ))
        db.send_create_signal('answers', ['UserMapPoints'])

        # Adding model 'AnswerEmpathy'
        db.create_table('answers_answerempathy', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['answers.Answer'], unique=True, primary_key=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answerBox', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('answers', ['AnswerEmpathy'])

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

        # Deleting model 'AnswerOpenEnded'
        db.delete_table('answers_answeropenended')

        # Deleting model 'AnswerSingleResponse'
        db.delete_table('answers_answersingleresponse')

        # Deleting model 'AnswerMap'
        db.delete_table('answers_answermap')

        # Deleting model 'UserMapPoints'
        db.delete_table('answers_usermappoints')

        # Deleting model 'AnswerEmpathy'
        db.delete_table('answers_answerempathy')

        # Deleting model 'AnswerMultiChoice'
        db.delete_table('answers_answermultichoice')


    models = {
        'answers.answer': {
            'Meta': {'object_name': 'Answer'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivity']"}),
            'addInstructions': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'answerUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'answers.answerempathy': {
            'Meta': {'object_name': 'AnswerEmpathy', '_ormbases': ['answers.Answer']},
            'answerBox': ('django.db.models.fields.TextField', [], {}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['answers.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'answers.answermap': {
            'Meta': {'object_name': 'AnswerMap', '_ormbases': ['answers.Answer']},
            'answerBox': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['answers.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'maxNumMarkers': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'answers.answermultichoice': {
            'Meta': {'object_name': 'AnswerMultiChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.MultiChoiceActivity']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'answers.answeropenended': {
            'Meta': {'object_name': 'AnswerOpenEnded', '_ormbases': ['answers.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['answers.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'answerbox': ('django.db.models.fields.TextField', [], {})
        },
        'answers.answersingleresponse': {
            'Meta': {'object_name': 'AnswerSingleResponse', '_ormbases': ['answers.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['answers.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'selected': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.MultiChoiceActivity']"})
        },
        'answers.usermappoints': {
            'Meta': {'object_name': 'UserMapPoints'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['answers.AnswerMap']"}),
            'point': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'curator': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'missions.mission': {
            'Meta': {'object_name': 'Mission'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'video': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'player_activities.multichoiceactivity': {
            'Meta': {'object_name': 'MultiChoiceActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'player_activities.playeractivity': {
            'Meta': {'object_name': 'PlayerActivity'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'createDate': ('django.db.models.fields.DateTimeField', [], {}),
            'creationUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['missions.Mission']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['player_activities.PlayerActivityType']"})
        },
        'player_activities.playeractivitytype': {
            'Meta': {'object_name': 'PlayerActivityType'},
            'defaultPoints': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['answers']
