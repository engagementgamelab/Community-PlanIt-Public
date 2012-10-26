# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AnswerWithOneChoice'
        db.delete_table('challenges_answerwithonechoice')

        # Deleting model 'AnswerEmpathy'
        db.delete_table('challenges_answerempathy')

        # Deleting model 'AnswerMap'
        db.delete_table('challenges_answermap')

        # Deleting model 'Answer'
        db.delete_table('challenges_answer')

        # Deleting model 'AnswerOpenEnded'
        db.delete_table('challenges_answeropenended')

        # Deleting model 'AnswerWithMultipleChoices'
        db.delete_table('challenges_answerwithmultiplechoices')

        # Removing M2M table for field selected on 'AnswerWithMultipleChoices'
        db.delete_table('challenges_answerwithmultiplechoices_selected')

        # Adding model 'ChallengeAnswerWithOneChoice'
        db.create_table('challenges_challengeanswerwithonechoice', (
            ('challengeanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.ChallengeAnswer'], unique=True, primary_key=True)),
            ('selected', self.gf('django.db.models.fields.related.OneToOneField')(related_name='singleresponse_answers', unique=True, to=orm['challenges.AnswerChoice'])),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='singleresponse_answers', to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['ChallengeAnswerWithOneChoice'])

        # Adding model 'ChallengeAnswerWithMultipleChoices'
        db.create_table('challenges_challengeanswerwithmultiplechoices', (
            ('challengeanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.ChallengeAnswer'], unique=True, primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='multiresponse_answers', to=orm['challenges.Challenge'])),
        ))
        db.send_create_signal('challenges', ['ChallengeAnswerWithMultipleChoices'])

        # Adding M2M table for field selected on 'ChallengeAnswerWithMultipleChoices'
        db.create_table('challenges_challengeanswerwithmultiplechoices_selected', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challengeanswerwithmultiplechoices', models.ForeignKey(orm['challenges.challengeanswerwithmultiplechoices'], null=False)),
            ('answerchoice', models.ForeignKey(orm['challenges.answerchoice'], null=False))
        ))
        db.create_unique('challenges_challengeanswerwithmultiplechoices_selected', ['challengeanswerwithmultiplechoices_id', 'answerchoice_id'])

        # Adding model 'ChallengeAnswer'
        db.create_table('challenges_challengeanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_challenges.challengeanswer_set', null=True, to=orm['contenttypes.ContentType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('challenges', ['ChallengeAnswer'])

        # Adding model 'ChallengeAnswerOpenEnded'
        db.create_table('challenges_challengeansweropenended', (
            ('challengeanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.ChallengeAnswer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='openended_answers', to=orm['challenges.OpenEndedChallenge'])),
        ))
        db.send_create_signal('challenges', ['ChallengeAnswerOpenEnded'])

        # Adding model 'ChallengeAnswerMap'
        db.create_table('challenges_challengeanswermap', (
            ('challengeanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.ChallengeAnswer'], unique=True, primary_key=True)),
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='map_answers', to=orm['challenges.MapChallenge'])),
        ))
        db.send_create_signal('challenges', ['ChallengeAnswerMap'])

        # Adding model 'ChallengeAnswerEmpathy'
        db.create_table('challenges_challengeanswerempathy', (
            ('challengeanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.ChallengeAnswer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='empathy_answers', to=orm['challenges.EmpathyChallenge'])),
        ))
        db.send_create_signal('challenges', ['ChallengeAnswerEmpathy'])


    def backwards(self, orm):
        # Adding model 'AnswerWithOneChoice'
        db.create_table('challenges_answerwithonechoice', (
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='singleresponse_answers', to=orm['challenges.Challenge'])),
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('selected', self.gf('django.db.models.fields.related.OneToOneField')(related_name='singleresponse_answers', unique=True, to=orm['challenges.AnswerChoice'])),
        ))
        db.send_create_signal('challenges', ['AnswerWithOneChoice'])

        # Adding model 'AnswerEmpathy'
        db.create_table('challenges_answerempathy', (
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='empathy_answers', to=orm['challenges.EmpathyChallenge'])),
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
        ))
        db.send_create_signal('challenges', ['AnswerEmpathy'])

        # Adding model 'AnswerMap'
        db.create_table('challenges_answermap', (
            ('map', self.gf('gmapsfield.fields.GoogleMapsField')()),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='map_answers', to=orm['challenges.MapChallenge'])),
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('challenges', ['AnswerMap'])

        # Adding model 'Answer'
        db.create_table('challenges_answer', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['auth.User'])),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_challenges.answer_set', null=True, to=orm['contenttypes.ContentType'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('challenges', ['Answer'])

        # Adding model 'AnswerOpenEnded'
        db.create_table('challenges_answeropenended', (
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='openended_answers', to=orm['challenges.OpenEndedChallenge'])),
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', max_length=1000)),
        ))
        db.send_create_signal('challenges', ['AnswerOpenEnded'])

        # Adding model 'AnswerWithMultipleChoices'
        db.create_table('challenges_answerwithmultiplechoices', (
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='multiresponse_answers', to=orm['challenges.Challenge'])),
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['challenges.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('challenges', ['AnswerWithMultipleChoices'])

        # Adding M2M table for field selected on 'AnswerWithMultipleChoices'
        db.create_table('challenges_answerwithmultiplechoices_selected', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('answerwithmultiplechoices', models.ForeignKey(orm['challenges.answerwithmultiplechoices'], null=False)),
            ('answerchoice', models.ForeignKey(orm['challenges.answerchoice'], null=False))
        ))
        db.create_unique('challenges_answerwithmultiplechoices_selected', ['answerwithmultiplechoices_id', 'answerchoice_id'])

        # Deleting model 'ChallengeAnswerWithOneChoice'
        db.delete_table('challenges_challengeanswerwithonechoice')

        # Deleting model 'ChallengeAnswerWithMultipleChoices'
        db.delete_table('challenges_challengeanswerwithmultiplechoices')

        # Removing M2M table for field selected on 'ChallengeAnswerWithMultipleChoices'
        db.delete_table('challenges_challengeanswerwithmultiplechoices_selected')

        # Deleting model 'ChallengeAnswer'
        db.delete_table('challenges_challengeanswer')

        # Deleting model 'ChallengeAnswerOpenEnded'
        db.delete_table('challenges_challengeansweropenended')

        # Deleting model 'ChallengeAnswerMap'
        db.delete_table('challenges_challengeanswermap')

        # Deleting model 'ChallengeAnswerEmpathy'
        db.delete_table('challenges_challengeanswerempathy')


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
        'challenges.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_choices'", 'to': "orm['challenges.Challenge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_barrier_correct_answer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'challenges.barrierchallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'BarrierChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'}),
            'minimum_coins_to_play': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'challenges.challenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'Challenge', '_ormbases': ['instances.BaseTreeNode']},
            'basetreenode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['instances.BaseTreeNode']", 'unique': 'True', 'primary_key': 'True'}),
            'challenge_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_player_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'challenges.challengeanswer': {
            'Meta': {'object_name': 'ChallengeAnswer'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_challenges.challengeanswer_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['auth.User']"})
        },
        'challenges.challengeanswerempathy': {
            'Meta': {'object_name': 'ChallengeAnswerEmpathy', '_ormbases': ['challenges.ChallengeAnswer']},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'empathy_answers'", 'to': "orm['challenges.EmpathyChallenge']"}),
            'challengeanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.ChallengeAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000'})
        },
        'challenges.challengeanswermap': {
            'Meta': {'object_name': 'ChallengeAnswerMap', '_ormbases': ['challenges.ChallengeAnswer']},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'map_answers'", 'to': "orm['challenges.MapChallenge']"}),
            'challengeanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.ChallengeAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'map': ('gmapsfield.fields.GoogleMapsField', [], {})
        },
        'challenges.challengeansweropenended': {
            'Meta': {'object_name': 'ChallengeAnswerOpenEnded', '_ormbases': ['challenges.ChallengeAnswer']},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'openended_answers'", 'to': "orm['challenges.OpenEndedChallenge']"}),
            'challengeanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.ChallengeAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000'})
        },
        'challenges.challengeanswerwithmultiplechoices': {
            'Meta': {'object_name': 'ChallengeAnswerWithMultipleChoices', '_ormbases': ['challenges.ChallengeAnswer']},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'multiresponse_answers'", 'to': "orm['challenges.Challenge']"}),
            'challengeanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.ChallengeAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'selected': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'multiresponse_answers'", 'symmetrical': 'False', 'to': "orm['challenges.AnswerChoice']"})
        },
        'challenges.challengeanswerwithonechoice': {
            'Meta': {'object_name': 'ChallengeAnswerWithOneChoice', '_ormbases': ['challenges.ChallengeAnswer']},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'singleresponse_answers'", 'to': "orm['challenges.Challenge']"}),
            'challengeanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.ChallengeAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'selected': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'singleresponse_answers'", 'unique': 'True', 'to': "orm['challenges.AnswerChoice']"})
        },
        'challenges.empathychallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'EmpathyChallenge', '_ormbases': ['challenges.Challenge']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio_text': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1000'}),
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.finalbarrierchallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'FinalBarrierChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.mapchallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'MapChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'}),
            'maxNumMarkers': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'challenges.multiresponsechallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'MultiResponseChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'}),
            'require_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'challenges.openendedchallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'OpenEndedChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'challenges.singleresponsechallenge': {
            'Meta': {'ordering': "('lft',)", 'object_name': 'SingleResponseChallenge', '_ormbases': ['challenges.Challenge']},
            'challenge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['challenges.Challenge']", 'unique': 'True', 'primary_key': 'True'})
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
        }
    }

    complete_apps = ['challenges']