# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Challenge'
        db.create_table('challenges_challenge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('flagged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='challenges', to=orm['instances.Instance'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('game_type', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('challenges', ['Challenge'])

        # Adding M2M table for field attachments on 'Challenge'
        db.create_table('challenges_challenge_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challenge', models.ForeignKey(orm['challenges.challenge'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('challenges_challenge_attachments', ['challenge_id', 'attachment_id'])

        # Adding model 'PlayerChallenge'
        db.create_table('challenges_playerchallenge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('declined', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('response_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='player_challenge', unique=True, null=True, to=orm['responses.CommentResponse'])),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_challenges', to=orm['challenges.Challenge'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_challenges', to=orm['auth.User'])),
        ))
        db.send_create_signal('challenges', ['PlayerChallenge'])

        # Adding M2M table for field attachments on 'PlayerChallenge'
        db.create_table('challenges_playerchallenge_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playerchallenge', models.ForeignKey(orm['challenges.playerchallenge'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('challenges_playerchallenge_attachments', ['playerchallenge_id', 'attachment_id'])

    def backwards(self, orm):
        
        # Deleting model 'Challenge'
        db.delete_table('challenges_challenge')

        # Removing M2M table for field attachments on 'Challenge'
        db.delete_table('challenges_challenge_attachments')

        # Deleting model 'PlayerChallenge'
        db.delete_table('challenges_playerchallenge')

        # Removing M2M table for field attachments on 'PlayerChallenge'
        db.delete_table('challenges_playerchallenge_attachments')

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
        'challenges.challenge': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'Challenge'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attachments.Attachment']", 'symmetrical': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'challenges'", 'to': "orm['instances.Instance']"}),
            'map': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'challenges.playerchallenge': {
            'Meta': {'object_name': 'PlayerChallenge'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_challenges'", 'to': "orm['challenges.Challenge']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'declined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_challenges'", 'to': "orm['auth.User']"}),
            'response': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'player_challenge'", 'unique': 'True', 'null': 'True', 'to': "orm['responses.CommentResponse']"}),
            'response_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
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
        'responses.commentresponse': {
            'Meta': {'object_name': 'CommentResponse', '_ormbases': ['responses.Response']},
            'message': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '1000'}),
            'posted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': "''"}),
            'response_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['responses.Response']", 'unique': 'True', 'primary_key': 'True'})
        },
        'responses.response': {
            'Meta': {'object_name': 'Response'},
            'answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attachment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attachments.Attachment']", 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response_type': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['challenges']
