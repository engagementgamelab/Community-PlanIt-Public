# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Game'
        db.create_table('games_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_type', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('games', ['Game'])

        # Adding model 'PlayerGame'
        db.create_table('games_playergame', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.Response'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['games.Game'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('games', ['PlayerGame'])

        # Adding M2M table for field comments on 'PlayerGame'
        db.create_table('games_playergame_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playergame', models.ForeignKey(orm['games.playergame'], null=False)),
            ('comment', models.ForeignKey(orm['comments.comment'], null=False))
        ))
        db.create_unique('games_playergame_comments', ['playergame_id', 'comment_id'])

        # Adding model 'OtherShoes'
        db.create_table('games_othershoes', (
            ('game_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['games.Game'], unique=True, primary_key=True)),
            ('prompt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prompts.ProfilePrompt'], null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.CommentResponse'], null=True, blank=True)),
        ))
        db.send_create_signal('games', ['OtherShoes'])

        # Adding model 'ThinkFast'
        db.create_table('games_thinkfast', (
            ('game_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['games.Game'], unique=True, primary_key=True)),
            ('prompt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prompts.BasicPrompt'], null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.ChoicesResponse'], null=True, blank=True)),
        ))
        db.send_create_signal('games', ['ThinkFast'])

        # Adding model 'Mapit'
        db.create_table('games_mapit', (
            ('game_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['games.Game'], unique=True, primary_key=True)),
            ('prompt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prompts.BasicPrompt'], null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['responses.MapResponse'], null=True, blank=True)),
        ))
        db.send_create_signal('games', ['Mapit'])


    def backwards(self, orm):
        
        # Deleting model 'Game'
        db.delete_table('games_game')

        # Deleting model 'PlayerGame'
        db.delete_table('games_playergame')

        # Removing M2M table for field comments on 'PlayerGame'
        db.delete_table('games_playergame_comments')

        # Deleting model 'OtherShoes'
        db.delete_table('games_othershoes')

        # Deleting model 'ThinkFast'
        db.delete_table('games_thinkfast')

        # Deleting model 'Mapit'
        db.delete_table('games_mapit')


    models = {
        'attachments.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instances.Instance']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'game_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'games.mapit': {
            'Meta': {'object_name': 'Mapit', '_ormbases': ['games.Game']},
            'game_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['games.Game']", 'unique': 'True', 'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prompts.BasicPrompt']", 'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['responses.MapResponse']", 'null': 'True', 'blank': 'True'})
        },
        'games.othershoes': {
            'Meta': {'object_name': 'OtherShoes', '_ormbases': ['games.Game']},
            'game_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['games.Game']", 'unique': 'True', 'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prompts.ProfilePrompt']", 'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['responses.CommentResponse']", 'null': 'True', 'blank': 'True'})
        },
        'games.playergame': {
            'Meta': {'object_name': 'PlayerGame'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['comments.Comment']", 'null': 'True', 'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['games.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['responses.Response']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'games.thinkfast': {
            'Meta': {'object_name': 'ThinkFast', '_ormbases': ['games.Game']},
            'game_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['games.Game']", 'unique': 'True', 'primary_key': 'True'}),
            'prompt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prompts.BasicPrompt']", 'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['responses.ChoicesResponse']", 'null': 'True', 'blank': 'True'})
        },
        'instances.instance': {
            'Meta': {'object_name': 'Instance'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'curator': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('gmapsfield.fields.GoogleMapsField', [], {}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'prompts.basicprompt': {
            'Meta': {'object_name': 'BasicPrompt', '_ormbases': ['prompts.Prompt']},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'basicprompt_game'", 'null': 'True', 'to': "orm['games.Game']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '260'}),
            'prompt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['prompts.Prompt']", 'unique': 'True', 'primary_key': 'True'})
        },
        'prompts.profileprompt': {
            'Meta': {'object_name': 'ProfilePrompt', '_ormbases': ['prompts.Prompt']},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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
            'game': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapresponse_game'", 'null': 'True', 'to': "orm['games.Game']"}),
            'map': ('gmapsfield.fields.GoogleMapsField', [], {}),
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

    complete_apps = ['games']
