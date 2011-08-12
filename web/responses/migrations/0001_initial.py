# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on = (
        ("comments", "0001_initial"),
    )
    def forwards(self, orm):
        
        # Adding model 'Response'
        db.create_table('responses_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response_type', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('flagged', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('answer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('responses', ['Response'])

        # Adding M2M table for field attachment on 'Response'
        db.create_table('responses_response_attachment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('response', models.ForeignKey(orm['responses.response'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('responses_response_attachment', ['response_id', 'attachment_id'])

        # Adding M2M table for field comments on 'Response'
        db.create_table('responses_response_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('response', models.ForeignKey(orm['responses.response'], null=False)),
            ('comment', models.ForeignKey(orm['comments.comment'], null=False))
        ))
        db.create_unique('responses_response_comments', ['response_id', 'comment_id'])

        # Adding model 'MapResponse'
        db.create_table('responses_mapresponse', (
            ('response_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['responses.Response'], unique=True, primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='Point', max_length=260)),
            ('message', self.gf('django.db.models.fields.CharField')(default=' ', max_length=1000)),
        ))
        db.send_create_signal('responses', ['MapResponse'])

        # Adding model 'Choice'
        db.create_table('responses_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=260)),
        ))
        db.send_create_signal('responses', ['Choice'])

        # Adding model 'ChoicesResponse'
        db.create_table('responses_choicesresponse', (
            ('response_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['responses.Response'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('responses', ['ChoicesResponse'])

        # Adding M2M table for field choices on 'ChoicesResponse'
        db.create_table('responses_choicesresponse_choices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('choicesresponse', models.ForeignKey(orm['responses.choicesresponse'], null=False)),
            ('choice', models.ForeignKey(orm['responses.choice'], null=False))
        ))
        db.create_unique('responses_choicesresponse_choices', ['choicesresponse_id', 'choice_id'])

        # Adding model 'CommentResponse'
        db.create_table('responses_commentresponse', (
            ('response_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['responses.Response'], unique=True, primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(default=' ', max_length=1000)),
            ('posted_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('responses', ['CommentResponse'])


    def backwards(self, orm):
        
        # Deleting model 'Response'
        db.delete_table('responses_response')

        # Removing M2M table for field attachment on 'Response'
        db.delete_table('responses_response_attachment')

        # Removing M2M table for field comments on 'Response'
        db.delete_table('responses_response_comments')

        # Deleting model 'MapResponse'
        db.delete_table('responses_mapresponse')

        # Deleting model 'Choice'
        db.delete_table('responses_choice')

        # Deleting model 'ChoicesResponse'
        db.delete_table('responses_choicesresponse')

        # Removing M2M table for field choices on 'ChoicesResponse'
        db.delete_table('responses_choicesresponse_choices')

        # Deleting model 'CommentResponse'
        db.delete_table('responses_commentresponse')


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
        'comments.comment': {
            'Meta': {'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['comments.Comment']", 'symmetrical': 'False', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']"}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'liked_comments'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        'responses.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '260'})
        },
        'responses.choicesresponse': {
            'Meta': {'object_name': 'ChoicesResponse', '_ormbases': ['responses.Response']},
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['responses.Choice']", 'symmetrical': 'False'}),
            'response_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['responses.Response']", 'unique': 'True', 'primary_key': 'True'})
        },
        'responses.commentresponse': {
            'Meta': {'object_name': 'CommentResponse', '_ormbases': ['responses.Response']},
            'message': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1000'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'response_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['responses.Response']", 'unique': 'True', 'primary_key': 'True'})
        },
        'responses.mapresponse': {
            'Meta': {'object_name': 'MapResponse', '_ormbases': ['responses.Response']},
            'map': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'message': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1000'}),
            'response_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['responses.Response']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Point'", 'max_length': '260'})
        },
        'responses.response': {
            'Meta': {'object_name': 'Response'},
            'answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['comments.Comment']", 'symmetrical': 'False', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response_type': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['responses']
