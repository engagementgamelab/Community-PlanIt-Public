# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Prompt'
        db.create_table('prompts_prompt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prompt_type', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('download', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='get_prompt_download', null=True, to=orm['attachments.Attachment'])),
        ))
        db.send_create_signal('prompts', ['Prompt'])

        # Adding M2M table for field attachments on 'Prompt'
        db.create_table('prompts_prompt_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prompt', models.ForeignKey(orm['prompts.prompt'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('prompts_prompt_attachments', ['prompt_id', 'attachment_id'])

        # Adding model 'BasicPrompt'
        db.create_table('prompts_basicprompt', (
            ('prompt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['prompts.Prompt'], unique=True, primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=260)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='basicprompt_game', null=True, to=orm['games.Game'])),
        ))
        db.send_create_signal('prompts', ['BasicPrompt'])

        # Adding model 'MapPrompt'
        db.create_table('prompts_mapprompt', (
            ('prompt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['prompts.Prompt'], unique=True, primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
        ))
        db.send_create_signal('prompts', ['MapPrompt'])

        # Adding model 'ProfilePrompt'
        db.create_table('prompts_profileprompt', (
            ('prompt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['prompts.Prompt'], unique=True, primary_key=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=125, null=True, blank=True)),
        ))
        db.send_create_signal('prompts', ['ProfilePrompt'])


    def backwards(self, orm):
        
        # Deleting model 'Prompt'
        db.delete_table('prompts_prompt')

        # Removing M2M table for field attachments on 'Prompt'
        db.delete_table('prompts_prompt_attachments')

        # Deleting model 'BasicPrompt'
        db.delete_table('prompts_basicprompt')

        # Deleting model 'MapPrompt'
        db.delete_table('prompts_mapprompt')

        # Deleting model 'ProfilePrompt'
        db.delete_table('prompts_profileprompt')


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
        'games.game': {
            'Meta': {'object_name': 'Game'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['comments.Comment']", 'null': 'True', 'blank': 'True'}),
            'game_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['missions.Mission']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'})
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
        'prompts.basicprompt': {
            'Meta': {'object_name': 'BasicPrompt', '_ormbases': ['prompts.Prompt']},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'basicprompt_game'", 'null': 'True', 'to': "orm['games.Game']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '260'}),
            'prompt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['prompts.Prompt']", 'unique': 'True', 'primary_key': 'True'})
        },
        'prompts.mapprompt': {
            'Meta': {'object_name': 'MapPrompt', '_ormbases': ['prompts.Prompt']},
            'map': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'prompt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['prompts.Prompt']", 'unique': 'True', 'primary_key': 'True'})
        },
        'prompts.profileprompt': {
            'Meta': {'object_name': 'ProfilePrompt', '_ormbases': ['prompts.Prompt']},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'prompt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['prompts.Prompt']", 'unique': 'True', 'primary_key': 'True'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True', 'blank': 'True'})
        },
        'prompts.prompt': {
            'Meta': {'object_name': 'Prompt'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attachments.Attachment']", 'symmetrical': 'False', 'blank': 'True'}),
            'download': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'get_prompt_download'", 'null': 'True', 'to': "orm['attachments.Attachment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prompt_type': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['prompts']
